import percolation as P
client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
locals_ = P.legacy.outlines.articleStability.outlineTable(client)
stats = P.legacy.outlines.articleStability.circularTables(client)
stats = P.legacy.outlines.articleStability.authorsTable(client)
