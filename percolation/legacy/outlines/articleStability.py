import percolation as P
from percolation.rdf.sparql.functions import plainQueryValues as pl
from percolation.rdf import prefix
import os
import dateutil.parser
prefix = 'PREFIX po: <http://purl.org/socialparticipation/po/>\n'
lacronyms = {'LAU': "gmane.linux.audio.users",
             'CPP': "gmane.comp.gcc.libstdc++.devel",
             'MET': "gmane.politics.organizations.metareciclagem",
             'LAD': "gmane.linux.audio.devel"}
order = ['LAU', 'LAD', 'MET', 'CPP']

# def circularTable(client, final_path='../../../stabilityInteraction/tables/', pickledir='../../../pickledir/'):
def authorsTable(client, final_path=os.path.dirname(__file__)+'/../../../../stabilityInteraction/tables/', pickledir=os.path.dirname(__file__)+'/../../../pickledir/'):
    ans = input('try to reload authors statistics? (Y/n)')
    if ans == 'n' or not os.path.isfile(pickledir+'authorsStatistics.pickle'):
        stats = {}
        for alist in order:
            q = '''PREFIX po: <http://purl.org/socialparticipation/po/> 
            select distinct ?author (COUNT(distinct ?message) as ?cmessage) where {
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


