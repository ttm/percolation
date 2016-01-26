__doc__="""

NOTES:
    See https://rdflib.readthedocs.org/en/4.2.1/_modules/rdflib/plugins/stores/sparqlstore.html
        where SparQLClient + SparQLQuery is called a "sparql store"

    INSERTs and DELETEs without a WHERE clause have the DATA keyword: INSERT DATA { ... } DELETE DATA { ... }.
    DELETE INSERT WHERE queries can't swap to INSERT DELETE WHERE. (The DELETE WHERE is in fact a D I W query without I) 
    
    Even so, I cant get this query to work: DELETE  {  GRAPH <http://purl.org/socialparticipation/po/AuxGraph#1> {  ?s  ?p  ?o  .  } }  INSERT  {      GRAPH <urn:x-arq:DefaultGraph> {  ?s  ?p  ?o  .  } }  WHERE   {  GRAPH <http://purl.org/socialparticipation/po/AuxGraph#1> {  ?s  <http://purl.org/socialparticipation/po/snapshot>  <http://purl.org/socialparticipation/po/Snapshot#GeorgeSanders08032014_fb>  .  } } '

    URI: tdb:unionDefaultGraph the union graph (don't seem to work now, maybe bugged)
    URI: urn:x-arq:DefaultGraph the default graph (seem to work)

    Legacy have had to split delete insert where query in 2: a insert where and delete where because of the bug above.

    a reference query that was dropped
        insert=(  
                ("?i1",NS.po.snapshot,snapshot),
                ("_:mblank",a,NS.po.ParticipantAttributes),
                ("_:mblank",NS.po.participant,"?i1"),
                ("_:mblank","?p","?o"),
                ("_:mblank",NS.po.snapshot,snapshot),
               )
        where=(
                ("?i1",a,NS.po.Participant),
                ("?i1","?p","?o"),
              )
        querystring=P.sparql.functions.buildQuery(triples1=insert,graph1=self.graphidAUX,
                                                  #triples2=where,graph2=self.graphidAUX,modifier2=" MINUS {?i1 a ?foovar} "
                                                  triples2=where,graph2=self.graphidAUX,modifier2=" FILTER(?p!=<%s>) "%(a,),
                                                  method="insert_where")
    in favor of a variation of:
        DELETE { ?s ?p ?o  }
        INSERT { ?s1 ?p ?o  }
        WHERE
        {
            { SELECT (uri(concat("http://another.domain.org/",
                                  SUBSTR(str(?s),24)) )
                      AS ?s1)
             {
               ?s ?p ?o .
               FILTER regex(str(?s), "^http://some.domain.org/")
             }}
        }


BACKUP

        delete=(
                 ("?s","?p","?o"),
                ("?s3","?p3","?s"),
               )
        insert=(
                 ("?s1","?p","?o"),
                 ("?s1",NS.po.genericURI,"?s"),
                 ("?s1",NS.po.snapshot,snapshot),
                 ("?s3","?p3","?s1"),
               )
        where=(
                ("?s",a,NS.po.Participant),
                ("?s","?p","?o"),
                ("OPTIONAL","?s3","?p3","?s"),
              )
        startB3_=" SELECT ?s ?p ?o ?s3 ?p3 (uri(concat(?s,'--','%s') ) AS ?s1) {"%(snapshot,)
        body3close_= " } } } "
        querystring=P.sparql.functions.buildQuery(
                                                  triples1=delete,graph1=self.graphidAUX,
                                                  triples2=insert,graph2=self.graphidAUX,
                                                  triples3=where, graph3=self.graphidAUX,
                                                           body3modifier=startB3_,body3close_=body3close_,
                                                  method="delete_insert_where")
"""

import os
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
from percolation.rdf import NS, a
c=P.check

default="urn:x-arq:DefaultGraph"
default=NS.po.MainGraph+"#1"
default="default"
g=r.Graph()
#g.addN(P.rdf.makeMetadata())

class SparQLClient:
    """Fuseki connection maintainer through rdflib"""
    def __init__(self,endpoint_url):
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint_url=endpoint_url
    def addLocalFileToEndpoint(self,tfile,tgraph=default):
        cmd="s-post {} {} {}".format(self.endpoint_url,tgraph,tfile)
        self.cmdline=cmd
        os.system(cmd)
    def removeLocalFileFromEndpoint(self,tfile,tgraph=default):
        cmd="s-delete {} {} {}".format(self.endpoint_url,tgraph,tfile)
        os.system(cmd)
    def restablishConnection(self,endpoint_url=None):
        if not endpoint_url:
            endpoint_url=self.endpoint_url
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint_url=endpoint_url
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)
class SparQLQueries:
    """Covenience class for inheritance with SparQLClient and SparQLLegacy"""
    iquery=[]
    rquery=[]
    def clearEndpoint(self,tgraph=default):
        if tgraph:
            query="CLEAR GRAPH <%s>"%(tgraph,)
        else:
            query="CLEAR DEFAULT"
        self.updateQuery(query)
    def addRemoteFileToEndpoint(self,remote_file_url,tgraph=default):
        part1="LOAD <%s> "%(remote_file_url)
        if tgraph:
            part2=" [ INTO <%s> ] "%(tgraph,)
        query=part1+part2
        self.updateQuery(query)
        raise NotImplementedError("Need to validate. Never been used")
    def insertTriples(self,triples,graph1=default):
        querystring=P.sparql.functions.buildQuery(triples,graph1=graph1,method="insert")
        self.iquery+=[querystring]
        self.result=self.updateQuery(querystring)
    def retrieveFromTriples(self,triples,graph1=default,modifier1="",startB_=None):
        querystring=P.sparql.functions.buildQuery(triples,graph1=graph1,modifier1=modifier1,startB_=startB_)
        self.rquery+=[querystring]
        return self.retrieveQuery(querystring)
    def retrieveQuery(self,querystring):
        """Query for retrieving information (e.g. through select)"""
        self.endpoint.method="GET"
        self.endpoint.setReturnFormat(JSON)
        return self.performQuery(querystring)
    def updateQuery(self,querystring):
        """Query to insert, delete and modify knowledge https://www.w3.org/Submission/SPARQL-Update/"""
        self.endpoint.method="POST"
        return self.performQuery(querystring)
    def performQuery(self,querystring):
        """Query method is defined at SparQLClient initialization."""
         # self.method=POST
        self.endpoint.setQuery(querystring) 
        return self.endpoint.queryAndConvert()
    def getAllTriples(self,graph1=default):
        qtriples=(("?s", "?p", "?o"),)
        self.triples=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(qtriples,graph1=graph1))
    def getNTriples(self,graph1=default):
        qtriples=(("?s", "?p", "?o"),)
        self.ntriples=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(qtriples,graph1=graph1,startB_=" (COUNT(*) as ?nt) WHERE { "))[0]
    def insertOntology(self,graph1=default):
        self.insertTriples(P.rdf.makeOntology(),graph1=graph1)
        # self.getNTriples(), P.utils.writeTriples(self.triples,"{}dummy.ttl".format(triples_dir))

class SparQLLegacyConvenience:
    """Convenience class for query and renderind analysis strictures, tables and figures"""
    graphidAUX=NS.po.AuxGraph+"#1"
    graphidAUX2=NS.po.AuxGraph+"#2"
    graphidAUX3=NS.po.AuxGraph+"#3"
    graphidAUX4=NS.po.AuxGraph+"#4"
    graphidAUX5=NS.po.AuxGraph+"#5"
    def __init__(self):
#        ontology_triples=P.rdf.makeOntology()
#        self.insertTriples(ontology_triples,self.graphidAUX) # SparQLQueries TTM
        self.getAllTriples(self.graphidAUX)
        self.ntriplesAUX=len(self.triples)
        self.triplesAUX=self.triples
    def getSnapshots(self,snaphot_type=None):
        if not snaphot_type:
            uri=NS.po.Snapshot
        else:
            uri=eval("NS.po.{}Snapshot".format(snaphot_type.title()))
            # NS.po.InteractionSnapshot, NS.po.GmaneSnapshot
        triples=(("?snapshot", a, uri),)
        self.snapshots=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(triples)) # SparQLQuery
    def addTranslatesFromSnapshots(self,snapshots=None):
        if snapshots==None:
            if not hasattr(self,"snapshots"):
                self.getSnapshots()
            snapshots=self.snapshots
        # query each snapshot to get translates through ontology
        for snapshot in snapshots:
            self.addTranslatesFromSnapshot(snapshot)
    def addTranslatesFromSnapshot(self,snapshot):
        # busco localdir e translates (GROUP BY?)
        triples=(snapshot,NS.po.defaultXML,"?translate"),
        translates=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(triples))
        triples=(snapshot,NS.po.localDir,"?localdir"),
        localdir=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(triples))[0]
        self.tmp=locals()
        # com os translates e o dir, carrego os translates
        c("into translates from snapshot")
#        P.utils.callDebugger()
        for translate in translates:
            fname=translate.split("/")[-1]
            fname2="{}/{}".format(localdir,fname)
            graphid=self.addTranslationFileToEndpoint(fname2,snapshot)
            # add the relation of po:associatedTranslate to the "graphs" graph
    def addTranslationFileToEndpoint(self,tfile,snapshot):
        #http://purl.org/socialparticipation/po/AuxGraph#1
        self.addLocalFileToEndpoint(tfile,self.graphidAUX)

        c("copy intermediary triples in AUX")
        self.getAllTriples(self.graphidAUX)
        self.triplesAUXINT0=self.triples
        self.ntriplesAUXINT0=len(self.triples)

        c("first substitute")
        delete=(
                 ("?s","?p","?o"),
                ("?s3","?p3","?s"),
               )
        insert=(
                 ("?s1","?p","?o"),
                 ("?s1",NS.po.genericURI,"?s"),
                 ("?s1",NS.po.snapshot,snapshot),
                 ("?s3","?p3","?s1"),
               )
        where=(
                ("?s",a,NS.po.Participant),
                ("?s","?p","?o"),
                ("OPTIONAL","?s3","?p3","?s"),
              )
#        startB3_=""" SELECT ?s ?p ?o ?s3 ?p3 (uri(concat(?s,'--','%s') ) AS ?s1) {"""%(snapshot,)
        bindline=" BIND(uri(concat(str(?s),'--','%s')) AS ?s1) "%(snapshot,)
        body3close_= " } "+bindline +" } "
        body3close_= bindline +" . } } "
        querystring=P.sparql.functions.buildQuery(
                                                  triples1=delete,graph1=self.graphidAUX,
                                                  triples2=insert,graph2=self.graphidAUX,
                                                  triples3=where, graph3=self.graphidAUX,
                                                           body3close_=body3close_,
                                                  method="delete_insert_where")
        #self.mquery2=querystring
        #self.updateQuery(querystring)

        c("second insert")
        insert=("?m",NS.po.snapshot,snapshot),
        where= ("?m",a,NS.po.InteractionInstance), # tw,gmane:message or fb interaction
        querystring=P.sparql.functions.buildQuery(triples1=insert,graph1=self.graphidAUX,
                                                  triples2=where,graph2=self.graphidAUX,method="insert_where")
        self.updateQuery(querystring)

        c("copy intermediary triples in AUX")
        self.getAllTriples(self.graphidAUX)
        self.triplesAUXINT=self.triples
        self.ntriplesAUXINT=len(self.triples)

        c("graph move")
        delete=("?s","?p","?o"), # aux
        insert=("?s","?p","?o"), # DEFAULT
        where=(
                ("?s",NS.po.snapshot,snapshot), # aux
                ("?s","?p","?o"), 
                )
        querystring=P.sparql.functions.buildQuery(
                                                  triples1=delete,graph1=self.graphidAUX,
                                                  triples2=insert,#graph2=default,#graph2="DEFAULT",
                                                  triples3=where,graph3=self.graphidAUX,
                                                  method="delete_insert_where")
        #self.updateQuery(querystring)
        self.mquery=querystring
        querystring=P.sparql.functions.buildQuery(
                                                  triples1=delete,graph1=self.graphidAUX,
                                                  triples2=where,graph2=self.graphidAUX,
                                                  method="delete_where")
        self.updateQuery(querystring)
        self.mqueryd=querystring




        c("delete trash (symmetric property and metafile for now)")
        delete=("?s","?p","?o"),
        where=(
                ("?s","?p",NS.owl.SymmetricProperty),
                ("?s","?p","?o"),
                )
        querystring=P.sparql.functions.buildQuery(triples1=delete,graph1=self.graphidAUX,
                                                  triples2=where,graph2=self.graphidAUX,
                                                  method="delete_where")
        delete=("?s","?p","?o"),
        where=(
                (snapshot,"?p","?o"),
                ("?s","?p","?o"),
                )
        querystring=P.sparql.functions.buildQuery(triples1=delete,graph1=self.graphidAUX,
                                                  triples2=where,graph2=self.graphidAUX,
                                                  method="delete_where")
        self.updateQuery(querystring)

        self.getNTriples(self.graphidAUX)
        if self.ntriples==self.ntriplesAUX:
            c("graphAUX restored correctly")
        else:
            c("somethig went wrong in restoring graphidAUX, keeping record")
            self.ntriplesAUX2=self.ntriples
            self.getAllTriples(self.graphidAUX)
            self.triplesAUX2=self.triples
        c("insert file path of translation to default graph and finish")
        triples=(snapshot,NS.po.translateFilePath,tfile),
        self.insertTriples(triples)
        # if empty afterwards, make dummy inference graph to copy triples from or load rdfs file
    def addMetafileToEndpoint(self,tfile):
        self.addLocalFileToEndpoint(tfile) # SparQLQueries
        snapshoturi=[i for i in P.sparql.functions.performFileGetQuery(tfile,(("?s",a,NS.po.Snapshot),))][0][0]
        snapshotsubclass=P.utils.identifyProvenance(tfile)
        triples=(
                    (snapshoturi,a,snapshotsubclass), # Gmane, FB, TW, ETC
                    (snapshoturi,NS.po.localDir,os.path.dirname(tfile)),
                    (snapshoturi,NS.po.metaFilePath,tfile),
                )
        self.insertTriples(triples) # SparQLQueries
    def makeNetwork(self,relation_uri,label_uri=None,rtype=1,directed=False):
        """Make network from data SparQL queried in endpoint_url.

        relation_uri hold the predicate uri to which individuals are the range or oboth range and domain.
        label_uri hold the predicate to which the range is the label (e.g. name or nick) of the individual.
        rtype indicate which type of structure to be queried, as exposed in:
        http://ttm.github.io/doc/semantic/report/2015/12/05/semantic-social-networks.html
        directed indicated weather the resulting network is a digraph or not."""
        sparql=self.endpoint
        if label_uri:
           mvars="i1","l1","i2","l2"
           label_qpart="""?i1  {} ?l1 .
                          ?i2  {} ?l2 .""".format(label_uri,label_uri)
        else: 
           mvars="i1","i2"
           label_qpart=""
        tvars=" ".join(["?{}" for i in mvars])
        if rtype==1: # direct relation 
            query="""SELECT  {}
                           WHERE {{ ?i1  {} ?i2 .
                                         {}      }}""".format(tvars,relation_uri,label_qpart)
        elif rtype==2: # mediated relation
            query="""SELECT  {} 
                           WHERE {{ ?foo  {} ?i1 .
                                    ?foo  {} ?i2 .
                                          {}      }}""".format(tvars,relation_uri,relation_uri,label_qpart)
        elif rtype==3: # twice mediated relation
            query="""SELECT  {} 
                           WHERE {{ ?foo  ?baz ?bar .
                                    ?foo   {} ?i1 .
                                    ?bar   {} ?i2 .
                                           {}      }}""".format(tvars,relation_uri,relation_uri,label_qpart)
        else:
            raise ValueError("rtype --> {} <-- not valid".format(rtype))
        c("query build ok")
        res=P.utils.mQuery(sparql,query,mvars)
        c("response received")
        if directed:
            dg=x.DiGraph()
        else:
            dg=x.Graph()
        for rel in res:
            id1,l1,id2,l2=rel
            if dg.has_node(id1): dg.node[id1]["weight"]+=1.
            else:       dg.add_node(id1,label=l1,weight=1.)

            if dg.has_node(id2): dg.node[id2]["weight"]+=1.
            else:       dg.add_node(id2,label=l2,weight=1.)

            if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
            else:       dg.add_edge(id1,id2,weight=2.)
        c("graph done")
        return dg

class Client(SparQLClient,SparQLQueries):
    """Class that holds sparql endpoint connection and convenienves for query"""
    def __init__(self,endpoint_url):
        SparQLClient.__init__(self,endpoint_url)
class LegacyClient(SparQLClient,SparQLQueries,SparQLLegacyConvenience):
    """Class that holds sparql endpoint connection and convenienves for query and renderind analysis strictures, tables and figures"""
    def __init__(self,endpoint_url):
        SparQLClient.__init__(self,endpoint_url)
        SparQLLegacyConvenience.__init__(self)

    
