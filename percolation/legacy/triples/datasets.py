# describe datasets:
# 1) snapshots
# 2) groups of snapshots
# 3) void: partitions of class and property
# 4) paths to files of published datasets

def datasets():
    localFiles() # .rdf .pickle .txt dumps void, full "/.percolation/data/*"
    onlineFiles() # from the void files of localFiles and write urls from online OLSD
    notes() # hand notes on the dataset
    loadVoid() # local if available, else online
    loadFull() # local if available, else online
    # for now, list some 3-4 dataset information.
    # load them in memory
    # this function should return the complete list of file addresses (local and remote)
    # with some description

def localFiles():
    P.utils.getFiles("./percolation/data/") # in ~/.percolation/data/

def onlineFiles():
    online_files=P.get((None,NS.po.onlineXML,None)),
    triples=[]
    for triple in online_files:
        triples+=[



