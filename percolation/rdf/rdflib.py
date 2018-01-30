from datetime import datetime
import inspect
import os
import rfc3986
import urllib
import rdflib as r
import percolation as P
c = P.check
U = r.URIRef


def info():
    uri_chars = """reserved     =  gen-delims / sub-delims
gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"
sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
            / "*" / "+" / "," / ";" / "="
unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~"
https://tools.ietf.org/html/rfc3986#section-2

NOTE: URI is not split with "%"
r.namespace.split_uri("http://purl.org/socialparticipation/irc/\
    Participant#labMacambiraLaleniaLog1%2818")"""
    return uri_chars


class NS:
    test =     r.Namespace("http://purl.org/socialparticipation/test/")   # caixa mágica
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
    social = r.Namespace("http://purl.org/socialparticipation/social/") # percolation, this framework itself
    participation = r.Namespace("http://purl.org/socialparticipation/participation/") # percolation, this framework itself
    facebook  =    r.Namespace("http://purl.org/socialparticipation/facebook/")  # facebook
    tw  =    r.Namespace("http://purl.org/socialparticipation/tw/")  # twitter
    irc =    r.Namespace("http://purl.org/socialparticipation/irc/") # irc
    gmane =  r.Namespace("http://purl.org/socialparticipation/gmane/") # gmane
    ld  =    r.Namespace("http://purl.org/socialparticipation/ld/")  # linkedin

    aavo  =    r.Namespace("http://purl.org/audiovisualanalytics/")
    aav  = r.Namespace("http://purl.org/audiovisualanalytics/vocabulary/")
    aao  =    r.Namespace("http://purl.org/audiovisualanalytics/ontology/")
    voeiia  =    r.Namespace("http://purl.org/audiovisualanalytics/voeiia/")

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
    skos =   r.namespace.SKOS
    U=   r.URIRef
a=NS.rdf.type
po=NS.po
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'

def timestampedURI(uriref=None,stringid="",datetime_=None):
    if not datetime:
        datetime_=datetime.now()
    sid=stringid+datetime_.isoformat()
    newuriref=uriref+"#"+sid
    return newuriref
def query(querystring,strict=False):
    """use get if using list of triples for data retrieval"""
    result= P.percolation_graph.query(querystring)
    triples=P.rdf.sparql.plainQueryValues(result)
    return triples

def get(subject=None, predicate=None, object_=None, context=None, percolation_graph=None, modifier1="", strict=False, minimized=False, join_queries=False):
    """Utility to get triples (or parts of them) by various criteria

    strict=False will reduce triples to a single triple if there is only one match.
    minimized=False witll return full triples, instead of only those that are not given for match.
    """
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    if isinstance(subject,(list,tuple)) and not predicate:
        query=P.rdf.sparql.buildQuery(subject,graph1=context,modifier1=modifier1)
        #c(query)
        if P.client:
            result=P.client.retrieveQuery(query)
        else:
            result=P.percolation_graph.query(query)
        triples=P.rdf.sparql.plainQueryValues(result,join_queries=join_queries)
    else:
        if subject:
            subject=r.URIRef(subject)
        contexts=[i.identifier for i in context_(percolation_graph=percolation_graph)]
        if context and not any((context in i) for i in contexts):
            raise ValueError("context "+context+" not existent, get will return empty")
        triples=[triple for triple in percolation_graph.triples((subject,predicate,object_),context)]
        if minimized==True:
            parts=[bool(i) for i in (subject,predicate,object_)]
            if sum(parts)==2:
                index=parts.index(False)
                item="i[{}]".format(index)
            else:
                item="("
                if not subject:
                    item+="i[0],"
                if not predicate:
                    item+="i[1],"
                if not object_:
                    item+="i[2]"
                item+=")"
            triples=[eval(item) for i in triples]
    if len(triples)==1 and strict==False: # only one triple
        triples=triples[0]
        if len(triples)==1: # if only one reference is being retrieved
            triples=triples[0]
    return triples


def remove(triples=None, context=None, percolation_graph=None):
    if not percolation_graph:
        percolation_graph = P.percolation_graph
    contexts = [i for i in context_(percolation_graph=percolation_graph)]
    if context and (context not in contexts):
        c("context", context, "not existent,  will not remove triple")
    else:
        if not triples:
            triples = [(None, None, None)]
        for triple in triples:
            percolation_graph.remove(triple, context=context)


def add(triples, context=None, percolation_graph=None):
    if isinstance(triples[0], (r.URIRef, r.Namespace)):
        triples = [triples]
    # triples = [i for i in triples if i[2]]
    if percolation_graph is None and P.client:
        c('==>>> add to sparql endpoint')
        P.client.insertTriples(triples, context)
        c('added')
        return
    elif percolation_graph is None:
        percolation_graph = P.percolation_graph
    quads = []
    for triple in triples:
        object_ = triple[2]
        subject = triple[0]
        if not isinstance(object_, (r.URIRef, r.Namespace)):
            object_ = r.Literal(object_)
        if not isinstance(subject, (r.URIRef, r.Namespace)):
            subject = r.URIRef(subject)
        quads += [(subject, triple[1], object_, context)]
    percolation_graph.addN(quads)


def context(context=None,command=None,percolation_graph=None):
    if P.client:
        if not context:
            return P.client.getAllGraphs()
        else:
            # get all triples from the graph
            return P.client.getAllTriples(context)
    if percolation_graph is None:
        percolation_graph=P.percolation_graph
    if not context:
        graphlist=[i for i in percolation_graph.contexts()]
#        c("no context in P.context(), return contexts list:",graphlist)
        return graphlist
    elif command==None:
        graph=percolation_graph.get_context(context)
#        c("return context graph named",context,"ntriples: ",len(graph))
        return graph
    elif command=="remove":
        percolation_graph.remove_context(context_(context))
#        c("tryed to removed context (not working): ", context,"return none")
context_=context


def set_(triples, context=None, percolation_graph=None):
    if not percolation_graph:
        percolation_graph = P.percolation_graph
    for triple in triples:
        object_ = triple[2]
        if not isinstance(object_, (r.URIRef, r.Namespace)):
            object_ = r.Literal(object_)
        quad_ = (triple[0], triple[1], None, context)
        percolation_graph.remove(quad_)
        quad = (triple[0], triple[1], object_, context)
        percolation_graph.add(quad)


def triplesScaffolding(subjects, predicates, objects, context=None):
    """Link subject(s) through predicate(s) to subject(s).

    Accepts any combination of one and N triples in inputs, eg:
      triplesScafolding(participants,NS.po.name,names) # N 1 N
      triplesScafolding(participants,name_props,name) # N N 1
      triplesScafolding(participant,name_pros,names) # 1 N N

      triplesScafolding(participant, names_props,name) # 1 N 1
      triplesScafolding(participant, NS.po.name,names) # 1 1 N
      triplesScafolding(participants,NS.po.name,name) # N 1 1

    Might be useful for rearanging lists into triples:
      triplesScafolding(participants,name_props,names) # N N N
      triplesScafolding(participant,NS.po.name,names) # 1 1 1"""
    if isinstance(subjects, str):
        subjects = r.URIRef(subjects)

    N = max([len(subjects), 0][isinstance(subjects, (r.URIRef, r.Namespace))],
            [len(predicates), 0][isinstance(predicates, (r.URIRef, r.Namespace))],
            [len(objects), 0][isinstance(objects, (r.URIRef, r.Namespace))])
    check = sum([((len(i) == N) or isinstance(i, (r.URIRef, r.Namespace)))
                 for i in (subjects, predicates, objects)]) == 3
    if not check:
        raise ValueError("input should be a combination of loose URIs and lists of same size ")
    triples = []
    if check == 3:
        for i, subject in enumerate(subjects):
            predicate = predicates[i]
            object_ = objects[i]
            triples += [(subject, predicate, object_)]
    else:
        if isinstance(subjects, (r.URIRef, r.Namespace)):
            subjects = [subjects]
        if isinstance(predicates, (r.URIRef, r.Namespace)):
            predicates = [predicates]
        if isinstance(objects, (r.URIRef, r.Namespace)):
            objects = [objects]
        if len(subjects) == 1:
            subjects *= N
        if len(predicates) == 1:
            predicates *= N
        if len(objects) == 1:
            objects *= N
        for subject, predicate, object_ in zip(subjects, predicates, objects):
            triples += [(subject, predicate, object_)]
    if context == "return_triples":
        return triples
    # c(outer_frame,dir(outer_frame),outer_frame.f_locals)
    # frames = inspect.getouterframes(inspect.currentframe())
    # outer_frame = frames[1][0]
    # if "triples" in outer_frame.f_locals:
    #     outer_frame.f_locals["triples"]+=triples
    # else:
    #     P.add(triples,context=context)
    P.add(triples, context=context)


def ic(uriref, string, context=None, snapshoturi=None):
    uri = uriref+"#"+urllib.parse.quote(string, safe="")
    assert rfc3986.is_valid_uri(uri)  # also rfc3986.normalize_uri
    triples = [
            (uri, a, uriref),
            ]
    if snapshoturi:
        triples += [
                 (uri, NS.po.snapshot, snapshoturi),
                 ]
    # frames = inspect.getouterframes(inspect.currentframe())
    # c(outer_frame,dir(outer_frame),outer_frame.f_locals)
    # outer_frame = frames[1][0]
    # if "triples" in outer_frame.f_locals:
    #     outer_frame.f_locals["triples"]+=triples
    # else:
    #     P.add(triples,context=context)
    P.add(triples,context=context)
    return uri

def writeByChunks(filename="path/name_without_extension",context=None,format_="both",ntriples=100000,triples=None, bind=[]):
    if not triples:
        triples=context_(context)
    g_=r.Graph()
    if bind:
        for item in bind:
            g_.namespace_manager.bind(item[0], item[1])
    triple_count=0
    chunk_count=0
    filenames_xml=[]
    sizes_xml=[]
    filenames_ttl=[]
    sizes_ttl=[]
    for triple in triples:
        object_=triple[2]
        subject=triple[0]
        if not isinstance(object_,(r.URIRef,r.Namespace)):
           object_=r.Literal(object_)
        if not isinstance(subject,(r.URIRef,r.Namespace)):
           subject=r.URIRef(subject)
        g_.add((subject,triple[1],object_))
        triple_count+=1
        if triple_count%ntriples==0:
            filename_="{}{:05d}".format(filename,chunk_count)
            filename_xml,filesize_xml,filename_ttl,filesize_ttl=write(filename_,graph=g_)
            filenames_xml+=[filename_xml]
            filenames_ttl+=[filename_ttl]
            sizes_xml+=[filesize_xml]
            sizes_ttl+=[filesize_ttl]
            g_=r.Graph()
            if bind:
                for item in bind:
                    g_.namespace_manager.bind(item[0], item[1])
            chunk_count+=1
    if len(g_):
        filename_="{}{:05d}".format(filename,chunk_count)
        filename_xml,filesize_xml,filename_ttl,filesize_ttl=write(filename_,graph=g_)
        filenames_xml+=[filename_xml]
        filenames_ttl+=[filename_ttl]
        sizes_xml+=[filesize_xml]
        sizes_ttl+=[filesize_ttl]
    return filenames_xml, sizes_xml, filenames_ttl, sizes_ttl
def write(filename="path/name_without_extension",context=None,format_="both",graph=None):
    if not graph:
        g=context_(context)
    else:
        g=graph
    c("starting serialization of",len(graph),"triples into",filename)
    filenames_sizes=[]
    if format_ in ("both","xml","rdf"):
        filename_=filename+".rdf"
        g.serialize(filename_,"xml"); c("xml", filename_)
        filenames_sizes+=[filename_.split("/")[-1]]
        filenames_sizes+=[os.path.getsize(filename_)/10**6]
    if format_ in ("both","turtle","ttl"):
        filename_=filename+".ttl"
        g.serialize(filename_,"turtle"); c("ttl", filename_)
        filenames_sizes+=[filename_.split("/")[-1]]
        filenames_sizes+=[os.path.getsize(filename_)/10**6]
    return filenames_sizes
