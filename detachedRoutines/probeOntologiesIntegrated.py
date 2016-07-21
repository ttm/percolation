import percolation as P
# graphs
# graphs = ('urn:twitter-legacy-ChennaiFloodsTweet00003.ttl', )
# graphs = ('urn:twitter-legacy-arenaNETmundialTweet00000.ttl', 'urn:twitter-legacy-arenaNETmundialTweetMeta.ttl')
# graphs_ = [('urn:facebook-legacy-AntonioAnzoategui18022013Friendship.ttl', 'urn:facebook-legacy-AntonioAnzoategui18022013Meta.ttl')]
graphs_ = [
    ('urn:facebook-legacy-Auricultura10042013Friendship.ttl',
     'urn:facebook-legacy-Auricultura10042013Interaction.ttl',
     'urn:facebook-legacy-Auricultura10042013Posts.ttl')
]
# graphs_ += [
#     ('urn:twitter-legacy-arenaNETmundialTweet00000.ttl'),
# ]
graphs_ += [
    ('urn:irc-legacy-hackerspace-cpsLog00000.ttl',
    'urn:irc-legacy-hackerspace-cpsLog00001.ttl',
    'urn:irc-legacy-hackerspace-cpsLog00002.ttl',)
]
endpoint_url = 'http://localhost:8890/sparql'


for graphs in graphs_:
    fvars = P.rdf.probeOntology(endpoint_url, graphs, 'testOntology')
