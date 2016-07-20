import os
import percolation as P
from percolation import c
from percolation.rdf.sparql.functions import plainQueryValues as pl
__doc__ = 'routine to probe ontology from rdf graph structures'


def probeOntology(endpoint_url, graph_urn, final_dir):
    if not os.path.isdir(final_dir):
        os.makedirs(final_dir)

    client = P.rdf.sparql.classes.LegacyClient(endpoint_url)
    from_ = '\nFROM <%s>\n' % (graph_urn,)

    def mkQuery(query, plain=True):
       query_ = query.split('WHERE')
       query__ = (query_[0], from_, 'WHERE '+query_[1])
       query___ = ''.join(query__)
       result = client.retrieveQuery(query___)
       if plain:
           return pl(result)
       else:
           return result

    c('find all classes')
    q = "SELECT DISTINCT ?o WHERE { ?s rdf:type ?o . }"
    # classes = pl(client.retrieveQuery(prefix+q))
    classes = mkQuery(q)
    classes_ = [i.split("/")[-1] for i in classes]

    c('find properties')
    q = "SELECT DISTINCT ?p WHERE {?s ?p ?o}"
    # properties = pl(client.retrieveQuery(prefix+q))
    properties = mkQuery(q)
    # properties_ = [i.split("/")[-1] for i in properties]

    c('antecedents and consequents of each class')
    neighbors = {}
    neighbors_ = {}
    for aclass in classes:
        q = "SELECT DISTINCT ?cs ?p WHERE { ?i a <%s> . ?s ?p ?i . OPTIONAL { ?s a ?cs . } }" % (aclass,)
        antecedent_property = mkQuery(q)
        q = "SELECT DISTINCT ?ap (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?ap ?o . filter (datatype(?o) != '') }" % (aclass,)
        consequent_property = mkQuery(q)
        q = "SELECT DISTINCT ?ap ?co WHERE { ?i a <%s> . ?i ?ap ?o . ?o a ?co . }" % (aclass,)
        consequent_property_ = mkQuery(q)
        neighbors[aclass] = (antecedent_property, consequent_property+consequent_property_)
        # neighbors[aclass] = (antecedent_property, dict(consequent_property, **consequent_property_))
        # class restrictions
    del q, aclass, antecedent_property, consequent_property
    triples = []
    for prop in properties:
        # check if property is functional
        q = 'SELECT DISTINCT (COUNT(?o) as ?co) WHERE { ?s <%s> ?o } GROUP BY ?s' % (prop,)
        is_functional = mkQuery(q)
        if len(is_functional) == 1 and is_functional[0]['value'] == 1:
            triples.append((prop, a, owl.FunctionalProperty))

        # datatype or object properties
        suj = mkQuery("SELECT DISTINCT ?cs WHERE { ?s <%s> ?o . ?s a ?cs . }" % (prop,))
        obj = mkQuery("SELECT DISTINCT ?co (datatype(?o) as ?do) WHERE { ?s <%s> ?o . OPTIONAL { ?o a ?co . } }" % (prop,))
        if len(cons) and ("XMLS" in obj[0]):
            triples.append((prop, a, owl.DataProperty))
        else:
            triples.append((prop, a, owl.ObjectProperty))
        if len(suj) > 1:
            B = r.BNode()
            triples.append((prop, rdfs.domain, B))
            for ss in suj:
                triples.append((B, owl.unionOf, ss))
        elif suj:
            triples.append((prop, rdfs.domain, suj[0]))
        if len(obj) > 1:
            B = r.BNode()
            triples.append((prop, rdfs.range, B))
            for ss in suj:
                triples.append((B, owl.unionOf, ss))
        elif obj:
            triples.append((prop, rdfs.range, obj[0]))

        # for drawing
        prop_ = prop.split("/")[-1]
        suj_ = [i.split('/')[-1] for i in suj]
        obj_ = [i.split('/')[-1] for i in obj]
    return locals()
