# describe datasets:
# 1) snapshots
# 2) groups of snapshots
# 3) void: partitions of class and property
# 4) paths to files of published datasets
import percolation as P
NS=P.rdf.NS
a=NS.rdf.type

def datasets():
    localFiles() # .rdf .pickle .txt dumps void, full "/.percolation/data/*"
    onlineFiles() # from the void files of localFiles and write urls from online OLSD
    notes() # hand notes on the dataset
    void() # local if available, else online
    full() # local if available, else online
    # for now, list some 3-4 dataset information.
    # load them in memory
    # this function should return the complete list of file addresses (local and remote)
    # with some description
def notes():
    pass
def minimalTestData():
    triples=[
            (NS.po.SnapshotFoo+"#1", NS.facebook.ego, True),
            (NS.po.SnapshotFoo+"#1", NS.facebook.userID, "1039203918"),
            (NS.po.SnapshotFoo+"#1", NS.facebook.user, NS.facebook.Participant+"Foop"),
            ]
    P.add(triples,context="void")
def void():
    triples=[
            (NS.po.SnapshotFoo+"#1", a, NS.po.FacebookSnapshot),
            (NS.po.SnapshotFoo+"#1", NS.po.rawFile, "~/.percolation/data/somedirs/something.raw"),
            (NS.po.SnapshotFoo+"#1", NS.po.rdfFile, "~/.percolation/data/somedirs/something.rdf"),
            (NS.po.SnapshotFoo+"#1", NS.po.voidFile, "~/.percolation/data/somedirs/void.raw"),
            ]
    P.add(triples,context="void")

def full():
    pass

def localFiles():
    #P.utils.getFiles("./percolation/data/") # in ~/.percolation/data/
    pass

def onlineFiles():
    #online_files=P.get((None,NS.po.onlineXML,None)),
    #triples=[]
    #for triple in online_files:
    #    triples+=[
    pass



