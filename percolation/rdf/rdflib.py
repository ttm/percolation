from datetime import datetime
def info():
   uri_chars="""reserved    = gen-delims / sub-delims
gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"
sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
            / "*" / "+" / "," / ";" / "="
unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~"
https://tools.ietf.org/html/rfc3986#section-2

NOTE: URI is not split with "%"
r.namespace.split_uri("http://purl.org/socialparticipation/irc/Participant#labMacambiraLaleniaLog1%2818")"""
 
def timestampedURI(uriref=None,stringid="",datetime_=None):
    if not datetime:
        datetime_=datetime.now()
    sid=stringid+datetime_.isoformat()
    newurired=uriref+"#"+sid
    return newuriref
def get(subject=None,predicate=None,object_=None,context=None,percolation_graph=None):
    if not percolation_graph:
        percolation_graph=P.percolation_graph
    triples=[triple for triple in percolation_graph((subject,predicate,object_),context)]
    if len(triples)==1: # only one triple
        triples=triples[0]
    return triples
