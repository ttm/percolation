import os
import rdflib as r
import percolation as P
from percolation import c
from .rdflib import NS, a
rdfs = NS.rdfs
owl = NS.owl
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
           return result['results']['bindings']

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
    triples = []
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
        q = "SELECT DISTINCT ?p WHERE {?s a <%s>. ?s ?p ?o .}" % (aclass,)
        props_c = mkQuery(q)
        q = "SELECT DISTINCT ?s WHERE {?s a <%s>}" % (aclass,)
        inds = mkQuery(q)
        for pc in props_c:
            if '22-rdf-syntax' in pc:
                continue
            q = "SELECT DISTINCT ?s ?co  (datatype(?o) as ?do) WHERE {?s a <%s>. ?s <%s> ?o . OPTIONAL {?o a ?co . }}" % (aclass, pc)
            inds2 = mkQuery(q, 0)
            inds2_ = set([i["s"]["value"] for i in inds2])
            objs = set([i["co"]["value"] for i in inds2 if "co" in i.keys()])
            vals = set([i["do"]["value"] for i in inds2 if "do" in i.keys()])
            if len(inds) == len(inds2_):  # existential
                if len(vals):
                    ob = list(vals)[0]
                else:
                    if len(objs):
                        ob = list(objs)[0]
                    else:
                        ob = 0
                if ob:
                    B = r.BNode()
                    triples += [
                                (aclass, rdfs.subClassOf, B),
                                (B, a, owl.Restriction),
                                (B, owl.onProperty, pc),
                                (B, owl.someValuesFrom, ob)
                               ]
            query4 = "SELECT DISTINCT ?s WHERE { ?s <%s> ?o .}" % (pc,)
            inds3 = mkQuery(query4)
            if set(inds) == set(inds3):  # universal
                if len(vals):
                    ob = list(vals)[0]
                else:
                    if len(objs):
                        ob = list(objs)[0]
                    else:
                        ob = 0
                if ob:
                    B = r.BNode()
                    triples += [
                                (aclass, rdfs.subClassOf, B),
                                (B, a, owl.Restriction),
                                (B, owl.onProperty, pc),
                                (B, owl.allValuesFrom, ob)
                                ]
    del q, aclass, antecedent_property, consequent_property
    for prop in properties:
        # check if property is functional
        q = 'SELECT DISTINCT (COUNT(?o) as ?co) WHERE { ?s <%s> ?o } GROUP BY ?s' % (prop,)
        is_functional = mkQuery(q)
        if len(is_functional) == 1 and is_functional[0] == 1:
            triples.append((prop, a, owl.FunctionalProperty))

        # datatype or object properties
        suj = mkQuery("SELECT DISTINCT ?cs WHERE { ?s <%s> ?o . ?s a ?cs . }" % (prop,))
        # obj = mkQuery("SELECT DISTINCT ?co (datatype(?o) as ?do) WHERE { ?s <%s> ?o . OPTIONAL { ?o a ?co . } }" % (prop,))
        obj1 = mkQuery("SELECT DISTINCT ?co WHERE { ?s <%s> ?o . ?o a ?co . }" % (prop,))
        obj2 = mkQuery("SELECT DISTINCT (datatype(?o) as ?do) WHERE { ?s <%s> ?o . }" % (prop,))
        obj = obj1+obj2
        if len(obj) and ("XMLS" in obj[0]):
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
        # prop_ = prop.split("/")[-1]
        # suj_ = [i.split('/')[-1] for i in suj]
        # obj_ = [i.split('/')[-1] for i in obj]
    return locals()
