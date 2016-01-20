import percolation as P, rdflib as r, os

class PercolationServer:
    def __init__(self,percolationdir="~/.percolation/"):
        percolationdir=os.path.expanduser(percolationdir)
        if not os.path.isdir(percolationdir):
            os.mkdir(percolationdir)
        dbdir=percolationdir+"sleepydb/"
        if not os.path.isdir(dbdir):
            os.mkdir(dbdir)
        percolation_graph=r.ConjunctiveGraph(store="Sleepycat")
        try:
            percolation_graph.open(dbdir, create=False)
        except: # get exception type (?)
            percolation_graph.open(dbdir, create=True)
#        else:
#            assert percolation_graph == r.store.VALID_STORE, 'The underlying store is corrupt'
        # add percolationdir and dbdir to percolation_graph
        P.percolation_graph=percolation_graph
        self.percolation_graph=percolation_graph
        P.percolation_server=self

def start(): # duplicate in legacy/outlines.py
    PercolationServer()
#    P.utils.startSession()
#    P.utils.aaSession()
def close(): # duplicate in legacy/outlines.py
    P.percolation_graph.close()
