import os
import rdflib as r
import pygraphviz as gv
import percolation as P
from percolation import c
from .rdflib import NS, a
rdfs = NS.rdfs
owl = NS.owl
from percolation.rdf.sparql.functions import plainQueryValues as pl
__doc__ = 'routine to probe ontology from rdf graph structures'


def probeOntology(endpoint_url, graph_urns, final_dir, one_datatype=True):
    if not os.path.isdir(final_dir):
        os.makedirs(final_dir)

    client = P.rdf.sparql.classes.LegacyClient(endpoint_url)
    from_ = ''
    for graph_urn in graph_urns:
        from_ += '\nFROM <%s>' % (graph_urn,)

    def mkQuery(query, plain=True):
       query_ = query.split('WHERE')
       query__ = (query_[0], from_, '\nWHERE '+query_[1])
       query___ = ''.join(query__)
       result = client.retrieveQuery(query___)
       if plain:
           return pl(result)
       else:
           return result['results']['bindings']

    c('find all classes')
    q = "SELECT DISTINCT ?class WHERE { ?s a ?class . }"
    # classes = pl(client.retrieveQuery(prefix+q))
    classes = mkQuery(q)

    c('antecedents, consequents and restrictions of each class')
    neighbors = {}
    triples = []
    existential_restrictions = {}
    universal_restrictions = {}
    for aclass in classes:
        q = "SELECT DISTINCT ?cs ?p WHERE { ?i a <%s> . ?s ?p ?i . OPTIONAL { ?s a ?cs . } }" % (aclass,)
        antecedent_property = mkQuery(q)
        # q = "SELECT DISTINCT ?ap (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?ap ?o . filter (datatype(?o) != '') }" % (aclass,)
        # consequent_property = mkQuery(q)
        # q = "SELECT DISTINCT ?ap ?co WHERE { ?i a <%s> . ?i ?ap ?o . ?o a ?co . }" % (aclass,)
        # consequent_property_ = mkQuery(q)
        q = "SELECT DISTINCT ?ap ?co (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?ap ?o . OPTIONAL { ?o a ?co . } }" % (aclass,)
        consequent_property__ = mkQuery(q, 0)
        consequent_property = [[i['ap']['value'], i['do']['value']] for i in consequent_property__ if 'do' in i]
        consequent_property_ = [[i['ap']['value'], i['co']['value']] for i in consequent_property__ if 'co' in i]
        neighbors[aclass] = (antecedent_property, consequent_property+consequent_property_)
        # neighbors[aclass] = (antecedent_property, dict(consequent_property, **consequent_property_))

        # class restrictions
        q = "SELECT DISTINCT ?p WHERE {?s a <%s>. ?s ?p ?o .}" % (aclass,)
        props_c = mkQuery(q)
        # q = "SELECT DISTINCT ?s WHERE {?s a <%s>}" % (aclass,)
        # inds = mkQuery(q)
        q = "SELECT (COUNT(DISTINCT ?s) as ?cs) WHERE {?s a <%s>}" % (aclass,)
        ninds = pl(client.retrieveQuery(q))[0]
        for pc in props_c:
            if '22-rdf-syntax' in pc:
                continue
            # q = "SELECT DISTINCT ?s ?co  (datatype(?o) as ?do) WHERE {?s a <%s>. ?s <%s> ?o . OPTIONAL {?o a ?co . }}" % (aclass, pc)
            q = "SELECT DISTINCT ?co (datatype(?o) as ?do) WHERE {?s a <%s>. ?s <%s> ?o . OPTIONAL {?o a ?co . }}" % (aclass, pc)
            inds2 = mkQuery(q, 0)
            # inds2_ = set([i["s"]["value"] for i in inds2])
            objs = set([i["co"]["value"] for i in inds2 if "co" in i.keys()])
            vals = set([i["do"]["value"] for i in inds2 if "do" in i.keys()])
            q = "SELECT (COUNT(DISTINCT ?s) as ?cs) WHERE {?s a <%s>. ?s <%s> ?o . }" % (aclass, pc)
            ninds2 = pl(client.retrieveQuery(q))[0]
            # if len(inds) == len(inds2_):  # existential
            if ninds == ninds2:  # existential
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
                    if aclass in existential_restrictions.keys():
                        existential_restrictions[aclass].append((pc, ob))
                    else:
                        existential_restrictions[aclass] = [(pc, ob)]
            q = "SELECT (COUNT(DISTINCT ?s) as ?cs) WHERE { ?s <%s> ?o . ?s a ?ca . FILTER(str(?ca) != '%s') }" % (pc, aclass)
            ninds3 = pl(client.retrieveQuery(q))[0]
            # q = "SELECT DISTINCT ?s WHERE { ?s <%s> ?o .}" % (pc,)
            # inds3 = mkQuery(q)
            # if set(inds) == set(inds3):  # universal
            # if all([i in set(inds) for i in inds3]):  # universal
            # if ninds == ninds3:  # universal
            if ninds3 == 0:  # universal
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
                    if aclass in universal_restrictions.keys():
                        universal_restrictions[aclass].append((pc, ob))
                    else:
                        universal_restrictions[aclass] = [(pc, ob)]
    del q, aclass, antecedent_property, consequent_property
    c('find properties')
    q = "SELECT DISTINCT ?p WHERE {?s ?p ?o}"
    # properties = pl(client.retrieveQuery(prefix+q))
    properties = mkQuery(q)
    # properties_ = [i.split("/")[-1] for i in properties]

    c('check if property is functional and get range and domain')
    functional_properties = set()
    for prop in properties:
        # check if property is functional
        q = 'SELECT DISTINCT (COUNT(?o) as ?co) WHERE { ?s <%s> ?o } GROUP BY ?s' % (prop,)
        is_functional = mkQuery(q)
        if len(is_functional) == 1 and is_functional[0] == 1:
            triples.append((prop, a, owl.FunctionalProperty))
            functional_properties.add(prop)

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
    # Drawing
    c('started drawing')
    A = gv.AGraph(directed=True, strict=False)
    q = """PREFIX po: <http://purl.org/socialparticipation/po/>
    SELECT DISTINCT ?snap WHERE { { ?i po:snapshot ?snap } UNION { ?snap po:snapshotID ?idfoo } }"""
    # SELECT DISTINCT ?snap WHERE { ?i po:snapshot ?snap }"""
    snap = mkQuery(q)[0]
    q = """PREFIX po: <http://purl.org/socialparticipation/po/>
    SELECT ?provenance
    WHERE { <%s> po:socialProtocol ?provenance }""" % (snap)
    # WHERE { { <%s> po:socialProtocolTag ?provenance } UNION
    #         { <%s> po:humanizedName ?provenance } }""" % (snap, snap)
    provenance = pl(client.retrieveQuery(q))[0]
    # A.graph_attr["label"] = r"General diagram of ontological structure from %s in the http://purl.org/socialparticipation/participationontology/ namespace.\nGreen edge denotes existential restriction;\ninverted edge nip denotes universal restriction;\nfull edge (non-dashed) denotes functional property." % (provenance,)
    edge_counter = 1
    node_counter = 1
    data_nodes = {}
    for aclass in classes:
        aclass_ = aclass.split('/')[-1]
        if aclass_ not in A.nodes():
            A.add_node(aclass_, style="filled")
            n = A.get_node(aclass_)
            n.attr['color'] = "#A2F3D1"
        neigh = neighbors[aclass]
        # for i in range(len(neigh[0])):  # antecendents
        #     label = neigh[0][i][0].split("/")[-1]
        #     elabel = neigh[0][i][1]
        #     elabel_ = elabel.split("/")[-1]
        #     if label not in A.nodes():
        #         A.add_node(label, style="filled")
        #         n = A.get_node(label)
        #         n.attr['color'] = "#A2F3D1"
        #     ekey = '{}-{}-{}'.format(label, aclass_, edge_counter)
        #     edge_counter += 1
        #     A.add_edge(label, aclass_, ekey)
        #     e = A.get_edge(label, aclass_, key=ekey)
        #     e.attr["label"] = elabel_
        #     e.attr["penwidth"] = 2.
        #     e.attr["arrowsize"] = 2.
        #     if elabel not in functional_properties:
        #         e.attr["style"] = "dashed"
        #     if neigh[0][i][0] in existential_restrictions.keys():
        #         restriction = existential_restrictions[neigh[0][i][0]]
        #         prop = [iii[0] for iii in restriction]
        #         obj = [iii[1] for iii in restriction]
        #         if (elabel in prop) and (obj[prop.index(elabel)] == aclass):
        #             e.attr["color"] = "#A0E0A0"
        #     if neigh[0][i][0] in universal_restrictions.keys():
        #         restriction = universal_restrictions[neigh[0][i][0]]
        #         prop = [iii[0] for iii in restriction]
        #         obj = [iii[1] for iii in restriction]
        #         if (elabel in prop) and (obj[prop.index(elabel)] == aclass):
        #             e.attr["color"] = "inv"
        for i in range(len(neigh[1])):  # consequents
            label = neigh[1][i][1].split("/")[-1]
            elabel = neigh[1][i][0]
            elabel_ = elabel.split('/')[-1]
            if "XMLS" in label:
                color = "#FFE4AA"
                if one_datatype:
                    if label in data_nodes:
                        label_ = data_nodes[label]
                    else:
                        label_ = node_counter
                        node_counter += 1
                        data_nodes[label] = label_
                else:
                    label_ = node_counter
                    node_counter += 1
            else:
                label_ = label
                color = "#A2F3D1"
            if label_ not in A.nodes():
                A.add_node(label_, style="filled")
                n = A.get_node(label_)
                n.attr['label'] = label.split("#")[-1]
                n.attr['color'] = color
            ekey = '{}-{}-{}'.format(aclass_, label_, edge_counter)
            edge_counter += 1
            A.add_edge(aclass_, label_, ekey)
            e = A.get_edge(aclass_, label_, key=ekey)
            e.attr["label"] = elabel_
            e.attr["color"] = color
            e.attr["penwidth"] = 2
            if r.URIRef(elabel) not in functional_properties:
                e.attr["style"] = "dashed"
            if aclass in existential_restrictions.keys():
                restrictions = existential_restrictions[aclass]
                prop = [iii[0] for iii in restrictions]
                if r.URIRef(elabel) in prop:
                    e.attr["color"] = "#A0E0A0"
            if aclass in universal_restrictions.keys():
                restrictions = universal_restrictions[aclass]
                prop = [iii[0] for iii in restrictions]
                if r.URIRef(elabel) in prop:
                    e.attr["arrowhead"] = "inv"
                    e.attr["arrowsize"] = 2.

    # A.draw(os.path.join(final_dir, "{}.png".format(final_dir)), prog="dot")
    # try:
    #     A.draw(os.path.join(final_dir, "{}_circo.png".format(final_dir)), prog="circo")
    # except:
    #     pass
    # A.draw(os.path.join(final_dir, "{}_twopi.png".format(final_dir)), prog="twopi", args="-Granksep=4")
    # A.write(os.path.join(final_dir, "{}.dot".format(final_dir)))
    A.draw(os.path.join(final_dir, "draw.png"), prog="dot")
    try:
        A.draw(os.path.join(final_dir, "draw_circo.png"), prog="circo")
    except:
        pass
    A.draw(os.path.join(final_dir, "draw_twopi.png"), prog="twopi", args="-Granksep=4")
    A.write(os.path.join(final_dir, "draw.dot"))
    # for triple in triples:
    #     g.add(triple)
    P.start(False)
    P.context('ontology', 'remove')
    P.add(triples, 'ontology')
    g = P.context('ontology')
    g.serialize(os.path.join(final_dir, 'ontology.owl'))
    g.serialize(os.path.join(final_dir, 'ontology.ttl'), 'turtle')
    return locals()
