from percolation.rdf import NS, a
def literature():
    triples=[
            (NS.po.Literature+"#decorator",NS.po.url,"http://pythonhosted.org/decorator/documentation.html"),
            (NS.po.Literature+"#decorator",NS.rdfs.comment,"Solid package with examples on keeping cache of function calls\
                    and making calls asynchronous and print status messages about the function"),
            ]
    return triples
