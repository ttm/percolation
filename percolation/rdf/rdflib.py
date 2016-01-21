from datetime import datetime
import rdflib as r, percolation as P
c=P.check
def info():
   uri_chars="""reserved    = gen-delims / sub-delims
gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"
sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
            / "*" / "+" / "," / ";" / "="
unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~"
https://tools.ietf.org/html/rfc3986#section-2

NOTE: URI is not split with "%"
r.namespace.split_uri("http://purl.org/socialparticipation/irc/Participant#labMacambiraLaleniaLog1%2818")"""

class NS:
    cm =     r.Namespace("http://purl.org/socialparticipation/cm/")   # caixa mágica
    obs =    r.Namespace("http://purl.org/socialparticipation/obs/") # ontology of the social library
    aa  =    r.Namespace("http://purl.org/socialparticipation/aa/")  # algorithmic autoregulation
    vbs =    r.Namespace("http://purl.org/socialparticipation/vbs/") # vocabulary of the social library
    opa =    r.Namespace("http://purl.org/socialparticipation/opa/") # participabr
    ops =    r.Namespace("http://purl.org/socialparticipation/ops/") # social participation ontology
    ocd =    r.Namespace("http://purl.org/socialparticipation/ocd/") # cidade democrática
    ore =    r.Namespace("http://purl.org/socialparticipation/ore/") # ontology of the reseach, for registering ongoing works, a RDF AA
    ot  =    r.Namespace("http://purl.org/socialparticipation/ot/")  # ontology of the thesis, for academic conceptualizations
    po = r.Namespace("http://purl.org/socialparticipation/po/") # the participation ontology, this framework itself
    per = r.Namespace("http://purl.org/socialparticipation/per/") # percolation, this framework itself
    fb  =    r.Namespace("http://purl.org/socialparticipation/fb/")  # facebook
    tw  =    r.Namespace("http://purl.org/socialparticipation/tw/")  # twitter
    irc =    r.Namespace("http://purl.org/socialparticipation/irc/") # irc
    gmane =  r.Namespace("http://purl.org/socialparticipation/gmane/") # gmane
    ld  =    r.Namespace("http://purl.org/socialparticipation/ld/")  # linkedin 
    dbp  =    r.Namespace("http://dbpedia.org/resource/")
    rdf =    r.namespace.RDF
    rdfs =   r.namespace.RDFS
    owl =    r.namespace.OWL
    xsd =    r.namespace.XSD
    dc =     r.namespace.DC
    dct =    r.namespace.DCTERMS
    foaf =   r.namespace.FOAF
    doap =   r.namespace.DOAP
    void =   r.namespace.VOID
    U=   r.URIRef
a=NS.rdf.type
 
def timestampedURI(uriref=None,stringid="",datetime_=None):
    if not datetime:
        datetime_=datetime.now()
    sid=stringid+datetime_.isoformat()
    newuriref=uriref+"#"+sid
    return newuriref
def get(subject=None,predicate=None,object_=None,context=None,percolation_graph=None):
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    contexts=[i for i in context_(percolation_graph=percolation_graph)]
    if context and (context not in contexts):
        c("context",context,"not existent, get will return empty")
    triples=[triple for triple in percolation_graph.triples((subject,predicate,object_),context)]
    if len(triples)==1: # only one triple
        triples=triples[0]
    return triples

def remove(triples=None,context=None,percolation_graph=None):
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    contexts=[i for i in context_(percolation_graph=percolation_graph)]
    if context and (context not in contexts):
        c("context",context,"not existent, will not remove triple")
    else:
        if not triples:
            triples=[(None,None,None)]
        for triple in triples:
            percolation_graph.remove(triple,context=context)

def add(triples,context=None,percolation_graph=None):
    if isinstance(triples[0],(r.URIRef,r.Namespace)):
        triples=[triples]
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    quads=[]
    for triple in triples:
        object_=triple[2]
        if not isinstance(object_,(r.URIRef,r.Namespace)):
           object_=r.Literal(object_)
        quads+=[(triple[0],triple[1],object_,context)]
    percolation_graph.addN(quads)
def context(context=None,command=None,percolation_graph=None):
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    if not context:
        graphlist=[i for i in percolation_graph.contexts()]
        c("no context in P.context(), return contexts list:",graphlist)
        return graphlist
    elif command==None:
        graph=percolation_graph.get_context(context)
        c("return context graph named",context,"ntriples: ",len(graph))
        return graph
    elif command=="remove":
        percolation_graph.remove_context(context_(context))
        c("tryed to removed context (not working): ", context,"return none")
context_=context
    
def set_(triples,context=None,percolation_graph=None):
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    for triple in triples:
        object_=triple[2]
        if not isinstance(object_,(r.URIRef,r.Namespace)):
           object_=r.Literal(object_)
        quad_=(triple[0],triple[1],None,context)
        percolation_graph.remove(quad_)
        quad=(triple[0],triple[1],object_,context)
        percolation_graph.add(quad)
