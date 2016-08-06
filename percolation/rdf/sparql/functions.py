__doc__="""generic routines that don't require a sparql connection"""
import percolation as P
import rdflib as r
from percolation.rdf import NS, a
c = P.check
default = ("urn:x-arq:DefaultGraph",)
default = "default"


def buildQuery(triples1,         graph1=default, modifier1="",
               triples2=None,    graph2=default, modifier2="",
               triples3=None,    graph3=default, modifier3="",
               distinct1=None,   startB_=None,   startB3_=None,
               body3close_=None, body3modifier="",
               method="select"):
    """The general query builder from fields and respective triples or uris"""
    if graph1 and graph1 != default:
        graphpart1 = " GRAPH <%s> { " % (graph1,)
        body1close = " } } "
    else:
        graphpart1 = ""
        body1close = " } "
    if graph2 != default:
        graphpart2 = " GRAPH <%s> { " % (graph2,)
        body2close = " } } "
    else:
        graphpart2 = ""
        body2close = " } "
    if graph3 != default:
        graphpart3 = " GRAPH <%s> { " % (graph3,)
        body3close = " } } "
    else:
        graphpart3 = ""
        body3close = " } "
    DATA_QUERY = method.count("_") == 0
    if isinstance(triples1, str):
        querystring1 = triples1
    elif isinstance(triples1, (tuple, list)):
        if distinct1:
            distinct1 = " DISTINCT "
        if len(triples1) == 3 and not isinstance(triples1[0], (tuple, list)):
            triples1 = (triples1,)
        tvars = []
        body = ""
        for line in triples1:
            tvars += [i for i in line if str(i)[0] == "?" and
                      "foo" not in i and " " not in i and i.count("?") == 1]
            body += formatQueryLine(line)
        tvars = P.utils.uniqueItems(tvars)
        tvars_string = (" %s "*len(tvars)) % tuple(tvars)
        if "select" in method.lower():
            start = "SELECT "
            startB = tvars_string+" WHERE { "
        elif "delete" in method.lower():
            start = "DELETE "
            if DATA_QUERY:
                start += " DATA "
            startB = " { "
        elif "insert" in method.lower():
            start = "INSERT "
            if DATA_QUERY:
                start += " DATA "
            startB = " { "
        if startB_:
            startB = startB_
        querystring1 = start+startB+graphpart1+body+body1close+modifier1
    else:
        querystring1 = ""
    if isinstance(triples2, str):
        querystring2 = triples2
    elif isinstance(triples2, (tuple, list)):
        if len(triples2) == 3 and not isinstance(triples2, (list, tuple)):
            triples2 = (triples2,)
        body2 = ""
        for line in triples2:
            body2 += formatQueryLine(line)
        if ("where" in method.lower()) and (method.count("_") == 1):
            start2 = " WHERE  "
            startB2 = " { "
        elif "insert" in method.lower():
            start2 = " INSERT "
            startB2 = " { "
        querystring2 = start2+startB2+graphpart2+body2+modifier2+body2close
    else:
        querystring2 = ""
    if isinstance(triples3, str):
        querystring3 = triples3
    elif isinstance(triples3, (tuple, list)):
        if len(triples3[0]) != 3:
            triples3 = (triples3,)
        body3 = ""
        for line in triples3:
            body3 += formatQueryLine(line)
        start3 = " WHERE  "
        startB3 = " { "
        if startB3_:
            startB3 = startB3_
        if body3close_:
            body3close = body3close_
        querystring3 = start3+startB3+graphpart3\
            + body3modifier+body3+body3close+modifier3
    else:
        querystring3 = ""
    querystring = querystring1+querystring2+querystring3
    return querystring


def dictQueryValues(result_dict):
    results = []
    for result in result_dict["results"]["bindings"]:
        keys = result.keys()
        this_result = {}
        for key in keys:
            value = result[key]["value"]
            type_ = result[key]["type"]
            if type_ == "uri":
                value = r.URIRef(value)
            elif type_ in ("literal", "bnode"):
                pass
            elif type_ == "typed-literal":
                if result[key]["datatype"] == (NS.xsd.integer).toPython():
                    value = int(value)
                elif result[key]["datatype"] == (NS.xsd.datetime).toPython():
                    pass
                elif result[key]["datatype"] == (NS.xsd.date).toPython():
                    pass
                elif result[key]["datatype"] == (NS.xsd.boolean).toPython():
                    if value == "true":
                        value = True
                    elif value == "false":
                        value = False
                    else:
                        raise TypeError("Incomming boolean not understood")
            else:
                raise TypeError("Type of incomming variable not understood")
            this_result[key] = [value]
        results += [this_result]
    return results


def plainQueryValues(result_dict, join_queries=False):
    """Return query values as simplest list.

    Set join_queries="hard" to keep list of lists structure
    when each result hold only one variable"""

    results = []
    if "bindings" in dir(result_dict):
        results_ = result_dict.bindings
        for result in results_:
            keys = sorted(result.keys())
            this_result = []
            for key in keys:
                value = result[key].toPython()
                this_result += [value]
            results += [this_result]
        if len(results) and len(keys) == 1 and join_queries != "hard":
            results = [i[0] for i in results]
        if len(results) == 1 and join_queries != "list":
            results = results[0]
        return results
    else:
        for result in result_dict["results"]["bindings"]:
            keys = sorted(result.keys())
            this_result = []
            for key in keys:
                value = result[key]["value"]
                type_ = result[key]["type"]
                if type_ == "uri":
                    value = r.URIRef(value)
                elif type_ in ("literal", "bnode"):
                    pass
                elif type_ == "typed-literal":
                    if result[key]["datatype"] == (NS.xsd.integer).toPython():
                        value = int(value)
                    elif result[key]["datatype"] == \
                            (NS.xsd.dateTime).toPython():
                        pass
                    elif result[key]["datatype"] == (NS.xsd.date).toPython():
                        pass
                    elif result[key]["datatype"] == (NS.xsd.boolean).toPython():
                        if value == "true":
                            value = True
                        elif value == "false":
                            value = False
                        else:
                            raise TypeError("Incomming boolean not understood")
                    else:
                        raise TypeError("Incomming typed-literal variable not\
                                        understood")
                else:
                    raise TypeError("Type of incomming variable not understood")
                this_result += [value]
            results += [this_result]
        if len(results) and len(keys) == 1 and join_queries != "hard":
            results = [i[0] for i in results]
        return results


def performFileGetQuery(tfile, triples=(("?s", a, NS.po.Snapshot),)):
    g = r.Graph()
    g.parse(tfile)
    tvars = []
    body = ""
    for line in triples:
        tvars += [i for i in line if i[0] == "?" and "foo" not in i]
        body += formatQueryLine(line)
    tvars = P.utils.uniqueItems(tvars)
    tvars_string = (" %s "*len(tvars)) % tuple(tvars)
    querystring = "SELECT "+tvars_string+" WHERE { "+body+" } "
    return g.query(querystring)


def formatQueryLine(triple):
    if len(triple) == 4:
        start = " %s { " % (triple[0],)
        end = " } "
        triple = triple[1:]
    else:
        start = ""
        end = ""
    line = ""
    if isinstance(triple[2], str) and len(triple[2]) == 1 and triple[2] == "?":
        return ""
    for term in triple:
        if isinstance(term, (r.Namespace, r.URIRef)):
            line += " <%s> " % (term,)
        elif (str(term)[0] == "?" and term.count("?") == 1 and
              " " not in term[0]) or (str(term)[:2] == "_:") or\
                "uri(" in str(term):
            line += " %s " % (term,)
        elif isinstance(term, str) and not (term[0] == "?" and
                                            term.count("?") == 1 and
                                            " " not in term):
            # line+=' '+repr(term)+' '
            # if "'" not in term:
            # term = term.replace('\\', "\\\\")
            term = term.replace('\\', "")
            term = term.replace('"', "'")
            # term = term.encode("unicode_escape").decode("utf8").encode(
            #     "unicode_escape").decode("utf8")
            line += ' """'+term+'""" '
        else:
            line += ' "%s" ' % (term,)
    line = start+line+end+" . "
    return line


def addToFusekiEndpoint(end_url, tfiles):
    import os
    import time
    aa = []
    for tfile in tfiles:
        time.sleep(.1)
        tgraph = P.utils.urifyFilename(tfile)
        cmd = "s-post {} {} {}".format(end_url, tgraph, tfile)
        aa += [os.system(cmd)]
