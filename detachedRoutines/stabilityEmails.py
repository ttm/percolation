import percolation as P
client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
data, q = P.legacy.outlines.articleStability.outlineTable(client)
