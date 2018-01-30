import re
from random import randint, choice
import pickle
from string import ascii_lowercase
from datetime import datetime
import networkx as x
# import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl

prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'


def randomNick():
    vowels = "aeiouy"
    consonants = "".join(i for i in ascii_lowercase if i not in vowels)
    nsyllables = randint(2, 5)
    nick = "".join(i for j in range(nsyllables) for i in
                   (choice(consonants), choice(vowels)))
    if randint(0, 1):
        nick = choice(vowels)+nick
    now = datetime.now()
    nick += str(now.hour)+str(now.minute)
    return nick


def uniqueItems(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def twitterReadPickle(filename):
    """pickle read for the Dumper class"""
    objs = []
    with open(filename, "rb") as f:
        while 1:
            try:
                objs.append(pickle.load(f))
            except EOFError:
                break
    return objs


def twitterReadPickleChunck(filename=None, tweets=[], fopen=None, ntweets=5000):
    """Read ntweets from filename or fopen and add them to tweets list"""
    if not fopen:
        f = open(filename, "rb")
    else:
        f = fopen
    # while len(tweets)<9900:
    while len(tweets) < ntweets:
        try:
            tweets += pickle.load(f)
        except EOFError:
            break
    return tweets, f
__rstring = "[{}]".format("".join(chr(i) for i in
                                  list(range(9))+list(range(11, 32))+[127]))
__reclean = re.compile(__rstring)


def cleanText(text):
    return __reclean.sub(r"", text)


def validateUrl(url_candidate):
    return bool(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                           r'(?:%[0-9a-fA-F][0-9a-fA-F]))+', url_candidate))


def toUndirected(xgraph):
    gg = x.Graph()
    gg.add_nodes_from(xgraph)
    gg.add_edges_from(xgraph.edges_iter(), weight=0)

    for u, v, d in xgraph.edges_iter(data=True):
            gg[u][v]['weight'] += d['weight']
    return gg


def makeNetworkFromSnapshotid(client, snapshotid):
    snapclass = snapshotid.split('#')[0].split('/')[-1]
    if snapclass == 'FacebookSnapshot':
        q = '''SELECT ?friend1 ?friend2 WHERE {{
            ?friendshipfoo po:snapshot <{}> .
            ?friendshipfoo a po:Friendship .
            ?friendshipfoo po:member ?friend1 .
            ?friendshipfoo po:member ?friend2 .
            }}
        '''.format(snapshotid, )
        relational_data = pl(client.retrieveQuery(prefix+q))
    elif snapclass == 'TwitterSnapshot':
        q = '''SELECT ?friend1 ?friend2 WHERE {{
            ?tweetfoo po:snapshot <{}> .
            ?tweetfoo a po:Tweet .
            ?tweetfoo po:author ?friend2 .
            ?tweetfoo po:retweetOf ?tweetfoo2 .
            ?tweetfoo2 po:author ?friend1 .
            }}
        '''.format(snapshotid, )
        relational_data = pl(client.retrieveQuery(prefix+q))
    else:
        raise ValueError('Only Facebook and Twitter snapshots implemented for now')
    return makeNetwork(relational_data)


def makeNetwork(relational_data, force_directed=False):
    if relational_data and len(relational_data[0]) == 3:
        gg = x.DiGraph()
        for val in relational_data:
            gg.add_edge(val[0], val[1], weight=int(val[2]))
        gg_ = toUndirected(gg)
        comp = x.weakly_connected_component_subgraphs(gg)[0]
        comp_ = x.connected_component_subgraphs(gg_)[0]
    elif relational_data and force_directed:
        edges = {}
        for val in relational_data:
            val_ = tuple(val)
            if val_ in edges:
                edges[val_] += 1
            else:
                edges[val_] = 1
        gg = x.DiGraph()
        for edge in edges:
            gg.add_edge(edge[0], edge[1], weight=edges[edge])
        gg_ = toUndirected(gg)
    elif relational_data:
        gg = x.Graph()
        for val in relational_data:
            gg.add_edge(val[0], val[1])
        # comp = x.connected_component_subgraphs(gg)[0]
        comp = max(x.connected_component_subgraphs(gg), key=len)
        gg_ = gg
        comp_ = comp
    return locals()


def pickSnapshot(client):
    prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
    snapshot = pl(client.retrieveQuery(prefix+'SELECT DISTINCT ?snap WHERE { ?s po:snapshot ?snap } LIMIT 1'))[0]
    return snapshot


def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)


def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject

def clearImport(packname):
    import sys
    keys=tuple(sys.modules.keys())
    for key in keys:
        if packname in key:
            del sys.modules[key]

class EmptyClass:
    pass
