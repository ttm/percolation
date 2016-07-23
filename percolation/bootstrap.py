import percolation as P
import rdflib as r
import os
import time
from rdflib import ConjunctiveGraph
TT = time.time()


class PercolationServer:
    def __init__(self, percolationdir="~/.percolation/"):
        percolationdir = os.path.expanduser(percolationdir)
        if not os.path.isdir(percolationdir):
            os.mkdir(percolationdir)
        dbdir = percolationdir+"sleepydb/"
        if not os.path.isdir(dbdir):
            os.mkdir(dbdir)
        percolation_graph = ConjunctiveGraph(store="Sleepycat")
        try:
            percolation_graph.open(dbdir, create=False)
        except:  # get exception type (?)
            percolation_graph.open(dbdir, create=True)
        P.percolation_graph = percolation_graph
        self.percolation_graph = percolation_graph
        P.percolation_server = self


endpoint_url_ = os.getenv("PERCOLATION_ENDPOINT")
P.client = None


def start(start_session=True, endpoint_url=endpoint_url_):
    """Startup routine"""
    c("endpoint url", endpoint_url)
    if endpoint_url:
        P.client = P.rdf.sparql.Client(endpoint_url)
    else:
        P.client = None
    PercolationServer()
    if start_session:
        P.utils.startSession()
#    P.utils.aaSession()


def close():  # duplicate in legacy/outlines.py
    P.percolation_graph.close()


def check(*args):
    global TT
    if not P.QUIET:
        if args and isinstance(args[0], str) \
                and (len(args[0]) == args[0].count("\n")):
            print("{}{:.3f}".format(args[0], time.time()-TT), *args[1:])
            TT = time.time()
        else:
            print("{:.3f}".format(time.time()-TT), *args)
            TT = time.time()
        if args[0] == "prompt":
            input("ANY KEY TO CONTINUE")
QUIET = False
c = check

if __name__ == "__main__":
    start()
    rdflibok = isinstance(P.percolation_graph, r.ConjunctiveGraph)
    ntriples = len(P.percolation_graph)
    c("rdflib in P.percolation_graph:", rdflibok, "ntriples:", ntriples)
    if endpoint_url_:
        ntriples = P.client.getNTriples()
        ngraphs = P.client.getNGraphs()
        c("connected to endpoint:", endpoint_url_, "with {} graphs \
          and {} triples".format(ngraphs, ntriples))
    else:
        c("not connected to any remote endpoint\n\
          (relying only on rdflib percolation_graph)")
    choice = input("print graphs (y/N)")
    if choice == "y":
        graphs = P.client.getAllGraphs()
        ntriples_ = []
        for graph in graphs:
            ntriples_ += [P.client.getNTriples(graph)]
        c(list(zip(ntriples_, graphs)))
    choice = input("print triples (y/N)")
    if choice == "y":
        c(P.client.getAllTriples())
