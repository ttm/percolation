import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl


def textAnalysis(client):
    prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
    snapshots = pl(client.retrieveQuery(prefix+'SELECT DISTINCT ?snap WHERE { ?s po:snapshot ?snap }'))
    snapshot = [snap for snap in snapshots if 'Twitter' in snap][0]
    # P.topology()
    network = P.utils.makeNetworkFromSnapshotid(client, snapshot)
    analysis = P.legacy.analyses.topological.TopologicalAnalysis(network['gg'])

    q = '''SELECT ?author ?text WHERE {
            ?tweet po:author ?author .
            ?tweet po:message ?text .
        }
        '''
    authors_text = pl(client.retrieveQuery(prefix+q))
    P.measures.text.overall.measureAll(authors_text, analysis.sectors['sectorialized_agents'])
    return snapshot, analysis


def analysis(client):
    snapshot = P.utils.pickSnapshot(client)
    # P.topology()
    network = P.utils.makeNetworkFromSnapshotid(client, snapshot)
    analysis = P.legacy.analyses.topological.TopologicalAnalysis(network['gg'])

    return snapshot, analysis
