import percolation as P
import rdflib as r
import networkx as x
import numpy as n
class NetworkEvolution:
    def __init__(self, window_size=200, step_size=200):
        self.window_size = window_size
        self.step_size = step_size
    def load(self, message_participant, replies):
        self.messageids = [i[0] for i in message_participant]
        # [msguri] = participanturi
        self.message_participant = dict(message_participant)
        interactions = {}
        for interaction in replies:
            # [msguri_reply] = msguri_original
            interactions[r.URIRef(interaction[1])] = r.URIRef(interaction[0])
        self.interactions = interactions
    def makeNetwork(self, messageids):
        g = x.DiGraph()
        for mid in messageids:
            participant = self.message_participant[mid]
            if participant not in g.nodes():
                g.add_node(participant)
            if mid in self.interactions.keys():  # if message is a reply
                mid0 = self.interactions[mid]
                # print('BANANA0', mid0)
                if mid0 in self.message_participant.keys() and mid0 in messageids:  # reply to message in snapshot
                    # print('BANANA')
                    participant0 = self.message_participant[mid0]
                    if participant0 not in g.nodes():
                        g.add_node(participant0)
                    if g.has_edge(participant0, participant):
                        g[participant0][participant]['weight'] += 1
                    else:
                        g.add_edge(participant0, participant, weight=1)
        return g
    def evolve(self, sectorialize=True, pca = True):
        self.networks = []
        self.networks_measures = []
        self.networks_pcas = []
        self.networks_sectorializations = []
        pointer = 0
        while pointer+self.window_size < len(self.messageids):
            mids = self.messageids[pointer:pointer+self.window_size]
            network = self.makeNetwork(mids)
            measures = self.takeMeasures(network)
            self.networks.append(network)
            self.networks_measures.append(measures)
            if pca:
                pca = P.analysis.pca.NetworkPCA(measures)
                self.networks_pcas.append(pca)
            if sectorialize:
                # minimum_incidence = max(1, int(measures.N*0.02))
                minimum_incidence = 2
                sectorialization = P.analysis.sectorialize.NetworkSectorialization(measures, minimum_incidence)
                del sectorialization.binomial
                self.networks_sectorializations.append(sectorialization)
            pointer += self.step_size
    def takeMeasures(self, network):
        N = network.number_of_nodes()
        E = network.number_of_edges()
        edges = network.edges(data=True)

        degrees = network.degree()
        nodes_ = sorted(network.nodes(), key=lambda x : degrees[x])
        degrees_ = [degrees[i] for i in nodes_]
        in_degrees = network.in_degree()
        in_degrees_ = [in_degrees[i] for i in nodes_]
        out_degrees = network.out_degree()
        out_degrees_ = [out_degrees[i] for i in nodes_]

        strengths = network.degree(weight="weight")
        strengths_ = [strengths[i] for i in nodes_]
        in_strengths = network.in_degree(weight="weight")
        in_strengths_ = [in_strengths[i] for i in nodes_]
        out_strengths = network.out_degree(weight="weight")
        out_strengths_ = [out_strengths[i] for i in nodes_]

        asymmetries = []
        disequilibriums = []
        asymmetries_edge_mean = []
        asymmetries_edge_std = []
        disequilibrium_edge_mean = []
        disequilibrium_edge_std = []

        for node in nodes_:
            if not degrees[node]:
                asymmetries.append(0.)
                disequilibriums.append( 0.)
                asymmetries_edge_mean.append(0.)
                asymmetries_edge_std.append(0.)    
                disequilibrium_edge_mean.append(0.)
                disequilibrium_edge_std.append(0.)
            else:
                asymmetries.append(
                    (in_degrees[node]-out_degrees[node])/degrees[node])
                disequilibriums.append( 
                    (in_strengths[node]-out_strengths[node])/strengths[node])
                edge_asymmetries = ea = []
                edge_disequilibriums = ed = []
                predecessors = network.predecessors(node)
                successors = network.successors(node)
                for pred in predecessors:
                    if pred in successors:
                        ea.append( 0. )
                        ed.append((network[pred][node]['weight']-network[node][pred]['weight'])/strengths[node])
                    else:
                        ea.append( 1. )
                        ed.append(network[pred][node]['weight']/strengths[node])
                for suc in successors:
                    if suc in predecessors:
                        pass
                    else:
                        ea.append(-1.)
                        ed.append(-network[node][suc]['weight']/strengths[node])
                asymmetries_edge_mean.append(   n.mean(ea))
                asymmetries_edge_std .append(   n.std(ea))  
                disequilibrium_edge_mean.append(n.mean(ed))
                disequilibrium_edge_std.append( n.std(ed)) 

        weighted_directed_betweenness = x.betweenness_centrality(network, weight="weight")
        weighted_directed_betweenness_ = [weighted_directed_betweenness[i] for i in nodes_]
        weighted_clusterings = x.clustering( P.utils.toUndirected(network), weight="weight")
        weighted_clusterings_ = [weighted_clusterings[i] for i in nodes_]
        # class NetworkMeasures:
        #     pass
        # nm = NetworkMeasures()
        # nm = lambda: None  # network measures
        # nm = type('', (), {})()
        nm = P.utils.EmptyClass()  # network measures
        locals_ = locals().copy()
        for i in locals_:
            if i != "self" and i != 'nm':
                exec("nm.{}={}".format(i, i))
        return nm

