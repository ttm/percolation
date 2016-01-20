import percolation as P
from .rdflib import NS
a=NS.rdf.type
c=P.check

def rdfsInference(data_context=None,ontology_context=None,infered_context=None):
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.subClassOf,None),context=ontology_context):
        for individual, footype, foosubject in P.percolation_graph.triples(\
                (None,a,subject),context=data_context):
            P.percolation.add((individual,a,object_),context=infered_context)
    c("finished subclass reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.subPropertyOf,None),context=ontology_context):
        for subject2,propertyfoo,object2 in P.percolation_graph.triples(\
                (None,subject,None),context=data_context):
            P.percolation.add((subject2,object_,object2),context=infered_context)
    c("finished subproperty reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.domain,None),context=ontology_context):
        for subject2,predicatefoo,objectfoo in P.percolation_graph(\
                (None,subject,None),context=data_context):
                P.percolation.add((subject2,a,object_),context=infered_context)
    c("finished domain reasoning")
    for subject, foo, object_ in P.percolation_graph.triples(\
            (None,NS.rdfs.range,None),context=ontology_context):
        for subjectfoo,predicatefoo,object2 in P.percolation_graph(\
                (None,subject,None),context=data_context):
                P.percolation.add((object2,a,object_),context=infered_context)
    c("finished range reasoning")
