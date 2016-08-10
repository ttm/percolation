import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl
from percolation.rdf import prefix
import os
import dateutil.parser
import numpy as n
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
lacronyms = {'LAU': "gmane.linux.audio.users",
             'CPP': "gmane.comp.gcc.libstdc++.devel",
             'MET': "gmane.politics.organizations.metareciclagem",
             'LAD': "gmane.linux.audio.devel"}
order = ['LAU', 'LAD', 'MET', 'CPP']

# def circularTable(client, final_path='../../../stabilityInteraction/tables/', pickledir='../../../pickledir/'):
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


