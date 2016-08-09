import percolation as P
client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
locals_ = P.legacy.outlines.articleStability.outlineTable(client)
statst = P.legacy.outlines.articleStability.circularTables(client)
statsa = P.legacy.outlines.articleStability.authorsTable(client)
evolution = P.legacy.outlines.articleStability.networksEvolution(client)
statsp = P.legacy.outlines.articleStability.pcaTables(evolution)
# statst = P.legacy.outlines.articleStability.sectorsTimelines(evolution)
