import re
from random import randint, choice
import pickle
from string import ascii_lowercase
from datetime import datetime
import networkx as x


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
    gg.add_edges_from(xgraph.edges_iter(), weight=0)

    for u, v, d in xgraph.edges_iter(data=True):
            gg[u][v]['weight'] += d['weight']
    return gg


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
        comp = x.connected_component_subgraphs(gg)[0]
        gg_ = gg
        comp_ = comp
    return locals()
