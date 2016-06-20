import pickle as pickle
import time
from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib as r
import pygraphviz as gv
import sys
from percolation import c
# import pylab as pl

# variaveis principais:
# classes (kk), props,
# neighbors_ (de classes)

# unir os nós de datatype iguais TTM

T = time.time()
U = r.URIRef


def fazQuery(query):
    NOW = time.time()
    # sparql = SPARQLWrapper("http://200.144.255.210:8082/cidadedemocratica/query")
    # sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
    sparql = SPARQLWrapper("http://localhost:3030/adbname/query")
    sparql.setQuery(PREFIX+query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(time.time()-NOW)
    return results["results"]["bindings"]
g = r.Graph()


def G(S, P, O):
    global g
    g.add((S, P, O))
owl = r.namespace.OWL
rdf = r.namespace.RDF
rdfs = r.namespace.RDFS
ocd = r.Namespace("http://purl.org/socialparticipation/ocd/")
xsd = r.namespace.XSD
notFunctionalProperties = ["tagged", "contact", "supporter"]
notFunctionalProperties_ = [ocd+i for i in notFunctionalProperties]
####
# Roteiro de métodos para construção da ontologia baseada nos dados
# data driven ontology

# 0) Triplifica conforme triplificaCD.py
# usa nomes mínimos para propriedades e classes como :body ou :name, classes como
# commentBody ou userName devem ser evitadas
# na triplificação. Podendo ser observadas e adicionadas
# no levantamento da ontologia.

# FEITO

# 0.5) Coloca dados triplificados num endpoint sparql para fazer as queries necessárias
# para o levantamento da ontologia.

# FEITO

# 1) Obtencao de todas as classes
# ?o where { ?s rdf:type ?o }
# com algumas excessoes (quais? TTM)
PREFIX = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ops: <http://purl.org/socialparticipation/ops#>
PREFIX opa: <http://purl.org/socialparticipation/opa#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcty: <http://purl.org/dc/dcmitype/>
PREFIX tsioc: <http://rdfs.org/sioc/types#>
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX schema: <http://schema.org/>
PREFIX aa: <http://purl.org/socialparticipation/aa/>
PREFIX ocd: <http://purl.org/socialparticipation/ocd/>"""

g.namespace_manager.bind("ops", "http://purl.org/socialparticipation/ops#")
g.namespace_manager.bind("rdf", r.namespace.RDF)
g.namespace_manager.bind("rdfs", r.namespace.RDFS)
g.namespace_manager.bind("foaf", r.namespace.FOAF)
g.namespace_manager.bind("xsd", r.namespace.XSD)
g.namespace_manager.bind("owl", r.namespace.OWL)
g.namespace_manager.bind("opa", "http://purl.org/socialparticipation/opa/")
g.namespace_manager.bind("ocd", "http://purl.org/socialparticipation/ocd/")
g.namespace_manager.bind("dc", "http://purl.org/dc/elements/1.1/")
g.namespace_manager.bind("dct", "http://purl.org/dc/terms/")
g.namespace_manager.bind("dcty", "http://purl.org/dc/dcmitype/")
g.namespace_manager.bind("gndo", "http://d-nb.info/standards/elementset/gnd#")
g.namespace_manager.bind("schema", "http://schema.org/")
g.namespace_manager.bind("sioc", "http://rdfs.org/sioc/ns#")


q = "SELECT DISTINCT ?class WHERE {?s a ?class}"
NOW = time.time()
# sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
sparql = SPARQLWrapper("http://localhost:3030/adbname/query")
sparql.setQuery(PREFIX+q)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("%.2f segundos para puxar todas as classes" %
      (time.time()-NOW,))
classes = [i["class"]["value"] for i in results["results"]["bindings"] if "w3.org" not in i["class"]["value"]]
trash = [i["class"]["value"] for i in results["results"]["bindings"] if "w3.org" in i["class"]["value"]]

# 2) Obtem todas as propriedades
# ?p where { ?s ?p ?o. }
# com algumas excessoes
q = "SELECT DISTINCT ?p WHERE {?s ?p ?o}"
NOW = time.time()
# sparql = SPARQLWrapper("http://200.144.255.210:8082/cd/query")
sparql = SPARQLWrapper("http://localhost:3030/adbname/query")
sparql.setQuery(PREFIX+q)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print("%.2f segundos para puxar todas as propriedades" %
      (time.time()-NOW,))
props = [i["p"]["value"] for i in results["results"]["bindings"] if "w3.org" not in i["p"]["value"]]
props_ = [i.split("/")[-1] for i in props]

# 3) Faz estrutura para cada classe e uma figura:
# classe no meio, dados à esquerda, classes à direita
# para cada classe, para cada individuo da classe,
# ver as relacoes estabelecidas com o individuo como
# sujeito e como objeto. Anotar a propriedade e o tipo de dado
# na ponta
# guarda a estrutura de relacionamento da classe.
neighbors = {}
neighbors_ = {}
for classe in classes:
    # res = fazQuery("SELECT DISTINCT ?p (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o }"%(classe,))
    NOW = time.time()
    print("\n%s antecedente,  consequente: " % (classe.split("/")[-1], ))
    ant = fazQuery("SELECT DISTINCT ?p ?cs WHERE { ?i a <%s> . ?s ?p ?i . ?s a ?cs . }" % (classe, ))
    ant_ = []
    for aa in ant:
        if "cs" in aa.keys():
            tobj = aa["cs"]["value"]
            ant_.append((tobj, aa["p"]["value"]))
    cons = fazQuery("SELECT DISTINCT ?p ?co (datatype(?o) as ?do) WHERE { ?i a <%s> . ?i ?p ?o . OPTIONAL { ?o a ?co . } }" % (classe, ))
    cons_ = []
    for cc in cons:
        if "co" in cc.keys():
            tobj = cc["co"]["value"]
            cons_.append((cc["p"]["value"], tobj))
        elif (("do" in cc.keys()) and ("w3.org" not in cc["p"]["value"])):
            tobj = cc["do"]["value"]
            cons_.append((cc["p"]["value"], tobj))
        elif (("do" in cc.keys()) and ("w3.org" in cc["p"]["value"])):
            c(cc["p"]["value"], tobj)  # to see what triple this is
            sys.exit()
    neighbors[classe] = (ant, cons)
    neighbors_[classe] = (ant_, cons_)
f = open("dumpVV.pickle", "wb")
vv = (neighbors, neighbors_)
pickle.dump(vv, f)
f.close()
fo = open("dumpVV.pickle", "rb")
vv_ = pickle.load(fo)
fo.close()
kk = vv_[1].keys()
for tkey in kk:  # for each class
    cl = tkey
    cl_ = cl.split("/")[-1]
    print(cl_)
    ex = vv_[1][cl]
    A = gv.AGraph(directed=True)
    # A.graph_attr["label"] = ("classe: %s,  no namespace interno: http://purl.org/socialparticipation/ocd/" % (cl_, ))
    A.graph_attr["label"] = ("class: %s" % (cl, ))
    for i in range(len(ex[0])):  # antecedents
        label = ex[0][i][0].split("/")[-1]  #  class
        elabel = ex[0][i][1].split("/")[-1]  # predicate
        print(label, elabel)
        A.add_node(label, style="filled")
        A.add_edge(label, cl_)
        e = A.get_edge(label, cl_)
        e.attr["label"] = elabel
        n = A.get_node(label)
        n.attr['color'] = "#A2F3D1"
    print("\n\n")
    for i in range(len(ex[1])):  # consequents
        label = ex[1][i][1].split("/")[-1]  # class or datatype
        elabel = ex[1][i][0].split("/")[-1]  # predicate
        print(elabel,  label)
        if "XMLS" in label:
            label_ = i
        else:
            label_ = label
        A.add_node(label_, style="filled")
        A.add_edge(cl_, label_)
        e = A.get_edge(cl_, label_)
        e.attr["label"] = elabel
        n = A.get_node(label_)
        n.attr['label'] = label
        if "XMLS" in label:
            n.attr['color'] = "#FFE4AA"
        else:
            n.attr['color'] = "#A2F3D1"
    n = A.get_node(cl_)
    n.attr['style'] = "filled"
    n.attr['color'] = "#6EAA91"
    nome = ("imgs/classes/%s.png" % (cl_, ))
    A.draw(nome, prog="dot")  # draw to png using circo
    print("Wrote %s" % (nome, ))

# 4) Faz estrutura geral e figura geral
A = gv.AGraph(directed=True)
A.graph_attr["label"] = "General diagram"
ii = 1
for tkey in kk:  # for each class
    cl_ = tkey.split("/")[-1]
    A.add_node(cl_, style="filled")
    n = A.get_node(cl_)
    n.attr['color'] = "#A2F3D1"
    ex = vv_[1][tkey]
    for i in range(len(ex[0])):  # for each antecedent
        label = ex[0][i][0].split("/")[-1]  # class
        elabel = ex[0][i][1].split("/")[-1]  # predicate
        print(elabel)
        if label not in A.nodes():
            A.add_node(label, style="filled")
            n = A.get_node(label)
            n.attr['color'] = "#A2F3D1"
        A.add_edge(label, cl_)
        e = A.get_edge(label, cl_)
        e.attr["label"] = elabel
    print("\n\n")
    for i in range(len(ex[1])):  # for each consequent
        label = ex[1][i][1].split("/")[-1]  # datatype of class
        elabel = ex[1][i][0].split("/")[-1]  # predicate
        print(elabel, label)
        if "XMLS" in label:  # if datatype
            label_ = ii
            ii += 1
            color = "#FFE4AA"
        else:
            label_ = label
            color = "#A2F3D1"
        if label_ not in A.nodes():
            A.add_node(label_, style="filled")
            n = A.get_node(label_)
            n.attr['label'] = label.split("#")[-1]
            n.attr['color'] = color
        A.add_edge(cl_, label_)
        e = A.get_edge(cl_, label_)
        e.attr["label"] = elabel
        e.attr["color"] = color
        e.attr["penwidth"] = 2
A.draw("imgs/OCD.png", prog="twopi", args="-Granksep=4")
A.draw("imgs/OCD2.png", prog="dot", args="-Granksep=.4 -Gsize='1000, 1000'")
print("Wrote geral")

# 4.5) qualificar literais
# ok.

# 5) Observando as triplas, observar hierarquias e conceitos especificos do namespace,
# como commentBody e userName. Ver README.md.
G(ocd.Problem, rdfs.subClassOf, ocd.Post)
G(ocd.Proposal, rdfs.subClassOf, ocd.Post)

G(ocd.supportCount, rdfs.subPropertyOf, ocd.counting)
G(ocd.inspirationCount, rdfs.subPropertyOf, ocd.counting)
G(ocd.commentCount, rdfs.subPropertyOf, ocd.counting)
G(ocd.followersCount, rdfs.subPropertyOf, ocd.counting)

# 6) As propriedades são qualificadas e as restrições de classe aplicadas.
# para cada propriedade, ver o que incide no domínio e no âmbito.
# Ao mesmo tempo, fazer os axiomas de classe

# Também pode ser pulada esta etapa para simplificar ontologia e evitar
# incompatibilidades com bancos de dados atualizados e maiores detalhes
# dados pelos especialistas.
# Abaixo estah o roteiro completo de observacao dos dados para extração das estruturas
# básicas, axiomas de propriedade, restrições de classe e visualizações.

# 6.1) estrutura básica e figuras:
P = {}
P_ = {}
for prop in props:
    # observar todos os subjeitos com q ela ocorre
    # observar todos os objetos com que ela ocorre
    # fazer estrutura, plotar cada uma
    prop_ = prop.split("/")[-1]
    suj = fazQuery("SELECT DISTINCT ?cs WHERE { ?s <%s> ?o . ?s a ?cs . }" % (prop,))
    obj = fazQuery("SELECT DISTINCT ?co (datatype(?o) as ?do) WHERE { ?s <%s> ?o . OPTIONAL { ?o a ?co . } }" % (prop,))
    P[prop_] = (suj, obj)
    A = gv.AGraph(directed=True)
    A.graph_attr["label"] = ("property: %s" % (prop,))
#    A.add_node(1,style = "filled")
#    A.add_node(2,style = "filled")
    A.add_edge(1, 2)
    e = A.get_edge(1, 2)
    e.attr["label"] = prop_
    n1 = A.get_node(1)
    n2 = A.get_node(2)
    n1.attr['style'] = "filled"
    n2.attr['style'] = "filled"
    n1.attr['color'] = "blue"
    n2.attr['color'] = "red"
    # Agiliza tags dos sujeitos
    ts = [i["cs"]["value"].split("/")[-1] for i in suj]
    # ls = string.join(ts,"<br />")
    ls = "<br />".join(ts)
    print("ls: "+ls)
    # n1.attr['label'] = ls
    n1.attr['label'] = ("<%s>" % (ls,))
    # Agiliza tags dos objetos
    if "mbox" in prop_:
        lo = "XMLSchema#anyURI"
        to = [lo]
    else:
        to1 = [i["co"]["value"].split("/")[-1] for i in obj if "co" in i.keys()]
        to2 = [i["do"]["value"].split("/")[-1] for i in obj if "do" in i.keys()]
        to = to1+to2
        # lo = string.join(to,"<br />")
        lo = "<br />".join(to)
    P_[prop_] = (ts, to)
    print("lo:"+lo)
    n2.attr['label'] = ("<%s>" % (lo,))
    nome = ("imgs/properties/%s.png" % (prop_,))
    A.draw(nome, prog="dot")  # draw to png using circo
    print("Wrote %s" % (nome,))

# variaveis props, classes, vv_, P_
f = open("dumpCheck.pickle", "wb")
tudo = (g, props, classes, vv_, P_)
pickle.dump(tudo, f)
f.close()

# CHECKPOINT
o = open("dumpCheck.pickle", "rb")
g, props, classes, vv_, P_ = pickle.load(o)
o.close()
# 6.2) qualificação das propriedades: range, domain e axioma de propriedade
# owl:ObjectProperty, owl:DatatypeProperty or owl:AnnotationProperty
# Aplicando automaticamente os critérios de
# range, domain, functional ou não
for prop in props:
    # check if functional with queries TTM
    if prop not in notFunctionalProperties_:
        G(U(prop), rdf.type, owl.functionalProperty)
    ant, cons = P_[prop.split("/")[-1]]
    if len(cons) and ("XMLS" in cons[0]):
        G(U(prop), rdf.type, owl.DatatypeProperty)
    else:
        G(U(prop), rdf.type, owl.ObjectProperty)
    if len(ant) > 1:
        B = r.BNode()
        G(U(prop), rdfs.domain, B)
        for ant_ in ant:
            G(B, owl.unionOf, U(ocd+ant_))
    elif ant:
        G(U(prop), rdfs.domain, U(ocd+ant[0]))

    if len(cons) > 1:
        B = r.BNode()
        G(U(prop), rdfs.range, B)
        for cons_ in cons:
            G(B, owl.unionOf, U(ocd+cons_))
    elif cons:
        if "XMLS" in cons[0]:
            G(U(prop), rdfs.range, U(xsd+cons[0]))
        else:
            G(U(prop), rdfs.range, U(ocd+cons[0]))
# restrições de classe
C = {}
Ci = {}
Ru = {}
Re = {}
for classe in classes:
    query = "SELECT DISTINCT ?p WHERE {?s a <%s>. ?s ?p ?o .}" % (classe,)
    props_c = fazQuery(query)
    props_c_ = [i["p"]["value"] for i in props_c if "22-rdf-syntax" not in i["p"]["value"]]
    C[classe] = props_c_
    query2 = "SELECT DISTINCT ?s WHERE {?s a <%s>}" % (classe,)
    inds = fazQuery(query2)
    inds_ = [i["s"]["value"] for i in inds]
    Ci[classe] = inds_
    for pc in props_c_:
        query3 = "SELECT DISTINCT ?s ?co  (datatype(?o) as ?do) WHERE {?s a <%s>. ?s <%s> ?o . OPTIONAL {?o a ?co . }}" % (classe, pc)
        inds2 = fazQuery(query3)
        inds2_ = set([i["s"]["value"] for i in inds2])
        objs = set([i["co"]["value"] for i in inds2 if "co" in i.keys()])
        vals = set([i["do"]["value"] for i in inds2 if "do" in i.keys()])
        print("%s --> %s , %s" % (classe, vals, objs))
        if len(inds_) == len(inds2_):
            print("%s, %s existencial" % (classe, pc))
            b_ = r.BNode()
            G(U(classe), rdfs.subClassOf, b_)
            G(b_, rdf.type, owl.Restriction)
            G(b_, owl.onProperty, U(pc))
            if len(vals):
                ob = list(vals)[0]
            else:
                try:
                    ob = list(objs)[0]
                except:
                    print(classe, pc)
                    ob = 0
            if ob:
                G(b_, owl.someValuesFrom, r.URIRef(ob))
                if classe in Re.keys():
                    Re[classe].append((pc, ob))
                else:
                    Re[classe] = [(pc, ob)]

        query4 = "SELECT DISTINCT ?s WHERE { ?s <%s> ?o .}" % (pc,)
        inds3 = fazQuery(query4)
        inds3_ = [i["s"]["value"] for i in inds3]
        if len(inds_) == len(inds3_):
            print("%s, %s universal" % (classe, pc))
            b_ = r.BNode()
            G(U(classe), rdfs.subClassOf, b_)
            G(b_, rdf.type, owl.Restriction)
            G(b_, owl.onProperty, U(pc))
            if len(vals):
                ob = list(vals)[0]
            else:
                try:
                    ob = list(objs)[0]
                except:
                    print(classe, pc)
                    ob = 0
            if ob:
                G(b_, owl.allValuesFrom, r.URIRef(ob))
                if classe in Ru.keys():
                    Ru[classe].append((pc, ob))
                else:
                    Ru[classe] = [(pc, ob)]
f = open("dumpREST.pickle", "wb")
tudo = (g, Re, Ru, C, Ci)
pickle.dump(tudo, f)
f.close()
# CHECKPOINT
fo = open("dumpREST.pickle", "rb")
g, Re, Ru, C, Ci = pickle.load(fo)
fo.close()

# 6.1) Enriquece figuras: classes, propriedades e geral
kk = vv_[1].keys()
for tkey in kk:
    cl = tkey
    cl_ = cl.split("/")[-1]
    print(cl_)
    ex = vv_[1][cl]
    A = gv.AGraph(directed=True)
    for i in range(len(ex[0])):  # antecedentes
        label = ex[0][i][0].split("/")[-1]
        elabel = ex[0][i][1].split("/")[-1]
        elabel_ = ex[0][i][1]
        print(label, elabel)
        A.add_node(label, style="filled")
        A.add_edge(label, cl_)
        e = A.get_edge(label, cl_)
        e.attr["label"] = elabel
        if elabel in notFunctionalProperties:
            e.attr["style"] = "dashed"
        if ex[0][i][0] in Re.keys():
            tr = Re[ex[0][i][0]]
            pp = [ii[0] for ii in tr]
            oo = [ii[1] for ii in tr]
            if (elabel_ in pp) and (oo[pp.index(elabel_)] == cl):
                e.attr["color"] = "#A0E0A0"
                print("EXISTENCIAL ANTECEDENTE")
        if ex[0][i][0] in Ru.keys():
            tr = Ru[ex[0][i][0]]
            pp = [ii[0] for ii in tr]
            oo = [ii[1] for ii in tr]
            if (elabel_ in pp) and (oo[pp.index(elabel_)] == cl):
                e.attr["arrowhead"] = "inv"
                print("EXISTENCIAL ANTECEDENTE")
        e.attr["penwidth"] = 2.
        e.attr["arrowsize"] = 2.
        n = A.get_node(label)
        n.attr['color'] = "#A2F3D1"
    print("\n\n")
    for i in range(len(ex[1])):  # consequentes
        label = ex[1][i][1].split("/")[-1]
        elabel = ex[1][i][0].split("/")[-1]
        elabel_ = ex[1][i][0]
        print(elabel, label)
        if "XMLS" in label:
            label_ = i
        else:
            label_ = label
        A.add_node(label_, style="filled")
        A.add_edge(cl_, label_)
        e = A.get_edge(cl_, label_)
        e.attr["label"] = elabel
        if elabel in notFunctionalProperties:
            e.attr["style"] = "dashed"
        if cl in Re.keys():
            tr = Re[cl]
            pp = [ii[0] for ii in tr]
            if elabel_ in pp:
                e.attr["color"] = "#A0E0A0"
                print("EXISTENCIAL")
        if cl in Ru.keys():
            tr = Ru[cl]
            pp = [ii[0] for ii in tr]
            if elabel_ in pp:
                e.attr["arrowhead"] = "inv"
                e.attr["arrowsize"] = 2.
                print("UNIVERSAL")
        e.attr["penwidth"] = 2.
        e.attr["arrowsize"] = 2.
        n = A.get_node(label_)
        n.attr['label'] = label
        if "XMLS" in label:
            n.attr['color'] = "#FFE4AA"
        else:
            n.attr['color'] = "#A2F3D1"
    n = A.get_node(cl_)
    n.attr['style'] = "filled"
    n.attr['color'] = "#6EAA91"
    A.graph_attr["label"] = (r"classe: %s, no namespace interno: http://purl.org/socialparticipation/ocd/.\nAresta tracejada: propriedade nao funcional.\nAresta verde: restricao existencial.\nPonta de seta invertida: restricao universal" % (cl_, ))
    nome = ("imgs/classes_/%s.png" % (cl_, ))
    A.draw(nome, prog="dot")  # draw to png using circo
    print("Wrote %s" % (nome, ))

# figura geral

A = gv.AGraph(directed=True)
A.graph_attr["label"] = r"Diagrama geral da OCD no namespace interno: http://purl.org/socialparticipation/ocd/\nAresta em verde indica restricao existencial,\ncom a ponta invertida indica restricao universal,\ntracejada indica propriedade nao funcional"
ii = 1
for tkey in kk:
    cl_ = tkey.split("/")[-1]
    cl = tkey
    if cl_ not in A.nodes():
        A.add_node(cl_, style="filled")
        n = A.get_node(cl_)
        n.attr['color'] = "#A2F3D1"
    ex = vv_[1][tkey]
    for i in range(len(ex[0])):
        label = ex[0][i][0].split("/")[-1]
        elabel = ex[0][i][1].split("/")[-1]
        print(elabel)
        if label not in A.nodes():
            A.add_node(label, style="filled")
            n = A.get_node(label)
            n.attr['color'] = "#A2F3D1"
        A.add_edge(label, cl_)
        e = A.get_edge(label, cl_)
        e.attr["label"] = elabel
        if elabel in notFunctionalProperties:
            e.attr["style"] = "dashed"
        if ex[0][i][0] in Re.keys():
            tr = Re[ex[0][i][0]]
            pp = [iii[0] for iii in tr]
            oo = [iii[1] for iii in tr]
            if (elabel_ in pp) and (oo[pp.index(elabel_)] == cl):
                e.attr["color"] = "#A0E0A0"
                print("EXISTENCIAL ANTECEDENTE")
        if ex[0][i][0] in Ru.keys():
            tr = Ru[ex[0][i][0]]
            pp = [iii[0] for iii in tr]
            oo = [iii[1] for iii in tr]
            if (elabel_ in pp) and (oo[pp.index(elabel_)] == cl):
                e.attr["arrowhead"] = "inv"
                print("EXISTENCIAL ANTECEDENTE")
        e.attr["penwidth"] = 2.
        e.attr["arrowsize"] = 2.

    print("\n\n")
    for i in range(len(ex[1])):  # consequentes
        label = ex[1][i][1].split("/")[-1]
        elabel = ex[1][i][0].split("/")[-1]
        elabel_ = ex[1][i][0]
        print(elabel, label)
        if "XMLS" in label:
            label_ = ii
            ii += 1
            color = "#FFE4AA"
        else:
            label_ = label
            color = "#A2F3D1"
        if label_ not in A.nodes():
            A.add_node(label_, style="filled")
            n = A.get_node(label_)
            n.attr['label'] = label.split("#")[-1]
            n.attr['color'] = color
        A.add_edge(cl_, label_)
        e = A.get_edge(cl_, label_)
        e.attr["label"] = elabel
        e.attr["color"] = color
        e.attr["penwidth"] = 2
        if elabel in notFunctionalProperties:
            e.attr["style"] = "dashed"
        if cl in Re.keys():
            tr = Re[cl]
            pp = [iii[0] for iii in tr]
            if elabel_ in pp:
                e.attr["color"] = "#A0E0A0"
                print("EXISTENCIAL")
        if cl in Ru.keys():
            tr = Ru[cl]
            pp = [iii[0] for iii in tr]
            if elabel_ in pp:
                e.attr["arrowhead"] = "inv"
                e.attr["arrowsize"] = 2.
                print("UNIVERSAL")

# A.draw("imgs/OCD_.png",prog = "twopi",args = "-Granksep = 14")
# A.draw("imgs/OCD_2.png",prog = "dot",args = "-Granksep = 14 -Gsize = '1000,1000'")
A.draw("imgs/OCD_.png", prog="dot")
A.draw("imgs/OCD_2.png", prog="circo")
A.draw("imgs/OCD_3.png", prog="fdp")
A.draw("imgs/OCD_4.png", prog="twopi")
print("Wrote geral _ ")

# figura com as propriedades
for prop in props:
    # observar todos os subjeitos com q ela ocorre
    # observar todos os objetos com que ela ocorre
    # fazer estrutura, plotar cada uma
    prop_ = prop.split("/")[-1]
    # suj = fazQuery("SELECT DISTINCT ?cs WHERE { ?s <%s> ?o . ?s a ?cs . }"%(prop,))
    # obj = fazQuery("SELECT DISTINCT ?co (datatype(?o) as ?do) WHERE { ?s <%s> ?o . OPTIONAL { ?o a ?co . } }"%(prop,))
    # P[prop_] = (suj,obj)
    suj, obj = P_[prop_]
    A = gv.AGraph(directed=True)
    A.graph_attr["label"] = (r"propriedade: %s, no namespace interno: http://purl.org/socialparticipation/ocd/\nAresta em verde indica restricao existencial,\ncom a ponta invertida indica restricao universal,\ntracejada indica propriedade nao funcional" % (prop_, ))
#    A.add_node(1,style = "filled")
#    A.add_node(2,style = "filled")
    A.add_edge(1, 2)
    e = A.get_edge(1, 2)
    e.attr["label"] = prop_
    if prop_ in notFunctionalProperties:
        # e.attr["style"] = "dotted"
        e.attr["style"] = "dashed"
    for cl in Re.keys():
        tr = Re[cl]
        pp = [iii[0] for iii in tr]
        if prop in pp:
            e.attr["color"] = "#A0E0A0"
            print("%s, EXISTENCIAL" % (prop_, ))

    for cl in Ru.keys():
        tr = Ru[cl]
        pp = [iii[0] for iii in tr]
        if prop in pp:
            e.attr["arrowhead"] = "inv"
            e.attr["arrowsize"] = 2.
            print("UNIVERSAL")

    e.attr["penwidth"] = 4

    n1 = A.get_node(1)
    n2 = A.get_node(2)
    n1.attr['style'] = "filled"
    n2.attr['style'] = "filled"
    n1.attr['color'] = "blue"
    n2.attr['color'] = "red"
    # Agiliza tags dos sujeitos
    # ts = [i["cs"]["value"].split("/")[-1] for i in suj]
    ts = suj
    ls = "<br />".join(ts)
    print("ls: "+ls)
    # n1.attr['label'] = ls
    n1.attr['label'] = ("<%s>" % (ls,))
    # Agiliza tags dos objetos
    if "mbox" in prop_:
        lo = "XMLSchema#anyURI"
        to = [lo]
    else:
        # to1 = [i["co"]["value"].split("/")[-1] for i in obj if "co" in i.keys()]
        # to2 = [i["do"]["value"].split("/")[-1] for i in obj if "do" in i.keys()]
        # to = to1+to2
        to = obj
        lo = "<br />".join(to)
    P_[prop_] = (ts, to)
    print("lo:"+lo)
    n2.attr['label'] = ("<%s>" % (lo,))
    nome = ("imgs/properties_/%s.png" % (prop_,))
    A.draw(nome, prog="dot")  # draw to png using circo
    print("Wrote %s" % (nome,))


# 7) O namespace é relacionado com namespaces externos através de: super classes e propriedades, e equivalentes classes e propriedades.
rdf = r.namespace.RDF
rdfs = r.namespace.RDFS
foaf = r.namespace.FOAF
owl = r.namespace.OWL
dc = r.namespace.DC
dct = r.namespace.DCTERMS
dcty = r.Namespace("http://purl.org/dc/dcmitype/")
gndo = r.Namespace("http://d-nb.info/standards/elementset/gnd#")
sc = r.Namespace("http://schema.org/")
ops = r.Namespace("http://purl.org/socialparticipation/ops#")
sioc = r.Namespace("http://rdfs.org/sioc/ns#")
xsd = r.namespace.XSD

g.namespace_manager.bind("ops", "http://purl.org/socialparticipation/ops#")
g.namespace_manager.bind("rdf", r.namespace.RDF)
g.namespace_manager.bind("rdfs", r.namespace.RDFS)
g.namespace_manager.bind("foaf", r.namespace.FOAF)
g.namespace_manager.bind("xsd", r.namespace.XSD)
g.namespace_manager.bind("owl", r.namespace.OWL)
g.namespace_manager.bind("opa", "http://purl.org/socialparticipation/opa/")
g.namespace_manager.bind("ocd", "http://purl.org/socialparticipation/ocd/")
g.namespace_manager.bind("dc", "http://purl.org/dc/elements/1.1/")
g.namespace_manager.bind("dct", "http://purl.org/dc/terms/")
g.namespace_manager.bind("dcty", "http://purl.org/dc/dcmitype/")
g.namespace_manager.bind("gndo", "http://d-nb.info/standards/elementset/gnd#")
g.namespace_manager.bind("schema", "http://schema.org/")
g.namespace_manager.bind("sioc", "http://rdfs.org/sioc/ns#")

# g.add((ocd.City,    rdfs.subClassOf, ))
# enriquece figuras

# 8) info sobre esta ontologia
ouri = ocd.ocd+".owl"
g.add((ouri, rdf.type, owl.Ontology))
g.add((ouri, dct.title, r.Literal(u"Ontologia do Cidade Democrática")))
g.add((ouri, owl.versionInfo, r.Literal(u"0.01au")))
g.add((ouri, dct.description, r.Literal(u"Ontologia do Cidade Democratica, levantada com base nos dados e para conectar com outras instâncias")))

# 8.1) Escreve OWL, TTL e PNG
f = open("OCD.owl", "wb")
f.write(g.serialize())
f.close()
f = open("OCD.ttl", "wb")
f.write(g.serialize(format="turtle"))
f.close()


# 9) Sobe no endpoint para mais testes

# Como foi feita para cada classe, também centrada na propriedade
# Fazer também para cada literal.
print("total time: ", time.time()-T)
