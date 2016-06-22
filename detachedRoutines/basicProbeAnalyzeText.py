import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl
import networkx as x
c = P.c

# prefix po
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
client = P.rdf.sparql.classes.LegacyClient('http://127.0.0.1:3030/adbname')

snapshots = pl(client.retrieveQuery(prefix+'SELECT DISTINCT ?snap WHERE { ?s po:snapshot ?snap }'))
snapshots = [snap for snap in snapshots if 'Twitter' in snap]

gg = []
for snapshot in snapshots:
    # retrieve friendships
    # make graph
    q = '''SELECT ?friend1 ?friend2 WHERE {{
            ?tweetfoo po:snapshot <{}> .
            ?tweetfoo a po:Tweet .
            ?tweetfoo po:author ?friend2 .
            ?tweetfoo po:retweetOf ?tweetfoo2 .
            ?tweetfoo2 po:author ?friend1 .
            }}
    '''.format(snapshot, )
    c('before query')
    friends = pl(client.retrieveQuery(prefix+q))
    c('after query')
    # g = x.DiGraph()
    # for friend1, friend2 in friends:
    #     g.add_edge(friend1, friend2)
    g = P.utils.makeNetwork(friends, True)
    gg.append(g)
    print(g['gg'].number_of_nodes(), g['gg'].number_of_edges(), snapshot)

for g in gg:
    print(g['gg'].number_of_nodes(), g['gg'].number_of_edges())
    g_ = max(x.connected_component_subgraphs(g['gg_']), key=len)
    print(g_.number_of_nodes(), g_.number_of_edges())
    # order nodes by degree
    # choose one with degree ~2
    # get all messages separately
    # get all messages with group by and concat
    degrees = g_.degree()
    for node in g_.nodes():
        # todo texto de cada autor
        q = '''SELECT (GROUP_CONCAT(?text) as ?ctext) WHERE {{
                ?tweet po:author <{}> .
                ?tweet po:message ?text .
            }}
            '''.format(node)
        text = pl(client.retrieveQuery(prefix+q))
        g_[node]['text'] = text[0]
        # q = '''SELECT ?text ?author WHERE {{
        #     ?tweetfoo po:author ?author .
        #     ?tweetfoo po:message ?text .
        # }} GROUP BY ?author
        # '''
        # get body
        # put into g_
    # get text of each and put into a variable in the graph nodes
    # analyze the text
    # make joint analyses of text and topology

