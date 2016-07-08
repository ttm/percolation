# from percolation import c
from percolation.rdf.sparql.functions import plainQueryValues as pl

prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'


def outline(client):
    # get all snapshots
    # snapshots = pl(client.retrieveQuery(prefix+'select distinct ?g where { GRAPH ?g {?s ?p ?o} }SELECT DISTINCT ?snap WHERE { GRAPH <urn:percolation> { ?s po:snapshot ?snap . } }'))
    snapshots = pl(client.retrieveQuery(prefix+'SELECT DISTINCT ?snap WHERE { ?s po:snapshot ?snap }'))
    snaps = {}
    for snapshot in snapshots:
        # get number of triples
        # ntriples = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?s) as ?c) WHERE { ?s ?p ?o . ?s po:snapshot <%s> . }' % (snapshot,)))
        ntriples = pl(client.retrieveQuery(prefix+'SELECT (COUNT(*) as ?c) WHERE { ?s ?p ?o . ?s po:snapshot <%s> . }' % (snapshot,)))[0]
        # get number of edges: union replyTo (gmane), directedTo (irc),
        # retweetOf (tweet)
        # nedges1 = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?interaction) as ?c) WHERE { { ?interaction po:retweetOf ?message } UNION { ?interaction po:replyTo ?message } UNION { ?interaction po:directedTo ?participant } . ?interaction po:snapshot <%s> }' % (snapshot,)))
        # # number of union Friendship, Interaction (facebook)
        # nedges2 = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?interaction) as ?c) WHERE { { ?interaction a po:Friendship } UNION { ?interaction a po:Interaction } . ?interaction po:snapshot <%s> }' % (snapshot,)))
        # nedges = nedges1+nedges2
        nedges = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?interaction) as ?c) WHERE { { ?interaction a po:Friendship } UNION { ?interaction a po:Interaction } UNION { ?interaction po:retweetOf ?message } UNION { ?interaction po:replyTo ?message } UNION { ?interaction po:directedTo ?participant } . ?interaction po:snapshot <%s> }' % (snapshot,)))[0]
        # get number of participants
        nparticipants = pl(client.retrieveQuery(prefix+'SELECT (COUNT(DISTINCT ?author) as ?c) WHERE { ?author a po:Participant .  ?author po:snapshot <%s> . }' % (snapshot,)))[0]
        # get number of chars
        nchars = pl(client.retrieveQuery(prefix+'SELECT (SUM(?nchars) as ?total) WHERE { ?message po:nChars ?nchars . ?message po:snapshot <%s> . }' % (snapshot,)))[0]
        snaps[snapshot] = {'ntriples': ntriples,
                           'nedges': nedges,
                           'nparticipants': nparticipants,
                           'nchars': nchars}
    # return snapshots
    return snaps
