import numpy as n, pylab as p, matplotlib
from scipy import stats

class NetworkPCA:
    """PCA cases of interest  for observing stability in interaction networks.

        1) Primacy of centrality measures for dispersion; and
        2) precedence of symmetry over clustering;
        3) average of all basic centrality measures for first compoment
    """
    def __init__(self,network_measures,network_partitioning=None,tdir=".",tname="sample.png", measures="all",plot_sym=False):
        # enable selection of measures input as string
        # through measures variable and exec() or eval() methods.
        self.M1=n.array(( network_measures.weighted_clusterings_,
                    network_measures.degrees_,
                    network_measures.weighted_directed_betweenness_
                    ))
        self.pca1=PCA(self.M1)
        if "in_strengths_" in dir(network_measures):
            self.M2=n.array(( network_measures.weighted_clusterings_,
                        network_measures.strengths_,
                        network_measures.in_strengths_,
                        network_measures.out_strengths_,
                        network_measures.degrees_,
                        network_measures.in_degrees_,
                        network_measures.out_degrees_,
                        network_measures.weighted_directed_betweenness_
                        ))
            self.M3=n.array(( network_measures.weighted_clusterings_,
                        network_measures.strengths_,
                        network_measures.in_strengths_,
                        network_measures.out_strengths_,
                        network_measures.degrees_,
                        network_measures.in_degrees_,
                        network_measures.out_degrees_,
                        network_measures.weighted_directed_betweenness_,
                        network_measures.asymmetries,
                        network_measures.asymmetries_edge_mean,
                        network_measures.asymmetries_edge_std,
                        network_measures.disequilibriums,
                        network_measures.disequilibrium_edge_mean,
                        network_measures.disequilibrium_edge_std,
                        ))
            self.pca2=PCA(self.M2)
            self.pca3=PCA(self.M3)
        if plot_sym:
            self.pca3.plotSym(network_partitioning,tdir,tname)
#            fig = matplotlib.pyplot.gcf()
#            fig.set_size_inches(11.,8.4)
#            p.suptitle("Symmetry prevalence over clutering for data dispersion")
#            p.subplot(311)
#            # plot degree x clust
#            p.title("degree x clustering")
#            label1=r"degree $\rightarrow$"
#            label2=r"clustering $\rightarrow$"
#            p.xlabel(label1, fontsize=15)
#            p.ylabel(label2, fontsize=15)
#            n_periphery=   len(network_partitioning.sectorialized_agents__[0])
#            n_intermediary=len(network_partitioning.sectorialized_agents__[1])
#            n_hubs=        len(network_partitioning.sectorialized_agents__[2])
#            M=n.array(network_measures.degrees_)
#            network_measures.degrees__=(M-M.mean())/M.std()
#            M=n.array(network_measures.weighted_clusterings_)
#            network_measures.weighted_clusterings__=(M-M.mean())/M.std()
#            p.ylim(min(network_measures.weighted_clusterings__)-1,max(network_measures.weighted_clusterings__)+1)
#            p.xlim(min(network_measures.degrees__)-1,max(network_measures.degrees__)+1)
#            p.plot(network_measures.degrees__[:n_periphery],network_measures.weighted_clusterings__[:n_periphery],"ko", ms=3.9,label="periphery")
#
#            p.plot(network_measures.degrees__[n_periphery:n_periphery+n_intermediary],network_measures.weighted_clusterings__[n_periphery:n_periphery+n_intermediary],"k^", ms=3.9,label="intermediary")
#
#            p.plot(network_measures.degrees__[-n_hubs:],network_measures.weighted_clusterings__[-n_hubs:],"k*", ms=3.9,label="hubs")
#
#            #p.subplot(312)
#            #self.pca2.plot(None,network_partitioning,labels=None,tdir=None,savefig=False,clear_fig=False,title="Vertices in principal components",label1=r"PC1 - degrees and strengths",label2=r"PC3 - clustering")
#            p.subplot(212)
#            self.pca3.plot(None,network_partitioning,labels=None,tdir=None,savefig=False,clear_fig=False,title="Vertices in principal components",label1=r"PC1 - degrees and strengths",label2="PC2 - symmetry")
#            p.subplots_adjust(left=0.08,bottom=0.12,right=0.97,top=0.88,wspace=0.13,hspace=0.88)
#            p.show()
#            #p.savefig("{}/{}".format(tdir,tname))
        elif network_partitioning:
            self.pca1.plot(tname.replace(".","_1."),network_partitioning,tdir=tdir)
            self.pca2.plot(tname.replace(".","_2."),network_partitioning,tdir=tdir)
            self.pca3.plot(tname.replace(".","_3."),network_partitioning,tdir=tdir)


class PCA:
    """Apply PCA to incoming datatable M (metrics x observations)

    Usage
    =====

    Initialize with a n x m matrix of n metrics each with m observations
    >>> foo=n.random(100)
    >>> p1=n.vstack((foo,foo))
    >>> p2=n.vstack((-foo,foo))
    >>> p3=n.vstack((foo,-foo))
    >>> M=n.hstack((p1,p2,p3))
    >>> pca=g.PCA(M)

    See attributes for information about data:
    >>> pca.eig_values # for eigen values from greatest down
    >>> pca.eig_values_ # for a normalized eig_values
    >>> pca.eig_vectors # for eigen vectors of the eig_values
    >>> pca.eig_vectors_ # for a normalized eig_vectors
    >>> pca.C # for covariance matrix
    >>> pca.M # for initial data 
    >>> pca.x # final positions in the principal component
    >>> pca.y # final positions in second principal component
    >>> pca.plot() # to plot observations in initial and final spaces
    

    """
    def __init__(self,*metrics,final_dimensions=2,draw=False):
        M=n.vstack(metrics)
        # zscore: # USE NUMPY.stats.zscore(M, axis=1, ddof=1)
        self.M_=n.copy(M)
        for i in range(M.shape[0]):
            if M[i].std():
                M[i]=(M[i]-M[i].mean())/M[i].std()
            else:
                M[i]=0.
        # convariance matrix:
        self.C=n.cov(M,bias=1)
        self.M=M

        eig_values, eig_vectors = n.linalg.eig(self.C)
        # Ordering eigenvalues and eigenvectors
        args=n.argsort(eig_values)[::-1]
        self.eig_values=eig_values[args]
        self.eig_values_=100*self.eig_values/n.sum(n.abs(self.eig_values))
        self.eig_vectors=eig_vectors[:,args]
        self.eig_vectors_=n.array([100*self.eig_vectors[:,i]/n.abs(self.eig_vectors[:,i]).sum() for i in range(self.eig_vectors.shape[1])]).T
        # retaining only some eigenvectors
        self.feature_vec=self.eig_vectors[:,:final_dimensions]
        self.feature_vec_=n.array([100*self.feature_vec[:,i]/n.abs(self.feature_vec[:,i]).sum() for i in range(self.feature_vec.shape[1])]).T

        self.final_data=n.dot(M.T,self.feature_vec)
        self.x=self.final_data[:,0]
        self.y=self.final_data[:,1]
    #def plot(self, tname="sample.png", network_partitioning=False,labels="full", tdir=".",savefig=True,clear_fig=True,title="Vertex plot in principal components (PCA)",label1="PC1",label2="PC2"):
    def plotSym(self,network_partitioning,tdir,tname):

        self.x_=self.M_[4] # degrees
        self.cc=self.M[0] #clustering 
        p.figure(figsize=(7.,4.))
        p.subplots_adjust(left=0.09,bottom=0.16,right=0.95,top=0.87,hspace=0.04)
        #fig = matplotlib.pyplot.gcf()
        #fig.set_size_inches(6.,8.4)
        #p.suptitle("Symmetry-related measures and clutering coefficient along connectivity")
        kl=max(network_partitioning.sectorialized_degrees__[0])+.5
        kr=max(network_partitioning.sectorialized_degrees__[1])+.5
        p.suptitle("Symmetry-related and clutering coefficient components along connectivity")
        p.subplot(211)
        p.plot((kl,kl),(-1000,1000),"g--",linewidth=3)
        p.plot((kr,kr),(-1000,1000),"g--",linewidth=3)
        p.xticks((),())
            # plot degree x clust
        #label1=r"degree $\rightarrow$"
        label2=r"clustering $\rightarrow$"
        #p.xlabel(label1, fontsize=15)
        p.ylabel(label2, fontsize=15)
        n_periphery=   len(network_partitioning.sectorialized_agents__[0])
        n_intermediary=len(network_partitioning.sectorialized_agents__[1])
        n_hubs=        len(network_partitioning.sectorialized_agents__[2])
        #M=n.array(network_measures.degrees_)
        #network_measures.degrees__=(M-M.mean())/M.std() #AQUI
        #M=n.array(network_measures.weighted_clusterings_)
        #network_measures.weighted_clusterings__=(M-M.mean())/M.std()
        p.ylim(min(self.cc)-0.9,max(self.cc)+.9)
        p.xlim(min(self.x_)-0.1,max(self.x_)+.1)
        p.plot(self.x_[:n_periphery],                          self.cc[:n_periphery],"ko", label="periphery"                             ,ms=10,alpha=.4)
        p.plot(self.x_[n_periphery:n_periphery+n_intermediary],self.cc[n_periphery:n_periphery+n_intermediary],"k^", label="intermediary",ms=10,alpha=.4)
        p.plot(self.x_[n_periphery+n_intermediary:],                              self.cc[-n_hubs:],"k*", label="hubs"                                      ,ms=10,alpha=.4)
        #p.plot(self.x_[-n_hubs:],                              self.cc[-n_hubs:],"k*", label="hubs"                                      ,ms=10,alpha=.4)

        #p.legend()
        p.legend(bbox_to_anchor=(0.17, .71, .8, .2), loc=3,
                           ncol=3, mode="expand", borderaxespad=0.)
        p.subplot(212)
        p.plot((kl,kl),(-1000,1000),"g--",linewidth=3)
        p.plot((kr,kr),(-1000,1000),"g--",linewidth=3)
        p.xticks((kl,kr),(r"k_L",r"k_R"))
        p.ylabel(r"PC2 $\rightarrow$", fontsize=15)
        p.xlabel(r"degree $\rightarrow$", fontsize=15)
#        p.title("degree x symmetry-related principal component")
        #self.pca3.plot(None,network_partitioning,labels=None,tdir=None,savefig=False,clear_fig=False,title="Vertices in principal components",label1=r"PC1 - degrees and strengths",label2="PC2 - symmetry")
        #p.subplots_adjust(left=0.08,bottom=0.12,right=0.97,top=0.88,wspace=0.13,hspace=0.88)
        #p.show()
        #p.savefig("{}/{}".format(tdir,tname))
#        elifnetwork_partitioning:
#            self.pca1.plot(tname.replace(".","_1."),network_partitioning,tdir=tdir)
#            self.pca2.plot(tname.replace(".","_2."),network_partitioning,tdir=tdir)
#            self.pca3.plot(tname.replace(".","_3."),network_partitioning,tdir=tdir)
#        p.title(title)

        p.ylim(min(self.y) -0.9,max(self.y)+  0.9)
        p.xlim(min(self.x_)-0.1,max(self.x_)+0.1)
        #n_periphery=   len(network_partitioning.sectorialized_agents__[0])
        #n_intermediary=len(network_partitioning.sectorialized_agents__[1])
        #n_hubs=        len(network_partitioning.sectorialized_agents__[2])
        p.plot(self.x_[:n_periphery],self.y[:n_periphery],"ko", label="perihpery"                                                       ,ms=10,alpha=.4)
        p.plot(self.x_[n_periphery:n_periphery+n_intermediary],self.y[n_periphery:n_periphery+n_intermediary],"k^", label="intermediary",ms=10,alpha=.4)
        p.plot(self.x_[-n_hubs:],self.y[-n_hubs:],"k*", label="hubs"                                                                    ,ms=10,alpha=.4)
        #p.show()
        p.savefig("{}/{}".format(tdir,tname))

    def plot(self, tname="sample.png", network_partitioning=False,labels="full", tdir=".",savefig=True,clear_fig=True,title="Vertex plot in principal components (PCA)",label1="PC1",label2="PC2"):
        if clear_fig:
            p.clf()
        if labels=="full":
            #foo=self.feature_vec[:,0]
            #foo_=("%.2f, "*len(foo)) % tuple(foo)
            foo=self.feature_vec_[:,0]
            foo__=("%.2f, "*len(foo)) % tuple(foo)
            label1+=" " + foo__

            #foo=self.feature_vec[:,1]
            #foo_=("%.2f, "*len(foo)) % tuple(foo)
            foo=self.feature_vec_[:,1]
            foo__=("%.2f, "*len(foo)) % tuple(foo)
            label2+=" " +foo__

            #foo=(self.eig_values[:4]/self.eig_values.sum())*100
            #foo_=r"$\lambda = $"+("%.2f, "*len(foo) % tuple(foo))
            foo=(self.eig_values_[:4])
            foo__=r"$\lambda = $"+("%.2f, "*len(foo) % tuple(foo))
            title+=" "+foo__
        if labels=="sym":
            pass

        p.xlabel(label1, fontsize=15)
        p.ylabel(label2, fontsize=15)
        #p.title(foo_)
        p.title(title)

        p.ylim(min(self.y)-1,max(self.y)+1)
        p.xlim(min(self.x)-1,max(self.x)+1)
        if not network_partitioning:
            p.plot(self.x,self.y,"k^", ms=3.9,label="intermediary")
        else:
            n_periphery=   len(network_partitioning.sectorialized_agents__[0])
            n_intermediary=len(network_partitioning.sectorialized_agents__[1])
            n_hubs=        len(network_partitioning.sectorialized_agents__[2])
            p.plot(self.x[:n_periphery],self.y[:n_periphery],"k^", ms=3.9,label="perihpery")
            p.plot(self.x[n_periphery:n_periphery+n_intermediary],self.y[n_periphery:n_periphery+n_intermediary],"k*", ms=3.9,label="hubs")
            p.plot(self.x[-n_hubs:],self.y[-n_hubs:],"ro", ms=3.9,label="hubs")
        p.legend()
        if savefig:
            p.savefig("{}/{}".format(tdir,tname))
            x=self.M[0]
            y=self.M[1]
            if clear_fig:
                p.clf()
            p.plot(x,y,"go", ms=3.9,label="intermediary")
            p.savefig("{}/Initial{}.png".format(tdir,tname))
