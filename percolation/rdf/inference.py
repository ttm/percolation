import percolation as P
from .rdflib import NS
a=NS.rdf.type
c=P.check


def performRdfsInference(data_context=None,ontology_context=None,inferred_context=None,clean_inferred_context=True):
    # clean inference graph if True
    if clean_inferred_context:
        P.context(inferred_context,"remove")
    previous_count=len(P.context(inferred_context))
    rdfsInferenceIterate(data_context,ontology_context,inferred_context)
    new_count=len(P.context(inferred_context))
    while previous_count != new_count:
        previous_count=len(P.context(inferred_context))
        rdfsInferenceIterate(inferred_context,ontology_context,inferred_context)
        new_count=len(P.context(inferred_context))
    c("should have all triples resulting from a rdfs subclass subproperty range and domain assertions")
def rdfsInferenceIterate(data_context=None,ontology_context=None,inferred_context=None):
    contexts=[i.identifier.lower() for i in P.context()]
    if data_context not in contexts:
        c("no data context")
    if ontology_context not in contexts:
        c("no ontology context")
    if inferred_context not in contexts:
        c("inferred context to be created context:",inferred_context)
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.subClassOf,None),context=ontology_context):
        for individual, footype, foosubject in P.percolation_graph.triples(\
                (None,a,subject),context=data_context):
            P.add((individual,a,object_),context=inferred_context)
        for foosubject, fooproperty, subject in P.percolation_graph.triples(\
                (None,None,subject),context=data_context):
            P.add((foosubject,fooproperty,object_),context=inferred_context)

    c("finished subclass reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.subPropertyOf,None),context=ontology_context):
        c(subject,foo,object_)
        for subject2,propertyfoo,object2 in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
            c(subject2,propertyfoo,object2)
            P.add((subject2,object_,object2),context=inferred_context)
    c("finished subproperty reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.domain,None),context=ontology_context):
        for subject2,predicatefoo,objectfoo in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
            P.add((subject2,a,object_),context=inferred_context)
    c("finished domain reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.range,None),context=ontology_context):
        for subjectfoo,predicatefoo,object2 in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
                P.add((object2,a,object_),context=inferred_context)
    c("finished range reasoning")
