# routines to deliver configuration files for open linked social data
import percolation as P
c=P.utils.check

def makeFusekiConfig(names0=["labMacambiraLaleniaLog3","labMacambiraLaleniaLog2","foradoeixo","gmane-linux-audio-users","gmane-linux-audio-devel","gmane-politics-organizations-metareciclagem","arenaNETmundial_tw","matehackers"],names1=[("music_tw",15),("obama_tw",3),("porn_tw",8),("god_tw",2),("art_tw",6)],names2=["participabr","cidadedemocratica","aa","gmane-comp-gcc-libstdcPP-devel"],empty=True,names0_=[],names1_=[],names2_=[]):
    """Makes a apache/jena/fuseki configuration file.

    # names0 follows the simplest pattern
    # names1 follows the pattern with multiple files
    # names2 dont follow pattern.
    # names0_, names1_ and names2_ are given for appending to initial list.

    Loads RDF files on the fly or afterwards (empty=True default)
    with P.config.loadFuseki(makeFusekiConfig())
    """

    body=""
    execline=[]
    if not empty:
        for i, name in enumerate(names2+names2_):
            if "gcc" in name:
                url="https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate.owl".format(name,name.replace("P","+"))
            if "participabr" in name:
                url="https://raw.githubusercontent.com/OpenLinkedSocialData/opa/master/participaTriplestore.rdf"
            if "cidadedemocratica" in name:
                url="file:/disco/triplas/cdTriplestore.rdf"
            if "aa" in name:
                url="https://raw.githubusercontent.com/OpenLinkedSocialData/aa01/master/rdf/aaTriplestore.rdf"
            body+="""
<#service{}> rdf:type fuseki:Service ;
    fuseki:name                        "{}" ; 
    fuseki:serviceQuery                "query" ;
    fuseki:dataset 
       [  rdf:type ja:RDFDataset ;
          ja:defaultGraph 
            [
              a ja:MemoryModel ;
              ja:content 
                [ ja:externalContent <{}> ] ;
            ] ;
      ] .
            """.format(i,name,url)

        for i, name in enumerate(names1+names1_):
            i+=len(names2)
            urls=""
            for count in range(name[1]+1):
                url="https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate{:05d}.owl".format(name[0],name[0],count)
               
                urls+=" ja:content [ ja:externalContent <{}> ] ;\n ".format(url)
            body+="""
<#service{}> rdf:type fuseki:Service ;
    fuseki:name                        "{}" ; 
    fuseki:serviceQuery                "query" ;
    fuseki:dataset 
       [  rdf:type ja:RDFDataset ;
          ja:defaultGraph 
            [
              a ja:MemoryModel ;
                {}
            ] ;
      ] .
            """.format(i,name[0],urls)
        for i, name in enumerate(names0+names0_):
            i+=len(names1)+len(names2)
            url="https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate.owl".format(name,name)
            body+="""
<#service{}> rdf:type fuseki:Service ;
    fuseki:name                        "{}" ; 
    fuseki:serviceQuery                "query" ;
    fuseki:dataset 
       [  rdf:type ja:RDFDataset ;
          ja:defaultGraph 
            [
              a ja:MemoryModel ;
              ja:content 
                [ ja:externalContent <{}> ] ;
            ] ;
      ] .
            """.format(i,name,url)
            
    if empty:
        for i, name in enumerate(names2+names2_):
            body+="""
            <#service{}> rdf:type fuseki:Service ;
                fuseki:name                        "{}" ; 
                fuseki:serviceQuery                "sparql" ;
                fuseki:serviceQuery                "query" ;
                fuseki:serviceUpdate               "update" ;
                fuseki:serviceUpload               "upload" ;
                fuseki:serviceReadWriteGraphStore  "data" ;     
                fuseki:serviceReadGraphStore       "get" ;
                fuseki:dataset               [
                                                rdf:type ja:RDFDataset ;
                                             ] ;
                .
            """.format(i,name)
            if "gcc" in name:
                execline+=["./s-put http://localhost:82/{} default https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate.owl".format(name,name,name.replace("P","+"))]
            if "participabr" in name:
                execline+=["./s-put http://localhost:82/{} default https://raw.githubusercontent.com/OpenLinkedSocialData/opa/master/participaTriplestore.rdf".format(name)]
            if "cidadedemocratica" in name:
                execline+=["./s-put http://localhost:82/{} default /disco/triplas/cdTriplestore.rdf".format(name)]
            if "aa" in name:
                execline+=["./s-put http://localhost:82/{} default https://raw.githubusercontent.com/OpenLinkedSocialData/aa01/master/rdf/aaTriplestore.rdf".format(name)]
        for i, name in enumerate(names1+names1_):
            i+=len(names2)
            body+="""
            <#service{}> rdf:type fuseki:Service ;
                fuseki:name                        "{}" ; 
                fuseki:serviceQuery                "sparql" ;
                fuseki:serviceQuery                "query" ;
                fuseki:serviceUpdate               "update" ;
                fuseki:serviceUpload               "upload" ;
                fuseki:serviceReadWriteGraphStore  "data" ;     
                fuseki:serviceReadGraphStore       "get" ;
                fuseki:dataset               [
                                                rdf:type ja:RDFDataset ;
                                             ] ;
                .
            """.format(i,name[0])
            count=0
            for arq in range(name[1]+1):
                execline+=["./s-put http://localhost:82/{} default https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate{:05d}.owl".format(name[0],name[0],name[0],count)]
                count+=1
        for i, name in enumerate(names0+names0_):
            i+=len(names1)+len(names2)
            body+="""
            <#service{}> rdf:type fuseki:Service ;
                fuseki:name                        "{}" ; 
                fuseki:serviceQuery                "sparql" ;
                fuseki:serviceQuery                "query" ;
                fuseki:serviceUpdate               "update" ;
                fuseki:serviceUpload               "upload" ;
                fuseki:serviceReadWriteGraphStore  "data" ;     
                fuseki:serviceReadGraphStore       "get" ;
                fuseki:dataset               [
                                                rdf:type ja:RDFDataset ;
                                             ] ;
                .
            """.format(i,name)
            execline+=["./s-put http://localhost:82/{} default https://raw.githubusercontent.com/OpenLinkedSocialData/{}/master/rdf/{}Translate.owl".format(name,name,name)]

    body+="""
        <#service{}> rdf:type fuseki:Service ;
        # URI of the dataset -- http://host:port/dsfoo
        fuseki:name                        "dsfoo" ; 
        fuseki:serviceQuery                "sparql" ;
        fuseki:serviceQuery                "query" ;
        fuseki:serviceUpdate               "update" ;
        fuseki:serviceUpload               "upload" ;
        fuseki:serviceReadWriteGraphStore  "data" ;     
        fuseki:serviceReadGraphStore       "get" ;
        fuseki:dataset               [
                                    rdf:type ja:RDFDataset ;
                                 ] ;
        .
        """.format(len(names0)+len(names1)+len(names2))

    header="""
    @prefix :        <#> .
    @prefix fuseki:  <http://jena.apache.org/fuseki#> .
    @prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

    @prefix rdfs:       <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix tdb:        <http://jena.hpl.hp.com/2008/tdb#> .
    @prefix ja:         <http://jena.hpl.hp.com/2005/11/Assembler#> .
    @prefix tw:         <http://purl.org/socialparticipation/tw/> .
    @prefix irc:        <http://purl.org/socialparticipation/irc/> .
    @prefix fb:         <http://purl.org/socialparticipation/fb/> .
    @prefix opa:        <http://purl.org/socialparticipation/opa/> .
    @prefix ocd:        <http://purl.org/socialparticipation/ocd/> .
    @prefix aa:         <http://purl.org/socialparticipation/aa/> .
    @prefix gmane:      <http://purl.org/socialparticipation/gmane/> .

    [] rdf:type fuseki:Server ;
       fuseki:services ("""+" ".join(["<#service{}>".format(i) for i in range(len(names0)+len(names1)+len(names2)+1)])+" ) .\n\n"
    fname="configAuto.ttl"
    f=open(fname,"w")
    f.write(header+body)
    f.close()
    c("{} written".format(fname))
    return execline

results=[]
def loadFuseki(execline):
    global results
    for line in execline:
        how=os.system(line)
        results.append(how)
