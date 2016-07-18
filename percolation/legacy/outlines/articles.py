# from percolation import c
from percolation.rdf.sparql.functions import plainQueryValues as pl

prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'


def outlineText(client):
    ntriples = pl(client.retrieveQuery(prefix+'SELECT (COUNT(*) as ?c) WHERE { ?s ?p ?o . }'))[0]
    nedges = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?interaction) as ?c) WHERE { { ?interaction a po:Friendship } UNION { ?interaction a po:Interaction } UNION { ?interaction po:retweetOf ?message } UNION { ?interaction po:replyTo ?message } UNION { ?interaction po:directedTo ?participant } . }'))[0]
    nparticipants = pl(client.retrieveQuery(prefix+'SELECT (COUNT(DISTINCT ?author) as ?c) WHERE { ?author a po:Participant . }'))[0]
    nchars = pl(client.retrieveQuery(prefix+'SELECT (SUM(?nchars) as ?total) WHERE { ?message po:nChars ?nchars . }'))[0]
    text = 'Database consists of {} triples, {} edges yield by interactions or relations, {} participants and {} characters.'.format(ntriples, nedges, nparticipants, nchars)

    nego = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?snap) as ?csnap) WHERE { ?snap po:isEgo true }'))[0]
    ngroup = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?snap) as ?csnap) WHERE { ?snap po:isGroup true }'))[0]
    ninteraction = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?snap) as ?csnap) WHERE { ?snap po:isInteraction true }'))[0]
    nfriendship = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?snap) as ?csnap) WHERE { ?snap po:isFriendship true }'))[0]
    ntext = pl(client.retrieveQuery(prefix+'SELECT (COUNT(?snap) as ?csnap) WHERE { ?snap po:isPost true }'))[0]
    text += ' Among all snapshots, {} are ego snapshots, {} are group snapshots; {} have interaction edges, {} have friendship edges; {} have text content from messages.'.format(
        nego, ngroup, ninteraction, nfriendship, ntext)
    return text


def outlineNSnapshots(client):
    snapshot_types = pl(client.retrieveQuery(prefix+'SELECT DISTINCT ?stype WHERE { ?snap a po:Snapshot . ?snap a ?stype . }'))
    nsnaps = {}
    for stype in snapshot_types:
        nsnaps_ = pl(client.retrieveQuery(prefix+'SELECT (COUNT(DISTINCT ?snap) as ?csnap) WHERE { ?snap a <%s> }' % (stype,)))[0]
        nsnaps[stype] = nsnaps_
    return nsnaps

    # get all snapshot types and count them
    return text


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
