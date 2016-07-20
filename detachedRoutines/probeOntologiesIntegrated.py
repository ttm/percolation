import percolation as P
# graphs
graphs = ('urn:twitter-legacy-ChennaiFloodsTweet00003.ttl', )
endpoint_url = 'http://localhost:8890/sparql'


for graph in graphs:
    fvars = P.rdf.probeOntology(endpoint_url, graph, 'testOntology')
