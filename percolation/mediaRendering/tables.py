import re
import numpy as n


def fromDict(tdict, column_names, fname='', caption='', longtable=False, size='\\scriptsize'):
    # first row with column names
    # subsequent rows with tdict key and column values
    first_row = ('\\textbf{{{}}}'+" & \\textbf{{{}}} "*(len(column_names)-1)+"\\\\\\hline\n").format(*column_names)
    rows = [first_row]
    for key in tdict:
        vals = tdict[key]
        row = key
        if len(column_names) > 2:
            for column_name in column_names[1:]:
                val = vals[column_name]
                if isinstance(val, float):
                    row += " & {:,.2f} ".format(val,)
                elif not val:
                    row += " & 0 "
                else:
                    row += " & {:,} ".format(val,)
        else:
            if isinstance(vals, float):
                row += " & {:,.2f} ".format(vals,)
            elif isinstance(vals, int):
                row += " & {:,} ".format(vals,)
            else:
                row += " & {} ".format(vals,)
        row += "\\\\\\hline\n"
        rows.append(row)
    string_table = ''.join(rows).replace('#', '\\#').replace('_', '\\_')
    if not longtable:
        table_complete = encapsulateTable(string_table, caption)
    else:
        table_complete = encapsulateLongTable(string_table, caption, size)
    if fname:
        with open(fname, 'w') as f:
            f.write(table_complete)
    return table_complete


def encapsulateLongTable(string_table, caption, size):
    caption_ = "\\caption{{{}}}\n".format(caption)
    rows = string_table.split('\\hline')
    ncolumns = rows[0].count("&")+1
    header = "\\begin{center}\n"+size+"\\begin{longtable}{| l |"+" c |"*(ncolumns-1)+"}\n"+caption_+'\\\\\n\\hline\n'
    header += rows[0]+'\\hline\\hline\n\\endfirsthead\n'
    header += '\\multicolumn{{{}}}{{c}}'.format(ncolumns)+'{\\tablename\\ \\thetable\\ -- \\textit{Continued from previous page}} \\\\\\hline\n'
    header += rows[0]+'\\hline\\hline\\endhead\n'
    # header += '\\hline\\endhead\n'
    header += '\\multicolumn{'+str(ncolumns)+'}{r}{\\textit{Continued on next page}} \\\\\n\\endfoot\\endlastfoot\n'
    footer = '\\end{longtable}\n\\end{center}'
    string_table_ = '\\hline'.join(rows[1:])
    table = header+string_table_+footer
    return table


def encapsulateTable(string_table, caption, label='foobar'):
    caption_ = "\\caption{{{}}}\label{{{}}}\n".format(caption, label)
    header = "\\begin{table*}[h!]\n\\begin{center}\n"+caption_+"\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&"))+"}\\hline\n"
    footer = "\\end{tabular}\\end{center}\n\\end{table*}"
    table = header+string_table+footer
    return table


# def doubleLines(tablefname, hlines=["i1", "i2"], vlines=["j1", "j2"], hlines_=[]):
def doubleLines(fname, hlines=[1, 2], vlines=[2, -1], hlines_=[], vlines_=[]):
    """make double lines or remove horizontal lines in a string latex table

    tablefname: the filename for the file with the table

    hlines: indexes of the horizontal lines to be duplicated
    vlines: indexes of the vertical lines to be duplicated
    hlines_: indexes of the horizontal lines to be omitted.
    vlines_: indexes of the vertical lines to be omitted.
    """
    with open(fname, "r") as f:
        lines = f.read()
    # colocando barras nas linhas verticais
    header = re.findall(r"\\begin{tabular}{(.*)}\\hline\n", lines)[0]
    indexes = [i.start() for i in re.finditer("\|", header)]
    header_ = header[:]
    foo = 0
    for j in vlines:
        j_ = indexes[j]+foo
        header_ = header_[:j_]+"||"+header_[j_+1:]
        foo += 1
    indexes = [i.start() for i in re.finditer("\|{1,2}", header)]
    for j in vlines_:
        j_ = indexes[j]
        header_ = header_[:j_]+" "+header_[j_+1:]
    lines__ = lines.replace(header, header_)
    # colocando barras nas linhas horizontais
    linhas = lines__.split("\\hline")
    ii = hlines
    linesF = lines__[:]
    for i in ii:
        linha = linhas[i]
        linha_ = linha+"\\hline"
        if lines__.count(linha) == 1:
            linesF = linesF.replace(linha, linha_)
        elif lines__.count(linha) > 1:
            raise ValueError("more than one equal line")
        else:
            raise ValueError("line does not exist")
    ii = hlines_
    for i in ii:
        linha = linhas[i]
        if lines__.count(linha) == 1:
            linesF = linesF.replace(linha+"\\hline", linha)
        elif lines__.count(linha) > 1:
            raise ValueError("more than one equal line")
        else:
            raise ValueError("line does not exist")
    with open(fname, 'w') as f:
        f.write(linesF)
    return linesF


def fontSize(fname, ftag="\\scriptsize", write=False):
    """Change size of table font"""
    with open(fname, "r") as f:
        lines = f.read()
    l = lines.split("\n")
    l.insert(1, ftag)
    l = "\n".join(l)
    if not write:
        return l
    else:
        writeTex(l, fname)


def writeTex(string, filename):
    with open(filename, "w") as f:
        f.write(string)


def makeTabular(labels,data,two_decimal=False,ttype=None):
    """Returns a latex tabular string from data with labels in first column.
    
    Returns latex printable or writable to files to
    be imported by latex files.
    """
    if len(labels)!=len(data):
        print("input one label per data row")
        return
    if not two_decimal:
        string = "".join([(labels[i]+" & {} "*len(datarow)+"\\\\\\hline\n").format(*datarow) for i, datarow in enumerate(data)])
    else:
        # data="".join([((str(labels[i])+" & %.2f "*len(datarow) +"\\\\\\hline\n")%tuple(datarow)) for i, datarow in enumerate(data)])
        string = ''
        for i, datarow in enumerate(data):
            string += str(labels[i])
            for item in datarow:
                if isinstance(item, float):
                    string += ' & %.2f ' % (item, )
                else:
                    string += ' & %s ' % (item, )
            string += '\\\\\\hline\n'
    return string


def partialSums(labels, data, partials, partial_labels="", datarow_labels=""):
    """Returns a latex table with sums of data.

    Data is though to be unidimensional. Each row
    is transposed to a column to which partial sum
    are added."""

    lines=[]
    for label in labels:
        lines.append("{} ".format(label))
    for datarow in data:
        for partial in partials:
            for line_num in range(len(datarow)):
                if (line_num%partial)==0:
                    lines[line_num]+="& \\multirow{{{:d}}}{{*}}{{ {:.2f} }}  ".format(partial, sum(datarow[line_num:line_num+partial]))
                else:
                    lines[line_num]+="& "

    for line_num in range(len(lines)):
        cuts = [(0 == (line_num+1) % partial) for partial in partials]
        i = 0
        suffix = ""
        for cut in cuts:
            if cut:
                for datarownum in range(len(data)):
                    num = i+(datarownum)*len(partials)
                    suffix += "\\cline{{{}-{}}}".format(num+2, num+2)
            i+=1
        lines[line_num] += "\\\\{}\n".format(suffix)
    
    ltable = "".join(lines)

    if partial_labels:
        header = ( (" & {}"*len(partial_labels)).format(*partial_labels) )*len(data)+" \\\\\\hline\n"
        ltable = header+ltable
    if datarow_labels:
        header = ((" & \\multicolumn{{%i}}{{c|}}{{{}}}"%(len(partials),))*len(datarow_labels)).format(*datarow_labels)+" \\\\\\hline\n"
        ltable = header+ltable
    header = "\\begin{center}\n\\begin{tabular}{| l ||"+" c |"*len(data)*len(partials)+"}\\hline\n"
    footer = "\\hline\\end{tabular}\n\\end{center}"
    ltable = header+ltable+footer
    return ltable


def pcaTable(labels, vec_mean, vec_std, val_mean, val_std):
    """Make table with PCA formation mean and std"""
    header = "\\begin{center}\n\\begin{tabular}{| l |"+" c |"*6+"}\\cline{2-7}\n"
    header += "\\multicolumn{1}{c|}{} & \\multicolumn{2}{c|}{PC1}          & \multicolumn{2}{c|}{PC2} & \multicolumn{2}{c|}{PC3}  \\\\\\cline{2-7}"
    header += "\\multicolumn{1}{c|}{} & $\mu$            & $\sigma$ & $\mu$         & $\sigma$ & $\mu$ & $\sigma$  \\\\\\hline\n"
    tt = n.zeros((vec_mean.shape[0], 6))
    tt[:,::2] = vec_mean
    tt[:,1::2] = vec_std
    tt_ = n.zeros(6)
    tt_[::2] = val_mean
    tt_[1::2] = val_std
    tab_data = n.vstack((tt,tt_))
    footer = "\\hline\\end{tabular}\n\\end{center}"
    table = header + makeTabular(labels, tab_data, True) + footer
    return table
