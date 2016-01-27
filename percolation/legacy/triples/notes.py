from percolation.rdf import NS, a
def triplification():
    triples=[
            (NS.po.Note+"#FBTriplification1",rdfs.comment,"Netvizz replaces post texts colons ',' and linebreaks '\\n' into underscores '_'\
                    in the posts triplification, all underscores are replaced by  linebreaks '\\n'") 
            ]
def literature():
    triples=[
            (NS.po.Literature+"#decorator",NS.po.url,"http://pythonhosted.org/decorator/documentation.html"),
            (NS.po.Literature+"#decorator",NS.rdfs.comment,"Solid package with examples on keeping cache of function calls\
                    and making calls asynchronous and print status messages about the function"),
            ]
    return triples
