import os
from percolation.rdf import NS, a, c
from percolation.rdf.sparql.classes import Client


def testReadWriteDelete(endpoint_url):
    client = Client(endpoint_url)
    triples = [
              (NS.test.Something, a, NS.test.OtherThing),
              ]
    client.insertTriples(triples,"another")
    c("should print a triple: ", client.getAllTriples("another"))
    client.updateQuery("DROP GRAPH <another> ")
    c("should not print a triple: ", client.getAllTriples("another"))
    client.insertTriples(triples,"another")
    c("should print a triple: ", client.getAllTriples("another"))
    client.insertTriples(triples,"even_another")
    query="SELECT ?g WHERE { GRAPH ?g {} }"
    c("should print all graphs : ", client.retrieveQuery(query))
    client.updateQuery("DROP GRAPH <another> ")
    client.updateQuery("DROP GRAPH <even_another> ")
    c("should have no more graphs : ", client.retrieveQuery(query))

    # add and remove triples
    triples_=[
             (NS.test.SomethingElse,NS.test.pred,"banana"),
             ]
    client.insertTriples(triples+triples_,"another")
    c("should print two triples: ", client.getAllTriples("another"))
    query = r"DELETE DATA { GRAPH <another> { <%s> <%s> 'banana' . } } " % \
             (NS.test.SomethingElse, NS.test.pred)
    client.updateQuery(query)
    c("should print one triple: ", client.getAllTriples("another"))
    client.updateQuery("DROP GRAPH <another> ")
    query="SELECT ?g WHERE { GRAPH ?g {} }"
    c("should have no more graphs : ", client.retrieveQuery(query))


if __name__ == "__main__":
    endpoint_url = os.getenv("PERCOLATION_ENDPOINT")
    if not endpoint_url:
        endpoint_url = input("please enter a sparql endpoint url")
    c("endpoint url:", endpoint_url)
    triples = testReadWriteDelete(endpoint_url)
    c("aqui", triples)
