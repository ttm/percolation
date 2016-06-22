from percolation import c
import powerlaw
__doc__ = "fit of arbitrary data to a power-law distribution"


def fitNetwork(topom_dict):
    """Under the framework developed at: http://arxiv.org/abs/1305.0215"""
    powerlaw_degree_fit = fitData(topom_dict["degrees_"])
    if 'strengths_' in topom_dict:
        powerlaw_strength_fit = fitData(topom_dict["strengths_"])
    else:
        powerlaw_strength_fit = powerlaw_degree_fit
    return powerlaw_degree_fit, powerlaw_strength_fit


def fitData(data):
    """Under the framework developed at: http://arxiv.org/abs/1305.0215"""
    c("plaw fit start")
    fit = powerlaw.Fit(data, discrete=True)
    c("plaw fit end")
    dists = list(fit.supported_distributions.keys())
    dists.remove("power_law")
    for dist in dists:
        c("plaw compare start: " + dist)
        comp = fit.distribution_compare("power_law", dist)
        exec("fit.{}_R=comp[0]".format(dist))
        exec("fit.{}_p=comp[1]".format(dist))
        c("plaw compare end: "+dist)
    del dist, comp
    return locals()
