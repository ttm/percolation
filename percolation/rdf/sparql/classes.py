__doc__ = """

NOTES:
    INSERTs and DELETEs without a WHERE clause have the DATA keyword:
        INSERT DATA { ... } DELETE DATA { ... }.
    DELETE INSERT WHERE queries can't swap to INSERT DELETE WHERE.
        (The DELETE WHERE is in fact a D I W query without I)
    URI: tdb:unionDefaultGraph the union graph
        (don't seem to work now, maybe bugged)
    URI: urn:x-arq:DefaultGraph the default graph
        (seem to work)

Example query where delete, insert and where are sequences of triples.
querystring=P.sparql.functions.buildQuery(
             triples1=delete,graph1=self.graphidAUX,
             triples2=insert,graph2=self.graphidAUX,
             triples3=where, graph3=self.graphidAUX,
             body3modifier=startB3_,body3close_=body3close_,
             method="delete_insert_where")
"""

import os
import rdflib as r
import networkx as x
import percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
from percolation.rdf import NS
c = P.check

default = NS.po.MainGraph+"#1"
default = "default"
default = "urn:x-arq:DefaultGraph"
default = None
g = r.Graph()
# g.addN(P.rdf.makeMetadata())


class SparQLClient:
    """Fuseki connection maintainer through rdflib"""
    def __init__(self, endpoint_url):
        self.endpoint = SPARQLWrapper(endpoint_url)
        self.endpoint_url = endpoint_url
        self.endpoint.setTimeout(10*60)

    def addLocalFileToEndpoint(self, tfile, tgraph=default):
        cmd = "s-post {} {} {}".format(self.endpoint_url, tgraph, tfile)
        self.cmdline = cmd
        os.system(cmd)

    def removeLocalFileFromEndpoint(self, tfile, tgraph=default):
        cmd = "s-delete {} {} {}".format(self.endpoint_url, tgraph, tfile)
        os.system(cmd)

    def restablishConnection(self, endpoint_url=None):
        if not endpoint_url:
            endpoint_url = self.endpoint_url
        self.endpoint = SPARQLWrapper(endpoint_url)
        self.endpoint_url = endpoint_url
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)


class SparQLQueries:
    """Covenience class for inheritance with SparQLClient and SparQLLegacy"""
    iquery = []
    rquery = []

    def clearEndpoint(self, tgraph=default):
        if tgraph:
            query = r"CLEAR GRAPH <%s>" % (tgraph,)
            query = r"DROP GRAPH <%s> " % (tgraph,)
        else:
            graphs = self.getAllGraphs()
            for graph in graphs:
                self.clearEndpoint(graph.split("/")[-1])
            query = "CLEAR DEFAULT"
        self.updateQuery(query)

    def addRemoteFileToEndpoint(self, remote_file_url, tgraph=default):
        part1 = "LOAD <%s> " % (remote_file_url)
        if tgraph:
            part2 = " [ INTO <%s> ] " % (tgraph,)
        query = part1+part2
        self.updateQuery(query)
        raise NotImplementedError("Need to validate. Never been used")

    def insertTriples(self, triples, graph1=default):
        querystring = P.rdf.sparql.functions.buildQuery(triples, graph1=graph1,
                                                        method="insert")
        self.iquery += [querystring]
        self.result = self.updateQuery(querystring)

    def retrieveFromTriples(self, triples, graph1=default, modifier1="",
                            startB_=None):
        querystring = P.rdf.sparql.functions.buildQuery(
            triples, graph1=graph1, modifier1=modifier1, startB_=startB_)
        self.rquery += [querystring]
        return self.retrieveQuery(querystring)

    def retrieveQuery(self, querystring):
        """Query for retrieving information (e.g. through select)"""
        self.endpoint.method = "GET"
        self.endpoint.setReturnFormat(JSON)
        self.endpoint.setTimeout(10*60)
        return self.performQuery(querystring)

    def updateQuery(self, querystring):
        """Query to insert, delete and modify knowledge
        https://www.w3.org/Submission/SPARQL-Update/"""
        # self.endpoint.method = "POST"
        return self.performQuery(querystring)

    def performQuery(self, querystring):
        """Query method is defined at SparQLClient initialization."""
        # self.method=POST
        self.endpoint.setQuery(querystring)
        return self.endpoint.queryAndConvert()

    def getAllTriples(self, graph1=default):
        qtriples = (("?s", "?p", "?o"),)
        self.triples = P.rdf.sparql.functions.plainQueryValues(
            self.retrieveFromTriples(qtriples, graph1=graph1)
        )
        return self.triples

    def getNTriples(self, graph1=default):
        qtriples = (("?s", "?p", "?o"),)
        self.ntriples = P.rdf.sparql.functions.plainQueryValues(
            self.retrieveFromTriples(
                qtriples, graph1=graph1, startB_=" (COUNT(*) as ?nt) WHERE { ")
        )[0]
        return self.ntriples
    def getAllGraphs(self):
        query=r"SELECT DISTINCT ?g WHERE { GRAPH ?g {?s ?p ?o} }"
        self.graphs= P.rdf.sparql.functions.plainQueryValues(
            self.retrieveQuery(query)
        )
        return self.graphs
    def getNGraphs(self):
        query=r"SELECT (COUNT(?g) as ?cg) WHERE { GRAPH ?g {} }"
        self.ngraphs = self.retrieveQuery(
            query)["results"]["bindings"][0]["cg"]["value"]
        return self.ngraphs

    def insertOntology(self, graph1=default):
        self.insertTriples(P.rdf.makeOntology(), graph1=graph1)
        # self.getNTriples(),
        # P.utils.writeTriples(self.triples,"{}dummy.ttl".format(triples_dir))


endpoint_url_ = os.getenv("PERCOLATION_ENDPOINT")


class Client(SparQLClient, SparQLQueries):
    """Class that holds sparql endpoint connection and convenienves for query"""
    def __init__(self, endpoint_url=endpoint_url_):
        SparQLClient.__init__(self, endpoint_url)


class SparQLLegacyConvenience:
    """Convenience class for query and renderind analysis structures,
    tables and figures"""
    def makeNetwork(self, relation_uri, label_uri=None, rtype=1,
                    directed=False):
        """Make network from data SparQL queried in endpoint_url.

        relation_uri: hold the predicate uri to which individuals are
                      the range or oboth range and domain.
        label_uri: hold the predicate to which the range is the label
                   (e.g. name or nick) of the individual.
        rtype: indicate which type of structure to be queried, as exposed in:
               http://ttm.github.io/doc/semantic/report/2015/12/05/\
                   semantic-social-networks.html
               directed indicated weather the resulting network is
               a digraph or not.
        """
        sparql = self.endpoint
        if label_uri:
            mvars = "i1", "l1", "i2", "l2"
            label_qpart = """?i1  {} ?l1 .
                          ?i2  {} ?l2 .""".format(label_uri, label_uri)
        else:
            mvars = "i1", "i2"
            label_qpart = ""
        tvars = " ".join(["?{}" for i in mvars])
        if rtype == 1:  # direct relation
            query = """SELECT  {}
                       WHERE {{ ?i1  {} ?i2 .
                                     {}      }}""".format(
                                         tvars, relation_uri, label_qpart)
        elif rtype == 2:  # mediated relation
            query = """SELECT  {}
                       WHERE {{ ?foo  {} ?i1 .
                                ?foo  {} ?i2 .
                                      {}      }}""".format(
                               tvars, relation_uri, relation_uri, label_qpart)
        elif rtype == 3:  # twice mediated relation
            query = """SELECT  {}
                       WHERE {{ ?foo  ?baz ?bar .
                                ?foo   {} ?i1 .
                                ?bar   {} ?i2 .
                                       {}      }}""".format(
                             tvars, relation_uri, relation_uri, label_qpart)
        else:
            raise ValueError("rtype --> {} <-- not valid".format(rtype))
        c("query build ok")
        res = P.utils.mQuery(sparql, query, mvars)
        c("response received")
        if directed:
            dg = x.DiGraph()
        else:
            dg = x.Graph()
        for rel in res:
            id1, l1, id2, l2 = rel
            if dg.has_node(id1):
                dg.node[id1]["weight"] += 1.
            else:
                dg.add_node(id1, label=l1, weight=1.)
            if dg.has_node(id2):
                dg.node[id2]["weight"] += 1.
            else:
                dg.add_node(id2, label=l2, weight=1.)
            if dg.has_edge(id1, id2):
                dg[id1][id2]["weight"] += 1.
            else:
                dg.add_edge(id1, id2, weight=2.)
        c("graph done")
        return dg


class LegacyClient(SparQLClient, SparQLQueries, SparQLLegacyConvenience):
    """Class that holds sparql endpoint connection and convenienves for
    query and renderind analysis strictures, tables and figures"""
    def __init__(self, endpoint_url):
        SparQLClient.__init__(self, endpoint_url)
        SparQLLegacyConvenience.__init__(self)

if __name__ == "__main__":
    endpoint_url = os.getenv("PERCOLATION_ENDPOINT")
    if not endpoint_url:
        endpoint_url = input("please enter a sparql endpoint url")
    client = Client(endpoint_url)
    print(dir(client))
