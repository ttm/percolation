import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl
from percolation.rdf import prefix
import os
import dateutil.parser
import numpy as n
import networkx as x
import social as S
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
lacronyms = {'LAU': "gmane.linux.audio.users",
             'CPP': "gmane.comp.gcc.libstdc++.devel",
             'MET': "gmane.politics.organizations.metareciclagem",
             'LAD': "gmane.linux.audio.devel"}
order = ['LAU', 'LAD', 'MET', 'CPP']

# def circularTable(client, final_path='../../../stabilityInteraction/tables/', pickledir='../../../pickledir/'):
def extraNetworks(final_path=os.path.dirname(__file__)+'/../../../../stabilityInteraction/tables/', pickledir=os.path.dirname(__file__)+'/../../../pickledir/', social_path=os.path.dirname(__file__)+'/../../../../social/'):

    ans = input('try to reload extra networks and analysis? (Y/n)')
    if ans == 'n' or not os.path.isfile(pickledir+'extraNetworks.pickle'):
        fg = S.utils.GDFgraph(social_path+'data/facebook/avlab_RenatoFabbri22022014.gdf') # graph should be on fg.G
        fg2 = S.utils.GDFgraph(social_path+'data/facebook/ego_MassimoCanevacci19062013.gdf') # graph should be on fg.G
        fg3 = S.utils.GDFgraph(social_path+'data/facebook/DemocraciaDiretaJa14072013.gdf') # graph should be on fg.G
        fg4 = S.utils.GDFgraph(social_path+'data/facebook/SiliconValleyGlobalNetwork27042013.gdf') # graph should be on fg.G
        fg5 = x.read_graphml(social_path+'data/extraData/amizadesParticipa.graphml') # graph should be on fg.G

        fd = S.utils.GDFgraph(social_path+'data/facebook/SiliconValleyGlobalNetwork27042013_interactions.gdf') # graph should be on fg.G
        fd2 = S.utils.GDFgraph(social_path+'data/facebook/SolidarityEconomy12042013_interactions.gdf') # graph should be on fg.G
        fd3 = S.utils.GDFgraph(social_path+'data/facebook/DemocraciaDiretaJa14072013_interactions.gdf') # graph should be on fg.G
        fd4 = S.utils.GDFgraph(social_path+'data/facebook/CienciasComFronteiras29032013_interactions.gdf') # graph should be on fg.G
        fd5 = x.read_graphml(social_path+'data/extraData/interacoesParticipa.graphml') # graph should be on fg.G

        tweets = S.twitter.pickle2rdf.readPickleTweetFile(social_path+'data/twitter/arenaNETmundial_tw.pickle')[0]
        G,G_ = S.utils.makeRetweetNetwork(tweets)
        F=[fg.G,fg2.G,fg3.G,fg4.G,fg5,fd.G,fd2.G,fd3.G,fd4.G,fd5,G,G_]

        def part(network):
            class NetworkMeasures_:
                pass
            nm=nm=NetworkMeasures_()
            nm.degrees=network.degree()
            nm.nodes_= sorted(network.nodes(), key=lambda x : nm.degrees[x])
            nm.degrees_=[nm.degrees[i] for i in nm.nodes_]
            nm.edges=     network.edges(data=True)
            nm.E=network.number_of_edges()
            nm.N=network.number_of_nodes()
            # np=g.NetworkPartitioning(nm,10,metric="g")
            np=P.analysis.sectorialize.NetworkSectorialization(nm,10,metric="g")
            return np

        parts=[]
        fracs=[]
        print("iniciando particionamentos")
        for net in F:
            pp=part(net)
            parts.append(pp)
            ll=[len(i) for i in pp.sectorialized_agents__]
            ll=[100*i/sum(ll) for i in ll]
            fracs.append(ll)

        def pca(network):
            class NetworkMeasures_:
                pass
            nm=nm=NetworkMeasures_()
            nm.degrees=network.degree()
            nm.nodes_= sorted(network.nodes(), key=lambda x : nm.degrees[x])
            nm.degrees_=[nm.degrees[i] for i in nm.nodes_]

            nm.gu=network.to_undirected()
            if network.is_directed():
                nm.weighted_directed_betweenness=x.betweenness_centrality(network,weight="weight")
                nm.weighted_clusterings=x.clustering( nm.gu ,weight="weight")
                nm.strengths=     network.degree(weight="weight")
                nm.strengths_=[nm.strengths[i] for i in nm.nodes_]
            else:
                nm.weighted_directed_betweenness=x.betweenness_centrality(network)
                nm.weighted_clusterings=x.clustering( nm.gu )
            nm.weighted_directed_betweenness_=[
              nm.weighted_directed_betweenness[i] for i in nm.nodes_]

            nm.weighted_clusterings_=[nm.weighted_clusterings[i] for i in nm.nodes_]
            if network.is_directed():
                nm.in_degrees=network.in_degree()
                nm.in_degrees_=[nm.in_degrees[i] for i in nm.nodes_]
                nm.out_degrees=network.out_degree()
                nm.out_degrees_=[nm.out_degrees[i] for i in nm.nodes_]
                nm.in_strengths= network.in_degree(weight="weight")
                nm.in_strengths_=[nm.in_strengths[i] for i in nm.nodes_]
                nm.out_strengths=network.out_degree(weight="weight")
                nm.out_strengths_=[nm.out_strengths[i] for i in nm.nodes_]

            nm.edges=     network.edges(data=True)
            nm.E=network.number_of_edges()
            nm.N=network.number_of_nodes()


            # symmetry measures
            if network.is_directed():
                nm.asymmetries=asymmetries=[]
                nm.disequilibriums=disequilibriums=[]
                nm.asymmetries_edge_mean=asymmetries_edge_mean=[]
                nm.asymmetries_edge_std=asymmetries_edge_std=[]
                nm.disequilibrium_edge_mean=disequilibrium_edge_mean=[]
                nm.disequilibrium_edge_std=disequilibrium_edge_std=[]
                for node in nm.nodes_:
                    if not nm.degrees[node]:
                        asymmetries.append(0.)
                        disequilibriums.append( 0.)
                        asymmetries_edge_mean.append(0.)
                        asymmetries_edge_std .append(0.)    
                        disequilibrium_edge_mean.append(0.)
                        disequilibrium_edge_std.append(0.)
                    else:
                        asymmetries.append(
                            (nm.in_degrees[node]-nm.out_degrees[node])/nm.degrees[node])
                        disequilibriums.append( 
                            (nm.in_strengths[node]-nm.out_strengths[node])/nm.strengths[node])
                        edge_asymmetries=ea=[]
                        edge_disequilibriums=ed=[]
                        predecessors=network.predecessors(node)
                        successors=  network.successors(node)
                        for pred in predecessors:
                            if pred in successors:
                                ea.append( 0. )
                                ed.append((network[pred][node]['weight']-network[node][pred]['weight'])/nm.strengths[node])
                            else:
                                ea.append( 1. )
                                ed.append(network[pred][node]['weight']/nm.strengths[node])
                        for suc in successors:
                            if suc in predecessors:
                                pass
                            else:
                                ea.append(-1.)
                                ed.append(-network[node][suc]['weight']/nm.strengths[node])
                        asymmetries_edge_mean.append(   n.mean(ea))
                        asymmetries_edge_std .append(   n.std(ea))  
                        disequilibrium_edge_mean.append(n.mean(ed))
                        disequilibrium_edge_std.append( n.std(ed)) 
            np = P.analysis.pca.NetworkPCA(nm)
            return np
        pcas=[]
        for net in F:
            pp=pca(net)
            pcas.append(pp)
            print("+1pca de net de F")
        for pa in parts: del pa.binomial
        # P.utils.pDump(F,pickledir+"F.pickle")
        # P.utils.pDump(pcas,pickledir+"pcasFB-TW.pickle")
        # P.utils.pDump(parts,pickledir+"partsFB-TW.pickle")
        # P.utils.pDump(fracs,pickledir+"fracsFB-TW.pickle")
        P.utils.pDump((F, pcas, parts, fracs), pickledir+"extraNetworks.pickle")
    else:
        F, pcas, parts, fracs = P.utils.pRead(pickledir+"extraNetworks.pickle")

    labels1=["$cc$","$k$","$bt$","$\\lambda$"]
    labels2=["$cc$","$s$","$s^{in}$","$s^{out}$",
             "$k$","$k^{in}$","$k^{out}$","$bt$","$\\lambda$"]
    labels3=["$cc$","$s$","$s^{in}$","$s^{out}$",
             "$k$","$k^{in}$","$k^{out}$","$bt$",
             "$asy$", "$\\mu^{asy}$","$\\sigma^{asy}$",
             "$dis$","$\\mu^{dis}$","$\\sigma^{dis}$","$\\lambda$"]
    labels_=["F1","F2","F3","F4","F5",
            "I1","I2","I3","I4","I5",
            "TT1","TT2"]

    # for i, label in enumerate(labels_):
    #     pca=pcas[i]
    #     vals=n.vstack((pca.pca1.eig_vectors_, pca.pca1.eig_values_))
    #     tstring=g.makeTables(labels1,vals)
    #     g.writeTex(tstring,TDIR+"tabPCA1{}.tex".format(label))

    # montar matriz de dados unica, 3 x nlistas = 27 colunas x 4 colunas
    NF = 5 # number of friendship networks
    NI = len(labels_)-NF # number of interaction networks
    nn = n.zeros((4,NF*3))
    for i in range(NF):
        pca=pcas[i]
        nn[:,i::NF]=n.abs(n.vstack((pca.pca1.eig_vectors_,pca.pca1.eig_values_)))

    tstring = P.mediaRendering.tables.makeTabular(labels1,nn,True)
    P.mediaRendering.tables.writeTex(tstring,final_path+"tabPCA1ExtraFNEW.tex")

    nn_=n.zeros((4,NI*3))
    for i in range(NI):
        pca=pcas[i+NF]
        nn_[:,i::NI]=n.abs(n.vstack((pca.pca1.eig_vectors_,pca.pca1.eig_values_)))

    tstring=P.mediaRendering.tables.makeTabular(labels1,nn_,True)
    P.mediaRendering.tables.writeTex(tstring,final_path+"tabPCA1ExtraINEW.tex")

    nn2=n.zeros((9,len(labels_[5:])*3))
    for i in range(5,len(labels_)):
        pca=pcas[i]
        nn2[:,i-5::len(labels_[5:])]=n.abs(n.vstack((pca.pca2.eig_vectors_[:,:3],pca.pca2.eig_values_[:3])))
    tstring2=P.mediaRendering.tables.makeTabular(labels2,nn2,True)
    P.mediaRendering.tables.writeTex(tstring2,final_path+"tabPCA2ExtraNEW.tex")

    nn3=n.zeros((15,len(labels_[5:])*3))
    for i in range(5,len(labels_)):
        pca=pcas[i]
        nn3[:,i-5::len(labels_[5:])]=n.abs(n.vstack((pca.pca3.eig_vectors_[:,:3],pca.pca3.eig_values_[:3])))
    tstring3=P.mediaRendering.tables.makeTabular(labels3,nn3,True)
    P.mediaRendering.tables.writeTex(tstring3,final_path+"tabPCA3ExtraNEW.tex")

    tstring3=P.mediaRendering.tables.makeTabular(labels_,n.array(fracs),True)
    P.mediaRendering.tables.writeTex(tstring3,final_path+"tabSectorsExtraNEW.tex")

    # Tabela geral sobre cada lista com:
    # sigla, proveniencia, critério para formação de aresta, dirigida ou nao, description, número de vertices, numero de arestas 
    data = [["F1", "Facebook","friendship","no","the friendship network of Renato Fabbri (author)",str(F[0].number_of_nodes()),str(F[0].number_of_edges())],
            ["F2", "Facebook","friendship","no","the friendship network of Massimo Canevacci (senior anthropologist)",str(F[1].number_of_nodes()),str(F[1].number_of_edges())],
            ["F3", "Facebook","friendship","no","the friendship network of a brazilian direct democracy group",str(F[2].number_of_nodes()),str(F[2].number_of_edges())],
            ["F4", "Facebook","friendship","no","the friendship network of the Silicon Valley Global Network group",str(F[3].number_of_nodes()),str(F[3].number_of_edges())],
            ["F5", "Participa.br","friendship","no","the friendship network of a brazilian federal social participation portal",str(F[4].number_of_nodes()),str(F[4].number_of_edges())],
            ["I1", "Facebook","interaction","yes","the interaction network of the Silicon Valley Global Network group",str(F[5].number_of_nodes()),str(F[5].number_of_edges())],
            ["I2", "Facebook","interaction","yes","the interaction network of a Solidarity Economy group",str(F[6].number_of_nodes()),str(F[6].number_of_edges())],
            ["I3", "Facebook","interaction","yes","the interaction network of a brazilian direct democracy group",str(F[7].number_of_nodes()),str(F[7].number_of_edges())],
            ["I4", "Facebook","interaction","yes","the interaction network of the 'Cience with Frontiers' group",str(F[8].number_of_nodes()),str(F[8].number_of_edges())],
            ["I5", "Participa.br","interaction","yes","the interaction network of a brazilian federal social participation portal",str(F[9].number_of_nodes()),str(F[9].number_of_edges())],
            ["TT1", "Twitter","retweet","yes","the retweet network of $\\approx 22k$ tweets with the hashtag \#arenaNETmundial",str(F[10].number_of_nodes()),str(F[10].number_of_edges())],
            ["TT2", "Twitter","retweet","yes","same as TT1, but disconnected agents are not discarded",str(F[11].number_of_nodes()),str(F[11].number_of_edges())]]
    data_=[i[1:] for i in data]
    tstring3=P.mediaRendering.tables.makeTabular(labels_,data_)
    P.mediaRendering.tables.writeTex(tstring3,final_path+"tabExtraNEW.tex")


def evolutionTimelines(client, final_path=os.path.dirname(__file__)+'/../../../../stabilityInteraction/figs/', pickledir=os.path.dirname(__file__)+'/../../../pickledir/'):
    sizes=[50,100,250,500,1000,3300,9900]
    # make sectorialization for each size for LAD and CPP networks
    # make plot with them
    order = 'LAD', 'CPP'
    nes = {}
    ans = input('try to reload evolution structures for timelines? (Y/n)')
    if ans == 'n' or not os.path.isfile(pickledir+'evolutionStructuresTimeline.pickle'):
        for alist in order:
            nes[alist] = []
            q = '''select distinct ?message ?participant where {
                   ?message po:author ?participant .
                   ?message po:createdAt ?date .
                   ?message po:snapshot ?snap .
                   ?snap po:gmaneID "%s" } ORDER BY ?date''' % (lacronyms[alist],) 
            from_ = pl(client.retrieveQuery(prefix+q))
            q = '''select ?message ?rmessage where {
                   ?rmessage po:createdAt ?date .
                   ?rmessage po:replyTo ?message .
                   ?rmessage po:snapshot ?snap .
                   ?snap po:gmaneID "%s" } ORDER BY ?date''' % (lacronyms[alist],) 
            replies = pl(client.retrieveQuery(prefix+q))
            for size in sizes:
                if size >= 250:
                    step_size = size
                else:
                    step_size = 200
                ne = P.measures.evolution.networkEvolution.NetworkEvolution(window_size=size, step_size=step_size)
                ne.load(from_, replies)
                ne.evolve(pca=False)
                nes[alist].append(ne)
        P.utils.pDump(nes, pickledir+'evolutionStructuresTimeline.pickle')
    else:
        nes = P.utils.pRead(pickledir+'evolutionStructuresTimeline.pickle')
    for alist in nes:
        for ne in nes[alist]:
            et = P.mediaRendering.figures.EvolutionTimelines(alist, ne, final_path=final_path)
            if ne.window_size == 1000:
                et.plotSingles()



def pcaTables(client, final_path=os.path.dirname(__file__)+'/../../../../stabilityInteraction/tables/', pickledir=os.path.dirname(__file__)+'/../../../pickledir/'):
    VE1=[]
    VE2=[]
    VE3=[]
    VA1=[]
    VA2=[]
    VA3=[]
    labels1=["$cc$","$k$","$bt$","$\\lambda$"]
    labels2=["$cc$","$s$","$s^{in}$","$s^{out}$",
             "$k$","$k^{in}$","$k^{out}$","$bt$","$\\lambda$"]
    labels3=["$cc$","$s$","$s^{in}$","$s^{out}$",
             "$k$","$k^{in}$","$k^{out}$","$bt$",
             "$asy$", "$\\mu^{asy}$","$\\sigma^{asy}$",
             "$dis$","$\\mu^{dis}$","$\\sigma^{dis}$","$\\lambda$"]
    # from networkEvolution function in this file
    nes = P.utils.pRead(pickledir+'evolutionStructures.pickle')
    # for lid, ne in zip(dl.downloaded_lists, NEs):
    for alist in order:
        ne = nes[alist]
        evec1 = n.abs(n.array([pca.pca1.eig_vectors_ for pca in ne.networks_pcas]))
        evec2 = n.abs(n.array([pca.pca2.eig_vectors_ for pca in ne.networks_pcas]))
        evec3 = n.abs(n.array([pca.pca3.eig_vectors_ for pca in ne.networks_pcas]))
        eval1 = n.abs(n.array([ pca.pca1.eig_values_ for pca in ne.networks_pcas]))
        eval2 = n.abs(n.array([ pca.pca2.eig_values_ for pca in ne.networks_pcas]))
        eval3 = n.abs(n.array([ pca.pca3.eig_values_ for pca in ne.networks_pcas]))

        VE1.append(evec1)
        VE2.append(evec2)
        VE3.append(evec3)

        VA1.append(eval1)
        VA2.append(eval2)
        VA3.append(eval3)

        m1 = evec1.mean(0)
        s1 = evec1.std(0)
        m1_ = eval1.mean(0)
        s1_ = eval1.std(0)

        m2 = evec2[:,:,:3].mean(0)
        s2 = evec2[:,:,:3].std(0)
        m2_ = eval2[:,:3].mean(0)
        s2_ = eval2[:,:3].std(0)

        m3 = evec3[:,:,:3].mean(0)
        s3 = evec3[:,:,:3].std(0)
        m3_ = eval3[:,:3].mean(0)
        s3_ = eval3[:,:3].std(0)

        # make table with each mean and std
        #t1=n.zeros((m1.shape[0],6))
        #t1[:,::2]=m1
        #t1[:,1::2]=s1
        #t1_=n.zeros(6)
        #t1_[::2]=m1_
        #t1_[1::2]=s1_
        #tab_data=n.vstack((t1,t1_))
        label = alist
        tstring = P.mediaRendering.tables.pcaTable(labels1, m1, s1, m1_, s1_)
        P.mediaRendering.tables.writeTex(tstring,final_path+"tabPCA1{}NEW.tex".format(label))
        tstring = P.mediaRendering.tables.pcaTable(labels2, m2, s2, m2_, s2_)
        P.mediaRendering.tables.writeTex(tstring,final_path+"tabPCA2{}NEW.tex".format(label))
        tstring = P.mediaRendering.tables.pcaTable(labels3,m3,s3,m3_,s3_)
        P.mediaRendering.tables.writeTex(tstring,final_path+"tabPCA3{}NEW.tex".format(label))
        if alist == 'LAU':
            ns = ne.networks_sectorializations[13]
            ne.networks_pcas[13].pca3.plotSym(ns, final_path+'../figs/', 'im13PCAPLOTNEW.png')
def networksEvolution(client, pickledir=os.path.dirname(__file__)+'/../../../pickledir/'):
    # get all interactions
    ans = input('try to reload evolution structures? (Y/n)')
    if ans == 'n' or not os.path.isfile(pickledir+'evolutionStructures.pickle'):
        nes = {}
        for alist in order:
            # q = '''select distinct ?from ?message where {
            #        ?message po:createdAt ?date .
            #        ?message po:author ?from .
            #        ?snap po:gmaneID "%s" } ORDER BY ?date''' % (lacronyms[alist],) 
            # from_msg = pl(client.retrieveQuery(prefix+q))
            q = '''select distinct ?message ?participant where {
                   ?message po:author ?participant .
                   ?message po:createdAt ?date .
                   ?message po:snapshot ?snap .
                   ?snap po:gmaneID "%s" } ORDER BY ?date''' % (lacronyms[alist],) 
            from_ = pl(client.retrieveQuery(prefix+q))
            q = '''select ?message ?rmessage where {
                   ?rmessage po:createdAt ?date .
                   ?rmessage po:replyTo ?message .
                   ?rmessage po:snapshot ?snap .
                   ?snap po:gmaneID "%s" } ORDER BY ?date''' % (lacronyms[alist],) 
            replies = pl(client.retrieveQuery(prefix+q))
            # instantiate evolutive class
            ne = P.measures.evolution.networkEvolution.NetworkEvolution(window_size=1000, step_size=1000)
            ne.load(from_, replies)
            ne.evolve()
            nes[alist] = ne
            print('evolved '+alist)
        P.utils.pDump(nes, pickledir+'evolutionStructures.pickle')
    else:
        nes = P.utils.pRead(pickledir+'evolutionStructures.pickle')
    # send interactions to evolutive class
    # evolutive class makes networks and takes measures
    return nes


def authorsTable(client, final_path=os.path.dirname(__file__)+'/../../../../stabilityInteraction/tables/', pickledir=os.path.dirname(__file__)+'/../../../pickledir/'):
    ans = input('try to reload authors statistics? (Y/n)')
    if ans == 'n' or not os.path.isfile(pickledir+'authorsStatistics.pickle'):
        stats = {}
        for alist in order:
            q = '''select distinct ?author (COUNT(distinct ?message) as ?cmessage) where {
            ?message po:author ?author .
            ?message a po:EmailMessage .
            ?message po:snapshot ?snap .
            ?snap po:gmaneID "%s" } GROUP BY ?author''' % (lacronyms[alist],)
            authors_messages = pl(client.retrieveQuery(prefix+q))
            stats[alist] = P.measures.authors.authorsStatistics.AuthorsStatistics(authors_messages)
        P.utils.pDump(stats, pickledir+'authorsStatistics.pickle')
    else:
        stats = P.utils.pRead(pickledir+'authorsStatistics.pickle')
    data_ = []
    for i in order:
        ae = stats[i]
        h_act = "{:.2f}".format(ae.n_msgs_h_)
        q1 = "{:.2f} ({:.2f}\\%)".format(ae.q1_*100, ae.Mq1*100)
        q3 = "{:.2f} ({:.2f}\\%)".format(ae.q3_*100, ae.Mq3*100)
        last_d10 = "{:.2f} (-{:.2f}\\%)".format(ae.last_d10_*100, ae.Mlast_d10*100)
        data_.append([h_act, q1, q3, last_d10])
    tstring = P.mediaRendering.tables.makeTabular(order, data_, True)
    P.mediaRendering.tables.writeTex(tstring, final_path+"userTabNEW.tex")
    return stats


def circularTables(client, final_path=os.path.dirname(__file__)+'/../../../../stabilityInteraction/tables/', pickledir=os.path.dirname(__file__)+'/../../../pickledir/'):
    # get datetimes from sent
    # try toPython
    # send array of datetimes to
    # temporalStatistics
    # save result insto pickledir
    # ask if open from pickledir or process all again
    ans = input('try to reload temporal statistics? (Y/n)')
    if ans == 'n' or not os.path.isfile(pickledir+'temporalStatistics.pickle'):
        stats = {}
        for alist in order:
            q = """select distinct ?message ?date where { ?message po:createdAt ?date .
            ?message po:snapshot ?snap .
            ?snap po:gmaneID '%s' . }""" % (lacronyms[alist],)
            dates = [i[0] for i in pl(client.retrieveQuery(prefix+q))]
            dates_ = [dateutil.parser.parse(date) for date in dates]
            stats[alist] = P.measures.time.temporalStatistics.TemporalStatistics(dates_)
        P.utils.pDump(stats, pickledir+'temporalStatistics.pickle')
    else:
        stats = P.utils.pRead(pickledir+'temporalStatistics.pickle')

    def circMeasures(tdict,mean=True):
        if mean:
           return [tdict["circular_measures"]["circular_mean"],
                tdict["circular_measures"]["std_unity_radius"],
                tdict["circular_measures"]["variance_unity_radius"],
                tdict["circular_measures"]["circular_dispersion"],
                tdict["max_discrepancy"],
                tdict["max_discrepancy_"][0],
                tdict["max_discrepancy_"][1],
            ]
        else:
           return ["--//--",
                tdict["circular_measures"]["std_unity_radius"],
                tdict["circular_measures"]["variance_unity_radius"],
                tdict["circular_measures"]["circular_dispersion"],
                tdict["max_discrepancy"],
                tdict["max_discrepancy_"][0],
                tdict["max_discrepancy_"][1],
            ]

    labels_=["seconds","minutes","hours","weekdays","month days","months"]
    for alist in order:
        data_=[]
        data_.append(circMeasures(stats[alist].seconds,False))
        data_.append(circMeasures(stats[alist].minutes,False))
        data_.append(circMeasures(stats[alist].hours))
        data_.append(circMeasures(stats[alist].weekdays))
        data_.append(circMeasures(stats[alist].monthdays))
        data_.append(circMeasures(stats[alist].months))
        tstring = P.mediaRendering.tables.makeTabular(labels_, data_, True)
        P.mediaRendering.tables.writeTex(tstring, final_path+"tab2TimeNEW{}.tex".format(alist))
    # hours along the days table
    row_labels=["{}h".format(i) for i in range(24)]
    for alist in order:
        ts = stats[alist]
        hi = 100*ts.hours["histogram"]/ts.hours["histogram"].sum()
        tstring = P.mediaRendering.tables.partialSums(row_labels,data=[hi],partials=[1,2,3,4,6,12],partial_labels=["1h","2h","3h","4h","6h","12h"])
        P.mediaRendering.tables.writeTex(tstring, final_path+"tabHours{}NEW.tex".format(alist))
    # days along the week
    data_=[100*stats[i].weekdays["histogram"]/stats[i].weekdays["histogram"].sum() for i in order]
    labels_=["LAU","LAD","MET","CPP"]
    tstring=P.mediaRendering.tables.makeTabular(labels_, data_, True)
    P.mediaRendering.tables.writeTex(tstring, final_path+"tabWeekdaysNEW.tex")
    # days of the month
    row_labels=["{}".format(i+1) for i in range(30)]
    for i in order:
        ts = stats[i]
        hi = 100*ts.monthdays["histogram"]/ts.monthdays["histogram"].sum()
        tstring = P.mediaRendering.tables.partialSums(row_labels, data=[hi], partials=[1,5,10,15], partial_labels=["1 day","5","10","15 days"])
        P.mediaRendering.tables.writeTex(tstring, final_path+"tabMonthdays{}NEW.tex".format(i))
    # months of the year
    row_labels=["Jan","Fev","Mar","Apr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    for i in order:
        ts = stats[i]
        hi = 100*ts.months["histogram"]/ts.months["histogram"].sum()
        tstring = P.mediaRendering.tables.partialSums(row_labels, data=[hi], partials=[1,2,3,4,6], partial_labels=["m.","b.","t.","q.","s."])
        P.mediaRendering.tables.writeTex(tstring, final_path+"tabMonths{}NEW.tex".format(i))
    return stats

def outlineTable(client, final_path='../../stabilityInteraction/tables/'):
    # for each of the four snapshots, get
    # date of first and last message
    # number of participants
    # number of threads
    # missing messages is 20000 - total messages
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
    table = P.mediaRendering.tables.makeTabular(order, data)
    P.mediaRendering.tables.writeTex(table, final_path+'tab1Overview.tex')
    return locals()


