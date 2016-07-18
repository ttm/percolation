import os
from collections import OrderedDict
import rdflib as r
import percolation as P
c = P.c

PDIR = "pickledir/"
fname = "{}basicOverall.pickle".format(PDIR)
if os.path.isfile(fname):
    snapshotid_stats, text, nsnapshots = P.utils.pRead(fname)
else:
    client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
    c('antes snapshots')
    snapshotid_stats = P.legacy.outlines.articles.outline(client)
    c('depois snapshots')
    c('antes text')
    text = P.legacy.outlines.articles.outlineText(client)
    c('depois text')
    nsnapshots = P.legacy.outlines.articles.outlineNSnapshots(client)
    P.utils.pDump((snapshotid_stats, text, nsnapshots), fname)
# table for ntriples, nparticipants, ninteractions, nchars
snapshotid_stats_ = OrderedDict()
snaps = [snap for snap in snapshotid_stats]
snaps.sort()
for snap in snaps:
    snap_ = snap.split('#')[-1]
    snapshotid_stats_[snap_] = snapshotid_stats[snap]
ADIR = '../../linkedOpenSocialData/'
fname = ADIR+'tables/basicOverall.tex'
P.mediaRendering.tables.fromDict(snapshotid_stats_, ('snapshot id', 'ntriples', 'nedges', 'nparticipants', 'nchars'), fname,
                                 'Number of triples (ntriples), number of relations/interactions/edges (nedges), number of participants (nparticipants) and number of characters (nchars) in each LOSD snapshot.',
                                 longtable=True)
with open(ADIR+'misc/overallText.tex', 'w') as f:
    f.write(text)
fname = ADIR+'tables/nsnapshots.tex'
nsnapshots_ = OrderedDict()
stype_ = r.URIRef('http://purl.org/socialparticipation/po/Snapshot')
snap_types = [snap for snap in nsnapshots if snap != stype_]
snap_types.sort()
for stype in snap_types:
    nsnapshots_[stype] = nsnapshots[stype]
nsnapshots_[stype_] = nsnapshots[stype_]
P.mediaRendering.tables.fromDict(nsnapshots_, ('snapshot provenance', 'number of snapshots'), fname, 'Number of snapshots from each provenance. Every snapshot is a \\texttt{po:Snapshot}; there are three types of the \\texttt{po:AASnapshot} class.')
P.mediaRendering.tables.doubleLines(fname, (1, -3), [])
# P.mediaRendering.tables.doubleLines(fname, [1], [1])
# P.mediaRendering.tables.fontSize(fname, write=True)
