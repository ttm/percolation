import percolation as P


class TopologicalAnalysis:
    def __init__(self, g='networkx_network'):
        self.topom_dict = P.measures.topology.directMeasures.topologicalMeasures(g)
        self.sectors = P.measures.topology.erdosSectors.getErdosSectors(self.topom_dict)
        self.scale_free = P.measures.topology.powerLawFit.fitNetwork(self.topom_dict)
