import pylab as p, matplotlib, os, pickle
from percolation.analysis.sectorialize import *

class EvolutionTimelines:
    # def __init__(self,tdir="./evolution/",label="gmaneID",draw=True):
    def __init__(self, label="gmaneID", network_evolution='ne_instance', draw=True, final_path='./evolution/'):
        # self.tdir=tdir
        self.network_evolution = network_evolution
        self.label = label
        self.final_path = final_path
        self.getMeasures()
        if draw:
            self.drawTimelines()
    # def getOverallMeasures(self):
    #     filenames=os.listdir(self.tdir)
    #     filenames_=[i for i in filenames if i.endswith(".pickle")]
    #     filename=[i for i in filenames_ if "overall" in i][0]
    #     with open(self.tdir+filename,"rb") as f:
    #             self.overall=pickle.load(f)
    def getMeasures(self):
        # self.getOverallMeasures()
        # filenames=os.listdir(self.tdir)
        # filenames_=[i for i in filenames if i.endswith(".pickle")]
        # filenames_=[i for i in filenames_ if i.startswith("im")]
        # filenames_.sort()
        agents={"s":[],"is":[],"os":[],
                "d":[],"id":[],"od":[],
                "exc":[],"excc":[],"exce":[],
                "inc":[],"incc":[],"ince":[],
                "nm":[],"totals":[]}
        # for filename in filenames_:
        #     with open(self.tdir+filename,"rb") as f:
        #         data=pickle.load(f)
        for i, net in enumerate(self.network_evolution.networks):
                # nm=data["nm"]
                nm = self.network_evolution.networks_measures[i]
                agents["nm"].append(nm)
                n_agents = nm.N
                agents["totals"].append(n_agents)
                # minimum_incidence=data["np"].minimum_incidence
                minimum_incidence = self.network_evolution.networks_sectorializations[i].minimum_incidence
                # agents["s"].append(data["np"].sectorialized_agents__)
                agents["s"].append(self.network_evolution.networks_sectorializations[i].sectorialized_agents__)
                agents["is"].append(
                        NetworkSectorialization(nm,minimum_incidence=minimum_incidence,metric="is").sectorialized_agents__ )
                agents["os"].append(
                        NetworkSectorialization(nm,minimum_incidence=minimum_incidence,metric="os").sectorialized_agents__ )
                agents["d"].append(
                        NetworkSectorialization(nm,minimum_incidence=minimum_incidence,metric="d").sectorialized_agents__ )
                agents["id"].append(
                        NetworkSectorialization(nm,minimum_incidence=minimum_incidence,metric="id").sectorialized_agents__ )
                agents["od"].append(
                        NetworkSectorialization(nm,minimum_incidence=minimum_incidence,metric="od").sectorialized_agents__ )
                # pegar os agentes da rede em
                # todos os outros critérios de particionamento simples:
                # d, id, od, is, os
                # e mandar eles para uma função que já calcula
                # os particionamentos compostos
                compound = compoundSectorialization(agents)
                agents["exc"].append(compound["exc"])
                agents["excc"].append(compound["excc"])
                agents["exce"].append(compound["exce"])
                agents["inc"].append(compound["inc"])
                agents["incc"].append(compound["incc"])
                agents["ince"].append(compound["ince"])
        self.agents = agents
    def plotFracs(self,ttype,subplot,ate,step_size, intext=False):
        p.subplot(subplot)
        p.title(ttype)
        if ttype == "degree": ttype_="d"
        if ttype == "strength": ttype_="s"
        if ttype == "in-degree": 
            ttype_="id"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "out-degree": ttype_="od"
        if ttype == "in-strength": 
            ttype_="is"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "out-strength": ttype_="os"
        if ttype == "exclusivist":
            ttype_="exc"
            not_classified=list([1-sum(self.fractionLengths(i,total)) 
                for i,total in zip(self.agents[ttype_],self.agents["totals"])])
            # p.plot(list(range(0,ate,step_size))[:-1],not_classified,"k-.x")
            if intext:
                p.plot(list(range(0,ate,step_size)), not_classified,"k-.x")
            else:
                p.plot(list(range(0,ate,step_size)), not_classified,"k")
        if ttype == "inclusivist":
            ttype_="inc"
            super_classified=list([sum(self.fractionLengths(i,total))-1 for i,total in zip(self.agents[ttype_],self.agents["totals"])])
            # p.plot(list(range(0,ate,step_size))[:-1],super_classified,"k-.x")
            if intext:
                p.plot(list(range(0, ate, step_size)), super_classified,"k-.x")
            else:
                p.plot(list(range(0, ate, step_size)), super_classified,"k")
        if ttype == "exclusivist cascade": 
            ttype_="excc"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "inclusivist cascade": 
            ttype_="incc"
            p.ylabel(r"fraction of nodes in each section $\rightarrow$")
        if ttype == "exclusivist externals": 
            ttype_="exce"
            p.xlabel(r"messages $\rightarrow$")
        if ttype == "inclusivist externals": 
            ttype_="ince"
            p.xlabel(r"messages $\rightarrow$")
        fractions = [self.fractionLengths(i,total) for i,total in zip(self.agents[ttype_], self.agents["totals"])]
        hubs_fractions = [i[2] for i in fractions]
        intermediary_fractions = [i[1] for i in fractions]
        periphery_fractions = [i[0] for i in fractions]
        print(list(range(0,ate,step_size)),periphery_fractions)
        print(len(list(range(0,ate,step_size))),
              len(periphery_fractions))
        #p.plot(list(range(0,ate,step_size))[:-1],periphery_fractions,   "b")
        #p.plot(list(range(0,ate,step_size))[:-1],intermediary_fractions,"g")
        #p.plot(list(range(0,ate,step_size))[:-1],hubs_fractions,        "r")
        # p.plot(list(range(0,ate,step_size))[:-1],periphery_fractions,   "ko-",ms=8,alpha=.7,label="periphery")
        # p.plot(list(range(0,ate,step_size))[:-1],intermediary_fractions,"k^-",ms=8,alpha=.7,label="intermediary")
        # p.plot(list(range(0,ate,step_size))[:-1],hubs_fractions,        "k*-",ms=10,alpha=.7,label="hubs")
        if intext:
            p.plot(list(range(0,ate,step_size)), periphery_fractions,   "ko-",ms=8,alpha=.7,label="periphery")
            p.plot(list(range(0,ate,step_size)), intermediary_fractions,"k^-",ms=8,alpha=.7,label="intermediary")
            p.plot(list(range(0,ate,step_size)), hubs_fractions,        "k*-",ms=10,alpha=.7,label="hubs")
        else:
            p.plot(list(range(0,ate,step_size)), periphery_fractions,    "b")
            p.plot(list(range(0,ate,step_size)), intermediary_fractions, "g")
            p.plot(list(range(0,ate,step_size)), hubs_fractions,         "r")
        p.ylim(0,1.)
        p.xticks((0, 5000, 10000, 15000))
        # p.xlim(-5,ate-1700+100)
        p.xlim(-5, ate)
    def plotMeasure(self,title,subplot,ate,step_size):
        if subplot=="5,2,10":
            p.subplot(5,2,10)
        else:
            p.subplot(subplot)
        p.title(title)
        if title=="total weight":
            measures=[sum([i[2]["weight"] for i in nm.edges])
                    for nm in self.agents["nm"]]
            p.ylabel(r"$\sum s_i \;\;\rightarrow$")
        elif title=="number of edges":
            measures=[i.E for i in self.agents["nm"]]
            #p.ylabel(r"$\mathfrak{z} \rightarrow$",fontsize=20)
            p.ylabel(r"$z \rightarrow$",fontsize=20)
        elif title=="number of vertices":
            measures=[i.N for i in self.agents["nm"]]
            p.xlabel(r"messages $\rightarrow$")
            p.ylabel(r"N $\rightarrow$")
        elif title=="center, periphery and discon.":
            center=[len(i.center) for i in self.agents["nm"]]
            p.plot(range(0,ate,step_size),center,"b")
            periphery=[len(i.periphery) for i in self.agents["nm"]]
            p.plot(range(0,ate,step_size),periphery,"k",linestyle="dashed")
            periphery_=[len(i.periphery_) for i in self.agents["nm"]]
            measures=[i+j for i,j in zip(periphery,periphery_)]
            p.xlabel(r"messages $\rightarrow$")
            p.ylabel("number of\nnodes"+r"$\rightarrow$")

        p.plot(range(0,ate,step_size),measures,"k")
        p.ylim(min(measures)*.99,max(measures)*1.01)
        p.xlim(-5,ate+5)

    def plotSingles(self):
        #p.clf()
        #fig = matplotlib.pyplot.gcf()
        #fig.set_size_inches(10.5,3.4) ###
        p.figure(figsize=(10.,4.))
        #ate=self.overall[1][0].n_messages-self.overall[0]["window_size"]
        # ate=self.overall[1][0].n_messages
        ate = 20000 - self.network_evolution.window_size
        # step_size=self.overall[0]["step_size"]
        step_size = self.network_evolution.step_size
        p.suptitle(r"Empirical fractions of participants in each of the Erdös sectors")
        #p.suptitle((r"Fraction of participants in each Erdös Sector. Window: %i messages."+"\nPlacement resolution: %i messages. %s") % (self.overall[0]["window_size"],step_size,self.label))

        self.plotFracs("degree",     "221",ate,step_size, intext=True)
        p.ylabel(r"$\overline{e_{1,\phi}} \;\rightarrow$",fontsize=20)
        self.plotFracs("strength",   "223",ate,step_size, intext=True)
        p.ylabel(r"$\overline{e_{4,\phi}} \;\rightarrow$",fontsize=20)
        p.xlabel(r"messages $\;\rightarrow$",fontsize=15)
        self.plotFracs("exclusivist","222",ate,step_size, intext=True)
        p.ylabel(r"$\overline{c_{1,\phi}} \;\rightarrow$",fontsize=20)
        self.plotFracs("inclusivist","224",ate,step_size, intext=True)
        p.ylabel(r"$\overline{c_{2,\phi}} \;\rightarrow$",fontsize=20)
        p.xlabel(r"messages $\;\rightarrow$",fontsize=15)
        #fig.set_size_inches(5.5,16.4) ###

        p.subplots_adjust(left=0.08,bottom=0.13,right=0.99,top=0.79,wspace=0.23,hspace=0.47)

        p.plot([],[],        "k-.x",label="without sector or ambiguous")
        p.legend(bbox_to_anchor=(-0.98, 2.7, 1.75, .1), loc=4,
                           ncol=4, mode="expand", borderaxespad=0.,fontsize=10,frameon=False)
        # filename="InText-W{}-S{}NEW.png".format(self.label,self.overall[0]["window_size"],step_size)
        filename="InText-W{}-S{}NEW.png".format(self.label, self.network_evolution.window_size, step_size)
        # legenda no superior direito
        tname="{}{}".format(self.final_path, filename)
        p.savefig(tname)
        print("written image file:", tname)
        #p.show()
    def plotFirstPage(self):
        p.clf()
        fig = matplotlib.pyplot.gcf()
        # fig.set_size_inches(7.,8.4)
        fig.set_size_inches(7.,5.4)
        # step_size=self.overall[0]["step_size"]
        step_size = self.network_evolution.step_size
        window_size = self.network_evolution.window_size
        # ate=self.overall[1][0].n_messages-self.overall[0]["window_size"]
        ate = 20000-window_size
        # p.suptitle("Primary divisions. Window: %i messages.\nPlacement resolution: %i messages. %s" % (self.overall[0]["window_size"],step_size,self.label))
        p.suptitle("Simple sectorializations. Window: %i messages.\nPlacement resolution: %i messages. %s" % (window_size, step_size, self.label))
        self.plotFracs("degree","321",ate,step_size)
        self.plotFracs("strength","322",ate,step_size)
        self.plotFracs("in-degree","323",ate,step_size)
        self.plotFracs("in-strength","324",ate,step_size)
        self.plotFracs("out-degree","325",ate,step_size)
        self.plotFracs("out-strength","326",ate,step_size)
        # self.plotMeasure("total weight","527",ate,step_size)
        # self.plotMeasure("number of edges","528",ate,step_size)
        # self.plotMeasure("number of vertices","529",ate,step_size)
        # self.plotMeasure("center, periphery and discon.","5,2,10",ate,step_size)
        # p.subplots_adjust(left=0.105,bottom=0.05,right=0.98,top=0.9,wspace=0.28,hspace=0.69)
        p.subplots_adjust(left=0.09,bottom=0.08,right=0.99,top=0.86,wspace=0.28,hspace=0.55)
        filename="{}-W{}-S{}NEW.png".format(self.label, window_size,step_size)
        p.savefig("{}{}".format(self.final_path, filename))
        # simple plot:
        p.clf()
        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(7.,5.4)
        # p.suptitle("Compound divisions. Window: %i messages.\nPlacement resolution: %i messages. %s" % (self.overall[0]["window_size"],step_size,self.label))
        p.suptitle("Compound sectorializations. Window: %i messages.\nPlacement resolution: %i messages. %s" % (window_size, step_size, self.label))
        self.plotFracs("exclusivist","321",ate,step_size)
        self.plotFracs("inclusivist","322",ate,step_size)
        self.plotFracs("exclusivist cascade","323",ate,step_size)
        self.plotFracs("inclusivist cascade","324",ate,step_size)
        self.plotFracs("exclusivist externals","325",ate,step_size)
        self.plotFracs("inclusivist externals","326",ate,step_size)
        p.subplots_adjust(left=0.09,bottom=0.08,right=0.99,top=0.86,wspace=0.28,hspace=0.55)
        filename="{}-W{}-S{}_NEW.png".format(self.label, window_size, step_size)
        p.savefig("{}{}".format(self.final_path, filename))

    def drawTimelines(self):
        self.plotFirstPage()

    def fractionLengths(self,list_of_lists,total):
        llist=[len(i) for i in list_of_lists]
        return [i/total for i in llist]
