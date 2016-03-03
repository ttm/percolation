import os
import urllib
from percolation.rdf import NS, a, c
test = NS.test
from percolation.rdf.sparql.functions import buildQuery
from percolation.rdf.sparql.classes import Client


def testReadWriteDelete(endpoint_url):
    client = Client(endpoint_url)
    triples = [
              (NS.test.Something, a, NS.test.OtherThing),
              ]
    client.insertTriples(triples, "another")
    c("should print a triple: ", client.getAllTriples("another"))
    client.updateQuery("DROP GRAPH <another> ")
    c("should not print a triple: ", client.getAllTriples("another"))
    client.insertTriples(triples, "another")
    c("should print a triple: ", client.getAllTriples("another"))
    client.insertTriples(triples, "even_another")
    query = "SELECT ?g WHERE { GRAPH ?g {} }"
    c("should print all graphs : ", client.retrieveQuery(query))
    client.updateQuery("DROP GRAPH <another> ")
    client.updateQuery("DROP GRAPH <even_another> ")
    c("should have no more graphs : ", client.retrieveQuery(query))

    # add and remove triples
    triples_ = [
               (NS.test.SomethingElse, NS.test.pred, "banana"),
               ]
    client.insertTriples(triples+triples_, "another")
    c("should print two triples: ", client.getAllTriples("another"))
    query = r"DELETE DATA { GRAPH <another> { <%s> <%s> 'banana' . } } " % \
            (NS.test.SomethingElse, NS.test.pred)
    client.updateQuery(query)
    c("should print one triple: ", client.getAllTriples("another"))
    client.updateQuery("DROP GRAPH <another> ")
    query = "SELECT ?g WHERE { GRAPH ?g {} }"
    c("should have no more dummy graphs : ", client.retrieveQuery(query))


def testTextIO(endpoint_url):
    client = Client(endpoint_url)
    triples = [
        (test.Dummy, test.desc,  """áéíóúćçêôãõà"""),
        (test.Dummy, test.desc2, "Não concordo com a inclusão da palavra controle, sou a favor da manutenção do texto 'Política Nacional de Participação Social'.\n\nA inclusão desta palavra pode ser interpretada como o poder de controle de determinados atores. O uso de 'Política Nacional de Participação Social'atende mais ao intuito de promover um ambiente democrático e horizontal nas relações de participação civil."),
        (test.Dummy, test.desc3, "Não concordo com a inclusão da palavra controle, sou a favor da manutenção do texto 'Política Nacional de Participação Social'.\n\nA inclusão desta palavra pode ser interpretada como o poder de controle de determinados atores. O uso de 'Política Nacional de Participação Social'atende mais ao intuito de promover um ambiente democrático e horizontal nas relações de participação civil."),
        (test.Dummy, test.desc3, " \\o/".encode("utf8")),
        # (test.Dummy, test.desc, "t:w\
        # ex't\n\rte'st"çóṕxx%@#*%&%)(+_ ")
              ]
    client.insertTriples(triples, "text_graph")
    c("all graphs:", client.getAllGraphs())
    c("triples in text_graph:", client.getAllTriples("text_graph"))

def customConnection(endpoint_url):
    client = Client(endpoint_url+"/update")
    triples = [
        (test.Dummy, test.desc,  """áéíóúćçêôãõà"""),
        (test.Dummy, test.desc2, "Não concordo com a inclusão da palavra controle, sou a favor da manutenção do texto 'Política Nacional de Participação Social'.\n\nA inclusão desta palavra pode ser interpretada como o poder de controle de determinados atores. O uso de 'Política Nacional de Participação Social'atende mais ao intuito de promover um ambiente democrático e horizontal nas relações de participação civil.".replace("\\","\\\\")),
        (test.Dummy, test.desc3, " \\o/".replace("\\","\\\\")),
        (test.Dummy, test.desc3, ' Denominação "ASd"'.replace('"',"'")),
        (test.Dummy, test.desc3, ' Denominação "ASd"'),
              ]
    querystring = buildQuery(triples, method="insert")
    client.endpoint.method = "GET"
    client.endpoint.method = "POST"
    # client.endpoint.requestMethod = ""
    client.endpoint.requestMethod = "postdirectly"
    client.endpoint.requestMethod = "urlencoded"
    client.endpoint.setQuery(querystring)
    client.performQuery(querystring)


if __name__ == "__main__":
    endpoint_url = os.getenv("PERCOLATION_ENDPOINT")
    if not endpoint_url:
        endpoint_url = input("please enter a sparql endpoint url")
    c("==> endpoint url:", endpoint_url)
    c("+++ testing create and delete graphs/contexts and triples:")
    #triples = testReadWriteDelete(endpoint_url)
    c("--- testing IO of text:", endpoint_url)
    #triples = testTextIO(endpoint_url)
    c("### testing custom server:", endpoint_url)
    triples = customConnection(endpoint_url)
    c("end of (remote) sparql endpoint tests", triples)
