import os
from collections import OrderedDict
import percolation as P
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
snapshotid_stats_ = OrderedDict()
for snap in snapshotid_stats:
    if not snap.endswith('_fb'):
        continue
    snap_ = snap.split('#')[-1]
    snapshotid_stats_[snap_] = snapshotid_stats[snap]
for snap in snapshotid_stats:
    snap_ = snap.split('#')[-1]
    if not snap_.startswith('twitter-legacy'):
        continue
    snapshotid_stats_[snap_] = snapshotid_stats[snap]
for snap in snapshotid_stats:
    snap_ = snap.split('#')[-1]
    if not snap_.startswith('irc-legacy'):
        continue
    snapshotid_stats_[snap_] = snapshotid_stats[snap]
for snap in snapshotid_stats:
    snap_ = snap.split('#')[-1]
    if not snap_.startswith('legacy-gmane'):
        continue
    snapshotid_stats_[snap_] = snapshotid_stats[snap]

ADIR = '../../linkedOpenSocialData/tables/'
fname = ADIR+'basicOverall.tex'
P.mediaRendering.tables.fromDict(snapshotid_stats_, ('snapshot id', 'ntriples', 'nedges', 'nparticipants', 'nchars'), fname,
                                 'Number of triples (ntriples), number of relations/interactions/edges (nedges), number of participants (nparticipants) and number of characters (nchars) in each LOSD snapshot.',
                                 longtable=True)
# P.mediaRendering.tables.doubleLines(fname, [1], [1])
# P.mediaRendering.tables.fontSize(fname, write=True)
