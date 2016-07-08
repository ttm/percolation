import re


def fromDict(tdict, column_names, fname='', caption='', longtable=False, size='\\scriptsize'):
    # first row with column names
    # subsequent rows with tdict key and column values
    first_row = ('\\textbf{{{}}}'+" & \\textbf{{{}}} "*(len(column_names)-1)+"\\\\\\hline\n").format(*column_names)
    rows = [first_row]
    for key in tdict:
        vals = tdict[key]
        row = key
        for column_name in column_names[1:]:
            val = vals[column_name]
            if isinstance(val, float):
                row += " & %.2f " % (val,)
            else:
                row += " & %s " % (val,)
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
    header += '\\hline \\multicolumn{'+str(ncolumns)+'}{r}{\\textit{Continued on next page}} \\\\\n\\endfoot\\hline\\endlastfoot\n'
    footer = '\\end{longtable}\n\\end{center}'
    string_table_ = '\\hline'.join(rows[1:])
    table = header+string_table_+footer
    return table


def encapsulateTable(string_table, caption):
    caption_ = "\\caption{{{}}}\n".format(caption)
    header = "\\begin{table*}[h!]\n\\begin{center}\n"+caption_+"\\begin{tabular}{| l |"+" c |"*(string_table.split("hline")[0].count("&"))+"}\\hline\n"
    footer = "\\end{tabular}\\end{center}\n\\end{table*}"
    table = header+string_table+footer
    return table


# def doubleLines(tablefname, hlines=["i1", "i2"], vlines=["j1", "j2"], hlines_=[]):
def doubleLines(fname, hlines=[1, 2], vlines=[2, -1], hlines_=[]):
    """make double lines or remove horizontal lines in a string latex table

    tablefname: the filename for the file with the table

    hlines: indexes of the horizontal lines to be duplicated

    vlines: indexes of the vertical lines to be duplicated

    hlines_: indexes of the horizontal lines to be omitted"""
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
