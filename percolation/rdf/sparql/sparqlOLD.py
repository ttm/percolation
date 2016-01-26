__doc__="useful sparql queries or routines"

import time, os
from IPython import embed
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
NS=P.rdf.NS
a=NS.rdf.type
class EndpointInterface:
    graphidAUX=NS.po.AuxGraph+"#1"
    def __init__(self,endpoint_url):
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint_url=endpoint_url
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)

    def addTranslatesFromSnapshots(self,snapshots=None):
        if snapshots==None:
            if not hasattr(self,"snapshots"):
                self.getMetaSnapshots()
            snapshots=self.snapshots
        # query each snapshot to get translates through ontology
        for snapshot in snapshots:
            self.addTranslatesFromSnapshot(snapshot)
    def addTranslatesFromSnapshot(self,snapshot):
        # busco localdir e translates (GROUP BY?)
        triple=snapshot,NS.po.defaultXML,"?translate"
        translates=plainQueryValues(self.performRetrieveQuery(triple))
        triple=snapshot,NS.po.localDir,"?localdir"
        localdir=plainQueryValues(self.performRetrieveQuery(triple))
        self.tmp=locals()
        # com os translates e o dir, carrego os translates
        translates="BANANA"
        for translate in translates:
            fname=translate.split("/")[-1]
            fname2="{}/{}".format(localdir,fname)
            graphid=self.addTranslationFileToEndpoint(fname2,snapshot)
            # add the relation of po:associatedTranslate to the "graphs" graph
    def addTranslationFileToEndpoint(self,tfile,snapshot):
        #http://purl.org/socialparticipation/po/AuxGraph#1
        cmd="s-post {} {} {}".format(self.endpoint_url, self.graphidAUX, tfile)
        ontology_triples=P.rdf.makeOntology()
        self.insertTriples(ontology_triples)
        # make updates on auxgraph
        messages=plainQueryValues(self.performRetrieveQuery("?message",a,NS.po.Message))
        participants=plainQueryValues(self.performRetrieveQuery("?participant",a,NS.po.Participant))
        triple="?foomsg",NS.gmane.author,"?participant"
        participants2=list(set(plainQueryValues(self.performRetrieveQuery(triple))))
        inds=messages+participants
        triples=[]
        for ind in inds:
            triples+=[(ind,NS.po.snapshot, snapshot)]

        insert=(
               (), 
                )
        where=(
               (), 
                )
        #WITH <http://example/addresses>
        #DELETE { ?person foaf:givenName 'Bill' }
        #INSERT { ?person foaf:givenName 'William' }
        #WHERE
        #  { ?person foaf:givenName 'Bill'
        #            } 
        # write fb friendships as classes with friends and snapshot
        # write other fb participant attributes as classes with a snapshot
        # associate fb interaction to snapshot

        # write tw participant attributes as classes with a snapshot

        # delete trash
        # DELETE { GRAPH IRIref { ?s ?p ?o } } WHERE { GRAPH IRIref { ?s ?p ?o } }

        # verify snaps to see if any other thing is associated to snaps
        # WITH <http://example/bookStore>

        triples=(
#                UPDATE=("?a",NS.po.referenceSnapshot,snapshot_uri)
#              WHERE=  ("?a", a ,NS.po.Participant),
                ("?m", a ,NS.po.Message),
                )
        # write all triples from auxgraph to defaultgraph
        # ADD/MOVE <self.graphidAux> TO DEFAULT 
    def addMetafileToEndpoint(self,tfile):
#        self.addFileToEndpoint(tfile)
        self.addFileToEndpoint(tfile)
        snapshoturi=[i for i in performFileGetQuery(tfile,(("?s",a,NS.po.Snapshot),))][0][0]
        snapshotsubclass=P.utils.identifyProvenance(tfile)
        triples=(
                    (snapshoturi,a,snapshotsubclass), # Gmane, FB, TW, ETC
                    (snapshoturi,NS.po.localDir,os.path.dirname(tfile)),
                    (snapshoturi,NS.po.metaFilepath,tfile),
                )
        self.insertTriples(triples)

    def addFileToEndpoint(self,tfile):
        cmd="s-post {} {} {}".format(self.endpoint_url, "default", tfile)
        os.system(cmd)
    def getAllTriples(self):
        qtriples=(("?s", "?p", "?o"),)
        self.triples=plainQueryValues(self.performRetrieveQuery(qtriples))
    def getSnapshots(self):
        qtriples=(
                ("?snapshot", a, NS.po.Snapshot),
#                ("?snapshot", a, NS.po.GmaneSnapshot),
#                ("?snapshot", a, NS.po.InteractionSnapshot),
                )
        self.snapshots=plainQueryValues(self.performRetrieveQuery(qtriples))
    def insertTriples(self,triples,graph=None):
        lines=""
        for triple in triples:
            line=formatQueryLine(triple)
            lines+=line
        if not graph:
            querystring = 'INSERT DATA {  %s  }'%(lines,)
        else:
            graphpart=" GRAPH <%s> { "%(graph,)
            querystring = 'INSERT DATA { %s %s } }'%(graphpart,lines,)
        self.result=self.postQuery(querystring)
    def performRetrieveQuery(self,querystring_or_triples,group_by=None):
        if isinstance(querystring_or_triples,(tuple,list)):
            if len(querystring_or_triples[0])!=3:
                querystring_or_triples=(querystring_or_triples,)
            tvars=[]
            body=""
            for line in querystring_or_triples:
                tvars+=[i for i in line if i[0]=="?" and "foo" not in i]
                body+=formatQueryLine(line)
            tvars=P.utils.uniqueItems(tvars)
            tvars_string=(" %s "*len(tvars))%tuple(tvars)
            querystring="SELECT "+tvars_string+" WHERE { "+body+" } "
        elif isinstance(querystring_or_triples,str):
            querystring=querystring_or_triples
        if group_by:
            querystring+="GROUP BY "+group_by
        self.query=querystring
        return self.retrieveQuery(querystring) 
    def retrieveQuery(self,querystring):
        return self.postQuery(querystring)
    def postQuery(self,querystring):
        self.endpoint.setQuery(querystring) 
        return self.endpoint.query().convert()
#        return self.endpoint.query()
    def renderDummyGraph(self,triples_dir="/disco/triplas/"):
        self.getAllTriples()
        P.utils.writeTriples(self.triples,"{}dummy.ttl".format(triples_dir))
        c("dummy ttl written")
    def insertOntology(self):
        self.insertTriples(P.rdf.makeOntology())

def addToFusekiEndpoint(end_url,tfiles):
    aa=[]
    for tfile in tfiles:
        time.sleep(.1)
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(end_url, tgraph, tfile)
        aa+=[os.system(cmd)]

def makeNetwork(endpoint_url,relation_uri,label_uri=None,rtype=1,directed=False):
    """Make network from data SparQL queried in endpoint_url.

    relation_uri hold the predicate uri to which individuals are the range or oboth range and domain.
    label_uri hold the predicate to which the range is the label (e.g. name or nick) of the individual.
    rtype indicate which type of structure to be queried, as exposed in:
    http://ttm.github.io/doc/semantic/report/2015/12/05/semantic-social-networks.html
    directed indicated weather the resulting network is a digraph or not."""
    sparql = SPARQLWrapper(endpoint_url)
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
def dictQueryValues(result_dict):
    keys=result_dict["head"]["vars"]
    results=[]
    for result in result_dict["results"]["bindings"]:
        this_result={}
        for key in keys:
            value=result[key]["value"]
            type_=result[key]["type"]
            if type_=="uri":
                value=r.URIRef(value)
            elif type_=="literal":
                pass
            else:
                raise TypeError("Type of incomming variable not understood")
            this_result[key]=[value]
        results+=[this_result]
    return results

def plainQueryValues(result_dict,join_queries=False):
    """Return query values as simplest list.
    
    Set join_queries="hard" to keep list of lists structure
    when each result hold only one variable"""

    keys=result_dict["head"]["vars"]
    results=[]
    for result in result_dict["results"]["bindings"]:
        this_result=[]
        for key in keys:
            value=result[key]["value"]
            type_=result[key]["type"]
            if type_=="uri":
                value=r.URIRef(value)
            elif type_ in ("literal","bnode"):
                pass
            elif type_=="typed-literal":
                if result[key]["datatype"]==(NS.xsd.integer).toPython():
                    value=int(value)
                elif result[key]["datatype"]==(NS.xsd.datetime).toPython():
                    pass
                elif result[key]["datatype"]==(NS.xsd.date).toPython():
                    pass
                elif result[key]["datatype"]==(NS.xsd.boolean).toPython():
                    if value=="true":
                        value=True
                    elif value=="false":
                        value=False
                    else:
                        raise TypeError("Incomming boolean not understood")
                else:
                    raise TypeError("Incomming typed-literal variable not understood")
            else:
                raise TypeError("Type of incomming variable not understood")
            this_result+=[value]
        results+=[this_result]
    if len(results) and len(keys)==1 and join_queries !="hard":
        results=[i[0] for i in results]
    return results
def performFileGetQuery(tfile,triples=(("?s",a,NS.po.Snapshot),)):
    g=r.Graph()
    g.parse(tfile)
    tvars=[]
    body=""
    for line in triples:
        tvars+=[i for i in line if i[0]=="?" and "foo" not in i]
        body+=formatQueryLine(line)
    tvars=P.utils.uniqueItems(tvars)
    tvars_string=(" %s "*len(tvars))%tuple(tvars)
    querystring="SELECT "+tvars_string+" WHERE { "+body+" } "
    return g.query(querystring)
def formatQueryLine(triple):
    line=""
    for term in triple:
        if isinstance(term,(r.Namespace,r.URIRef)):
            line+=" <%s> "%(term,)
        elif term[0]=="?":
            line+=" %s "%(term,)
        elif isinstance(term,str) and term[0]!="?":
             line+=' "%s" '%(term,)
        else:
            line+=' "%s" '%(term,)
    line+= " . "
    return line

