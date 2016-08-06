from percolation.rdf.sparql.functions import plainQueryValues as pl
from percolation.rdf import prefix
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'

def outlineTable(client, final_path='./'):
    # for each of the four snapshots, get
    # date of first and last message
    # number of participants
    # number of threads
    # missing messages is 20000 - total messages
    lacronyms = {'LAU': "gmane.linux.audio.users",
                 'CPP': "gmane.comp.gcc.libstdc++.devel",
                 'MET': "gmane.politics.organizations.metareciclagem",
                 'LAD': "gmane.linux.audio.devel"}
    order = ['LAU', 'LAD', 'MET', 'CPP']
    data = []
    for alist in order:
        q = '''select ?date where {
        ?message po:createdAt ?date .
        ?message po:snapshot ?snap .
        ?snap po:gmaneID "%s" } ORDER BY ?date LIMIT 3''' % (lacronyms[alist],) 
        datemin = pl(client.retrieveQuery(prefix+q))[-1:]
        q = '''select (MAX(?date) as ?ldate) where {
        ?message po:createdAt ?date . 
        ?message po:snapshot ?snap .
        ?snap po:gmaneID "%s" . }''' % (lacronyms[alist],)
        datemax = pl(client.retrieveQuery(prefix+q))
        dates = datemin+datemax
        dates = [i.split('T')[0] for i in dates]
        q = '''select (COUNT(DISTINCT ?participant) as ?cp) where {
        ?participant a po:Participant .
        ?participant po:snapshot ?snap .
        ?snap po:gmaneID "%s" . }''' % (lacronyms[alist],)
        nparticipants = pl(client.retrieveQuery(prefix+q))
        # q = '''select (COUNT(DISTINCT ?messages) as ?cmessages) where {
        # ?message po:snapshot ?snap .
        # FILTER NOT EXISTS { ?message po:replyTo ?message2 }
        # ?snap po:gmaneID "%s" . }''' % (lacronyms[alist],)
        # nthreads = pl(client.retrieveQuery(prefix+q))

        order_ = [i for i in order if i!=alist]
        q = '''select (COUNT(DISTINCT ?message) as ?cmessages) where {
        ?message a po:EmailMessage .
        ?message po:author ?author .
        ?message po:createdAt ?createdat .
        ?message po:text ?text .
        ?author po:observation ?obs .
        ?obs po:email ?email .
        ?author po:snapshot ?snap .
        ?obs po:snapshot ?snap .
        ?message po:snapshot ?snap .
        ?snap po:gmaneID "%s" }''' % (lacronyms[alist])
        nempty = 20000 - pl(client.retrieveQuery(prefix+q))[0]

        q = '''select (COUNT(DISTINCT ?message) as ?cmessages) where {
        ?message po:replyTo ?message2 . 
        ?message po:snapshot ?snap .
        ?snap po:gmaneID "%s" . }''' % (lacronyms[alist],)
        nthreads = [20000 - nempty - pl(client.retrieveQuery(prefix+q))[0]]

        data.append([])
        data[-1] += dates + nparticipants + nthreads + [nempty]
    return data, q


