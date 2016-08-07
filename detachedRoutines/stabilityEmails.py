import percolation as P
client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
locals_ = P.legacy.outlines.articleStability.outlineTable(client)
statst = P.legacy.outlines.articleStability.circularTables(client)
statsa = P.legacy.outlines.articleStability.authorsTable(client)
statsp = P.legacy.outlines.articleStability.pcaTable(client)
