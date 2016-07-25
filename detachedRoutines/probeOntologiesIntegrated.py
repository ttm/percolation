import percolation as P
# graphs
# graphs = ('urn:twitter-legacy-ChennaiFloodsTweet00003.ttl', )
# graphs = ('urn:twitter-legacy-arenaNETmundialTweet00000.ttl', 'urn:twitter-legacy-arenaNETmundialTweetMeta.ttl')
# graphs_ = [('urn:facebook-legacy-AntonioAnzoategui18022013Friendship.ttl', 'urn:facebook-legacy-AntonioAnzoategui18022013Meta.ttl')]
graphs_ = [('urn:facebook-legacy-AntonioAnzoategui18022013Friendship.ttl',)]
graphs_ += [
    ('urn:facebook-legacy-Auricultura10042013Friendship.ttl',
     'urn:facebook-legacy-Auricultura10042013Interaction.ttl',
     'urn:facebook-legacy-Auricultura10042013Posts.ttl')
]
graphs_ += [
    (
     'urn:facebook-legacy-Auricultura10042013Meta.ttl',
     'urn:facebook-legacy-Auricultura10042013Friendship.ttl',
     'urn:facebook-legacy-Auricultura10042013Interaction.ttl',
     'urn:facebook-legacy-Auricultura10042013Posts.ttl')
]
graphs_ += [
    ('urn:twitter-legacy-arenaNETmundialTweet00000.ttl',),
]
graphs_ += [
    (
     'urn:twitter-legacy-arenaNETmundialMeta.ttl',
     'urn:twitter-legacy-arenaNETmundialTweet00000.ttl',
    ),
]
graphs_ += [
    ('urn:irc-legacy-hackerspace-cpsLog00000.ttl',
     'urn:irc-legacy-hackerspace-cpsLog00001.ttl',
     'urn:irc-legacy-hackerspace-cpsLog00002.ttl',)
]
graphs_ += [
    (
     'urn:irc-legacy-hackerspace-cpsMeta.ttl',
     'urn:irc-legacy-hackerspace-cpsLog00000.ttl',
     'urn:irc-legacy-hackerspace-cpsLog00001.ttl',
     'urn:irc-legacy-hackerspace-cpsLog00002.ttl',)
]
graphs_ += [
    (
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00000.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00001.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00002.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00003.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00004.ttl',
    )
]
graphs_ += [
    (
     'urn:gmane-legacy-.linux.audio.devel1-20000Meta.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00000.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00001.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00002.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00003.ttl',
     'urn:gmane-legacy-.linux.audio.devel1-20000Email00004.ttl',
    )
]
graphs_ += [
    (
        'urn:participabrMeta.ttl',
        'urn:participabr.ttl',
    )
]
graphs_ += [
    (
        'urn:participabr.ttl',
    )
]
graphs_ += [
    (
        'urn:cidadedemocraticaMeta.ttl',
        'urn:cidadedemocratica00000.ttl',
        'urn:cidadedemocratica00001.ttl',
        'urn:cidadedemocratica00002.ttl',
        'urn:cidadedemocratica00003.ttl',
        'urn:cidadedemocratica00004.ttl',
        'urn:cidadedemocratica00005.ttl',
        'urn:cidadedemocratica00006.ttl',
        'urn:cidadedemocratica00007.ttl',
        'urn:cidadedemocratica00008.ttl',
        'urn:cidadedemocratica00009.ttl',
        'urn:cidadedemocratica00010.ttl',
        'urn:cidadedemocratica00011.ttl',
        'urn:cidadedemocratica00012.ttl',
        'urn:cidadedemocratica00013.ttl',
        'urn:cidadedemocratica00014.ttl',
        'urn:cidadedemocratica00015.ttl',
    )
]
graphs_ += [
    (
        'urn:cidadedemocratica00000.ttl',
        'urn:cidadedemocratica00001.ttl',
        'urn:cidadedemocratica00002.ttl',
        'urn:cidadedemocratica00003.ttl',
        'urn:cidadedemocratica00004.ttl',
        'urn:cidadedemocratica00005.ttl',
        'urn:cidadedemocratica00006.ttl',
        'urn:cidadedemocratica00007.ttl',
        'urn:cidadedemocratica00008.ttl',
        'urn:cidadedemocratica00009.ttl',
        'urn:cidadedemocratica00010.ttl',
        'urn:cidadedemocratica00011.ttl',
        'urn:cidadedemocratica00012.ttl',
        'urn:cidadedemocratica00013.ttl',
        'urn:cidadedemocratica00014.ttl',
        'urn:cidadedemocratica00015.ttl',
    )
]
graphs_ += [
    (
        'urn:aaircMeta.ttl',
        'urn:aamongoMeta.ttl',
        'urn:aamysqlMeta.ttl',
        'urn:aairc.ttl',
        'urn:aamongo.ttl',
        'urn:aamysql.ttl',
    )
]
graphs_ += [
    (
        'urn:aairc.ttl',
        'urn:aamongo.ttl',
        'urn:aamysql.ttl',
    )
]
endpoint_url = 'http://localhost:8890/sparql'


for graphs in graphs_[3:5]:
    if 'Meta.' in graphs[0]:
        fvars = P.rdf.probeOntology(endpoint_url, graphs, 'ontologies/'+graphs[0].split(':')[1], one_datatype=False)
    else:
        fvars = P.rdf.probeOntology(endpoint_url, graphs, 'ontologies/'+graphs[0].split(':')[1])
