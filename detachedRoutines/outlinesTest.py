import percolation as P
c = P.c

# client = P.rdf.sparql.classes.LegacyClient('http://127.0.0.1:3030/adbname')
client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
# snapshotid, analysis = P.legacy.outlines.demo.analysis(client)
c('antes')
snapshotid_stats = P.legacy.outlines.articles.outline(client)
c('depois')
# snapshotid, analysis = P.legacy.outlines.demo.textAnalysis(client)
