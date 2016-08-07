import numpy as n, calendar, datetime

def circularStatistics(population, period):
    pop=n.array(population)
    pop_=pop*2*n.pi/period
    j=n.complex(0,1)
    vec_n=n.e**(j*pop_)
    mean_vec=vec_n.sum()/len(vec_n) # first moment
    mean_angle=n.arctan2(mean_vec.real,mean_vec.imag)
    size_mean_vec=n.abs(mean_vec)
    variance_unity_radius=1-size_mean_vec
    std_unity_radius=n.sqrt(-2*n.log(size_mean_vec))
    circular_mean=mean_angle*(period/(2*n.pi))
    circular_variance=variance_unity_radius*(period**2/(2*n.pi))
    circular_std=std_unity_radius*(period/(2*n.pi))

    second_moment=(vec_n**2).sum()/len(vec_n)
    size_second_moment=n.abs(second_moment)
    circular_dispersion=(1-size_second_moment)/(2*(size_mean_vec**2))

    return dict(mean_vec=mean_vec,
            mean_angle=mean_angle, 
            size_mean_vec=size_mean_vec,
            circular_mean=circular_mean, 
            circular_variance=circular_variance, 
            circular_std=circular_std, 
            variance_unity_radius=variance_unity_radius, 
            std_unity_radius=std_unity_radius,
            circular_dispersion=circular_dispersion)

class TemporalStatistics:
    def __init__(self,datetimes):
        self.datetimes=datetimes
        self.n_observations=len(datetimes)
        self.bad_datetimes=[]
        self.makeStatistics()
    def makeStatistics(self):
        """Make statistics from seconds to years"""
        self.uniformComparisson()
        self.secondsStats()
        self.minutesStats()
        self.hoursStats()
        self.weekdaysStats()
        self.monthdaysStats_()
        self.monthsStats()
        self.yearsStats()
    def uniformComparisson(self):
        ar=n.random.randint(0,60,(1000,self.n_observations))
        cc=n.array([n.histogram(i,60)[0] for i in ar])
        cc_=cc.min(1)/cc.max(1)
        self.obs60=(cc_.mean(),cc_.std())
        self.obs60_=cc_

        ar=n.random.randint(0,24,(1000,self.n_observations))
        cc=n.array([n.histogram(i,24)[0] for i in ar])
        cc_=cc.min(1)/cc.max(1)
        self.obs24=(cc_.mean(),cc_.std())
        self.obs24_=cc_

        ar=n.random.randint(0,30,(1000,self.n_observations))
        cc=n.array([n.histogram(i,30)[0] for i in ar])
        cc_=cc.min(1)/cc.max(1)
        self.obs30=(cc_.mean(),cc_.std())
        self.obs30_=cc_

        ar=n.random.randint(0,7,(1000,self.n_observations))
        cc=n.array([n.histogram(i,7)[0] for i in ar])
        cc_=cc.min(1)/cc.max(1)
        self.obs7=(cc_.mean(),cc_.std())
        self.obs7_=cc_
        
        #self.obs60=n.random.randint(0,60,(1000, self.n_observations))
        #self.count_obs60=[obs60.count(i) for i in set(obs60)]
        #self.obs24=n.random.randint(0,24,self.n_observations)
        #self.count_obs24=[obs24.count(i) for i in set(obs24)]
        # IN MONTHs function:
        #self.obs12=n.random.randint(0,12,len(self.months.samples))
        #self.obs30=n.random.randint(0,30,self.n_observations)
        #self.count_obs12=[obs12.count(i) for i in set(obs12)]
        #self.obs7=n.random.randint(0,7,self.n_observations)
        #self.count_obs12=[obs12.count(i) for i in set(obs12)]
        
    def secondsStats(self):
        # contagem para histograma
        seconds=[i.second for i in self.datetimes]
        histogram=n.histogram(seconds,bins=list(range(61)))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics(seconds,60)
        seconds=dict(
            circular_measures=circular_measures,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs60,
            samples=seconds,
            histogram=histogram)
        self.seconds=seconds

    def minutesStats(self):
        samples=[i.minute for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(61)))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics(samples,60)
        minutes=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs60,
            circular_measures=circular_measures
        )
        self.minutes=minutes


    def hoursStats(self):
        samples=[i.hour for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(25)))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics(samples,24)
        hours=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs24,
            circular_measures=circular_measures
        )
        self.hours=hours
    def weekdaysStats(self):
        samples=[i.weekday() for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(8)))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics(samples,7)
        self.weekdays=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs7,
            circular_measures=circular_measures
        )
    def monthdaysStats_(self):
        def aux(xx):
            #return (xx.day-1)/(
            #        calendar.monthrange(xx.year, xx.month)[1] )
            return ((xx.day-1)*24*60+xx.hour*60+xx.minute )/(
                    calendar.monthrange(xx.year, xx.month)[1]*24*60)
        samples=[aux(i) for i in self.datetimes]
        mean_month_size=n.mean([calendar.monthrange(xx.year, xx.month)[1]
            for xx in self.datetimes])
        mean_month_size=n.round(mean_month_size)
        histogram=n.histogram(samples,bins=n.linspace(0,1,mean_month_size+1))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics([i*mean_month_size for i in samples],mean_month_size)
        self.monthdays=dict(
            mean_month_size=mean_month_size,
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs30,
            circular_measures=circular_measures,
        )
    def monthdaysStats(self):
        def aux(xx):
            return (xx.day-1)/(
                    calendar.monthrange(xx.year, xx.month)[1] )
        samples=[aux(i) for i in self.datetimes]
        mean_month_size=n.mean([calendar.monthrange(xx.year, xx.month)[1]
            for xx in self.datetimes])
        mean_month_size=n.round(mean_month_size)
        histogram=n.histogram(samples,bins=n.linspace(0,1,mean_month_size+1))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics(samples,1)
        self.monthdays=dict(
            mean_month_size=mean_month_size,
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs30,
            circular_measures=circular_measures,
        )
    def monthsStats(self,truncate=True):
        year=365.242199 # days
        if truncate:
            delta=self.datetimes[-1]-self.datetimes[0]
            if delta.days > year:
                delta_=(delta.total_seconds()/(24*60*60))%year
                max_date=self.datetimes[-1]-datetime.timedelta(delta_%year)
            else:
                max_date=self.datetimes[-1]
            try:
                samples=[i.month-1 for i in self.datetimes if i <= max_date]
            except:
                samples=[]
                for i in self.datetimes:
                    try:
                        foo=i<=max_date
                        if foo:
                            samples.append(i.month-1)
                    except:
                        self.bad_datetimes+=[i]

        else:
            samples=[i.month-1 for i in self.datetimes]
        histogram=n.histogram(samples,bins=list(range(13)))[0]
        max_discrepancy=histogram.min()/histogram.max()
        # medidas circulares
        circular_measures=circularStatistics(samples,12)

        ar=n.random.randint(0,12,(1000,len(samples)))
        cc=n.array([n.histogram(i,12)[0] for i in ar])
        cc_=cc.min(1)/cc.max(1)
        self.obs12=(cc_.mean(),cc_.std())
        self.obs12_=cc_


        self.months=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
            max_discrepancy_=self.obs12,
            circular_measures=circular_measures
        )
    def yearsStats(self):
        samples=[i.year for i in self.datetimes]
        smin=min(samples)
        smax=max(samples)
        histogram=n.histogram(samples,bins=list(range(smin,smax+2)))[0]
        max_discrepancy=histogram.min()/histogram.max()
        self.years=dict(
            samples=samples,
            histogram=histogram,
            max_discrepancy=max_discrepancy,
        )
