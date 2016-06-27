import percolation as P

client = P.rdf.sparql.classes.LegacyClient('http://127.0.0.1:3030/adbname')
# snapshotid, analysis = P.legacy.outlines.demo.analysis(client)
snapshotid, analysis = P.legacy.outlines.demo.textAnalysis(client)
