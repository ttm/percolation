import numpy as n


def mediaDesvio2(adict={"stringkey": "strings_list"}):
    measures = {"strings": adict, "numeric": {}, "lengths": {}}
    keys = [key for key in adict if key[0] != "n"]
    for key in keys:
        lengths = [len(i) for i in adict[key]]
        measures["numeric"]["m"+key] = n.mean(lengths)
        measures["numeric"]["d"+key] = n.std(lengths)
        measures["lengths"][key] = lengths
    return measures


def mediaDesvio(adict={"stringkey": "strings_list"}, tids=("astring", "bstring")):
    """Calcula media e desvio dos tamanhos das strings"""
    if not tids:
        tids = tuple(adict.keys())
    measures_dict = {}
    lengths_dict = {}
    for tid in tids:
        lengths = [len(i) for i in adict[tid]]
        measures_dict["m"+tid] = n.mean(lengths)
        measures_dict["d"+tid] = n.std(lengths)
        lengths_dict["L"+tid] = lengths
    return measures_dict, lengths_dict
