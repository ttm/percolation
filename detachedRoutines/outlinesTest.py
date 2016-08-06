import os
import ast
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
                                 'Number of triples (ntriples), number of relations/interactions/edges (nedges), number of participants (nparticipants) and number of characters (nchars) in each snapshot.',
                                 longtable=True)
with open(ADIR+'misc/overallText.tex', 'w') as f:
    f.write(text)
fname = ADIR+'tables/nsnapshots.tex'
nsnapshots_ = OrderedDict()
stype_ = r.URIRef('http://purl.org/socialparticipation/po/Snapshot')
snap_types = [snap for snap in nsnapshots if snap != stype_]
snap_types.sort()
for stype in snap_types:
    nsnapshots_[stype[0]] = stype[1]
nsnapshots_['all'] = sum(nsnapshots_.values())
P.mediaRendering.tables.fromDict(nsnapshots_, ('social protocol',
    'number of snapshots'), fname, 'Number of snapshots from each provenance.')
P.mediaRendering.tables.doubleLines(fname, (1, -3), [])
# P.mediaRendering.tables.doubleLines(fname, [1], [1])
# P.mediaRendering.tables.fontSize(fname, write=True)

# make facebook table
# select group names and URLs
client = P.rdf.sparql.classes.LegacyClient('http://localhost:8890/sparql')
name_url = P.legacy.outlines.articles.facebookGroups(client)
name_url.sort()
nu = OrderedDict()
for nu_ in name_url:
    if nu_[1][0] == '[':
        # nu[nu_[0]] = nu_[1][1:-1].replace("'",'')
        avars = ast.literal_eval(nu_[1])
        text = ''
        for var in avars:
            text += ' \\url{'+var+'} ,'
        text = text[:-2]
        nu[nu_[0]] = text
    else:
        nu[nu_[0]] = '\\url{'+nu_[1]+'}'
# make table with them
fname = ADIR+'tables/facebookReferences.tex'
text = '''All the Facebook snapshots are either the result of individuals who downloaded
their data (and donated to the first author) or data downloaded from groups.
In the first case, it is senseless to present references. In the second
case, we present the group name and a link to a post in the group where
data and figures were delivered back to the group.'''
P.mediaRendering.tables.fromDict(nu, ('group name',
    'url(s)'), fname, text)
