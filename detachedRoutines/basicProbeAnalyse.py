import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl
import networkx as x
c = P.c

# prefix po
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
client = P.rdf.sparql.classes.LegacyClient('http://127.0.0.1:3030/adbname')

snapshots = pl(client.retrieveQuery(prefix+'SELECT DISTINCT ?snap WHERE { ?s po:snapshot ?snap }'))

gg = []
for snapshot in snapshots:
    # retrieve friendships
    # make graph
    q = '''SELECT ?friend1 ?friend2 WHERE {{
            ?friendshipfoo po:snapshot <{}> .
            ?friendshipfoo a po:Friendship .
            ?friendshipfoo po:member ?friend1 .
            ?friendshipfoo po:member ?friend2 .
            }}
    '''.format(snapshot, )
    c('before query')
    friends = pl(client.retrieveQuery(prefix+q))
    c('after query')
    g = x.Graph()
    for friend1, friend2 in friends:
        g.add_edge(friend1, friend2)
    gg.append(g)

for g in gg:
    print(g.number_of_nodes(), g.number_of_edges())
    # topological analysis
    # direct measures ok
    # erdos sectors
    # scale free similarity
