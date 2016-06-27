import percolation as P


def analysis(client):
    snapshot = P.utils.pickSnapshot(client)
    # P.topology()
    network = P.utils.makeNetworkFromSnapshotid(client, snapshot)
    analysis = P.legacy.analyses.topological.TopologicalAnalysis(network['gg'])

    return snapshot, analysis
