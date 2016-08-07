import collections as c, numpy as n
class AuthorsStatistics:
    def __init__(self, authors_messages):
        self.author_messages_= author_messages_= c.OrderedDict(sorted(authors_messages, key=lambda x: x[1]))
        self.n_authors=len(author_messages_)

        self.authors=list(author_messages_.keys())
        # self.msgs=list(author_messages_.values())

        self.authors_n_msgs = n.array(list(author_messages_.values()))

        self.basicMeasures()
        self.messageAuthorsCorrespondence()
    def basicMeasures(self):
        self.mean_msgs=n.mean(self.authors_n_msgs)
        self.std_msgs=n.std(self.authors_n_msgs)
        plist=[5,10,25,50,75,90,95]
        self.percentiles=percentiles={}
        for percentile in plist:
            percentiles[percentile]=n.percentile(self.authors_n_msgs,plist)

    def oneMore(self,bool_array):
        args=n.nonzero(bool_array-1)[0]
        bool_array[args[0]]=True
        return bool_array
    def oneLess(self,bool_array):
        args=n.nonzero(bool_array-1)[0]
        bool_array[args[-1]]=True
        return bool_array
    def messageAuthorsCorrespondence(self):
        self.n_msgs_h=self.authors_n_msgs[-1]
        self.n_msgs_h_=100*self.n_msgs_h/sum(self.authors_n_msgs)
        self.cumulative=n.array([n.sum(self.authors_n_msgs[:i+1]) for i in range(self.n_authors)])
        self.cumulative_=self.cumulative/sum(self.authors_n_msgs)
        self.last_d10=1+(self.cumulative_<.10).sum()
        self.last_d10_=self.last_d10/self.n_authors
        self.q1=1+(self.cumulative_>0.75).sum()
        self.q1_=self.q1/self.n_authors
        self.q3=1+(self.cumulative_>0.25).sum()
        self.q3_=self.q3/self.n_authors

        self.Mlast_d10 =self.authors_n_msgs[self.oneMore(self.cumulative_<0.10)].sum()/sum(self.authors_n_msgs)

        self.Mq1=self.authors_n_msgs[self.oneLess(self.cumulative_>0.75)].sum()/sum(self.authors_n_msgs)

        self.Mq3=self.authors_n_msgs[self.oneLess(self.cumulative_>0.25)].sum()/sum(self.authors_n_msgs)

