import os
import percolation as P
from percolation import c
from percolation.rdf.sparql.functions import plainQueryValues as pl
__doc__ = 'routine to probe ontology from rdf graph structures'


def probeOntology(endpoint_url, graph_urn, final_dir):
    if not os.path.isdir(final_dir):
        os.mkdir(final_dir)
    prefix = 'FROM <%s>\n' % (graph_urn,)
    client = P.rdf.sparql.classes.LegacyClient(endpoint_url)
    c('find all classes')
    q = "SELECT DISTINCT ?o WHERE { ?s rdf:type ?o . }"
    classes = pl(client.retrieveQuery(prefix+q))
    classes_ = [i.split("/")[-1] for i in classes]

    c('find properties')
    q = "SELECT DISTINCT ?p WHERE {?s ?p ?o}"
    properties = pl(client.retrieveQuery(prefix+q))
    properties_ = [i.split("/")[-1] for i in properties]

    c('antecedents and consequents of each class')
    neighbors = {}
    neighbors_ = {}
    for aclass in classes:
        q = "SELECT DISTINCT ?cs ?p WHERE { ?i a <%s> . ?s ?p ?i . OPTIONAL { ?s a ?cs . } }" % (aclass,)
        antecedent_property = client.retrieveQuery(prefix+q)
        q = "SELECT DISTINCT ?p ?co (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o . OPTIONAL { ?o a ?co . } }" % (aclass,)
        consequent_property = client.retrieveQuery(prefix+q)
        neighbors[aclass] = (antecedent_property, consequent_property)
    del q, aclass, antecedent_property, consequent_property
    return locals()
