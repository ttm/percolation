import percolation as P
import os
c = P.c

PDIR = "pickledir/"
fname = "{}basicOverall.pickle".format(PDIR)
if os.path.isfile(fname):
    snapshotid_stats = P.utils.pRead(fname)
else:
    client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
    c('antes')
    snapshotid_stats = P.legacy.outlines.articles.outline(client)
    c('depois')
    P.utils.pDump(snapshotid_stats, fname)
# table for ntriples, nparticipants, ninteractions, nchars
