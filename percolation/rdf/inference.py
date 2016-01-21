import percolation as P
from .rdflib import NS
a=NS.rdf.type
c=P.check

def rdfsInferencePerform(data_context=None,ontology_context=None,inffered_context=None,clean_inffered_context=True):
    # clean inference graph if True
    if clean_inffered_context:
        P.context(inffered_context,"remove")
    previous_count=len(P.context(inffered_context))
    rdfsInferenceIterate(data_context,ontology_context,inffered_context)
    # inference over inffered triples:
    new_count=len(P.context(inffered_context))
    while previous_count != new_count:
        previous_count=len(P.context(inffered_context))
        rdfsInferenceIterate(inffered_context,ontology_context,inffered_context)
        new_count=len(P.context(inffered_context))
    c("should have all triples resulting from a rdfs subclass subproperty range and domain assertions")
def rdfsInferenceIterate(data_context=None,ontology_context=None,inffered_context=None):
    contexts=[i.identifier.lower() for i in P.context()]
    if data_context not in contexts:
        c("no data context")
    if ontology_context not in contexts:
        c("no ontology context")
    if inffered_context not in contexts:
        c("inffered context to be created context:",inffered_context)
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.subClassOf,None),context=ontology_context):
        for individual, footype, foosubject in P.percolation_graph.triples(\
                (None,a,subject),context=data_context):
            P.add((individual,a,object_),context=inffered_context)
    c("finished subclass reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.subPropertyOf,None),context=ontology_context):
        c(subject,foo,object_)
        for subject2,propertyfoo,object2 in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
            c(subject2,propertyfoo,object2)
            P.add((subject2,object_,object2),context=inffered_context)
    c("finished subproperty reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.domain,None),context=ontology_context):
        for subject2,predicatefoo,objectfoo in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
            P.add((subject2,a,object_),context=inffered_context)
    c("finished domain reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.range,None),context=ontology_context):
        for subjectfoo,predicatefoo,object2 in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
                P.add((object2,a,object_),context=inffered_context)
    c("finished range reasoning")
