import percolation as P, os, time
from rdflib import ConjunctiveGraph
TT=time.time()

class PercolationServer:
    def __init__(self,percolationdir="~/.percolation/"):
        percolationdir=os.path.expanduser(percolationdir)
        if not os.path.isdir(percolationdir):
            os.mkdir(percolationdir)
        dbdir=percolationdir+"sleepydb/"
        if not os.path.isdir(dbdir):
            os.mkdir(dbdir)
        percolation_graph=ConjunctiveGraph(store="Sleepycat")
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
    P.utils.startSession()
#    P.utils.aaSession()
def close(): # duplicate in legacy/outlines.py
    P.percolation_graph.close()
def check(*args):
    global TT
    prompt=0
    if args[0]==1:
        prompt=1
        args=args[1:]
    if args and isinstance(args[0],str) and (len(args[0])==args[0].count("\n")):
        print("{}{:.3f}".format(args[0],time.time()-TT),*args[1:]); TT=time.time()
    else:
        print("{:.3f}".format(time.time()-TT),*args); TT=time.time()
    if prompt:
        input("ANY KEY TO CONTINUE")

