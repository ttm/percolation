import numpy as n
import time
import string
import os
import nltk as k
import percolation as P
c = P.c

wn = k.corpus.wordnet
STOPWORDS = set(k.corpus.stopwords.words('english'))
tpath = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
if 'words.txt' not in os.listdir('.'):
    print('downloading english words list')
    os.system('wget https://raw.githubusercontent.com/dwyl/english-words/master/words.txt {}words.txt'.format(tpath))
    print('finished download')
with open(tpath + 'words.txt') as f:
    WORDLIST = set(f.read())

__doc__ = "analysis of chars, tokens, sentences and messages"


def systemAnalyseAll(sectors_analysis):
    all_texts_measures = {}
    for sector in sectors_analysis:
        for data_grouping in sectors_analysis[sector]["raw_analysis"]:
            for data_group in sectors_analysis[sector]["raw_analysis"][data_grouping]:
                for measure_group in data_group:
                    for measure_type in data_group[measure_group]:
                        for measure_name in data_group[measure_group][measure_type]:
                            measure = data_group[measure_group][measure_type][measure_name]
                            if measure_type == "lengths_overall":  # directly from tokens
                                measure_type_ = "lengths_overall"
                                data_grouping_ = "strings"
                            elif measure_type == "numeric_overall_low":  # texts
                                measure_type_ = "numeric_overall_low"
                                data_grouping_ = "texts"
                            elif measure_type == "numeric_overall":  # authors
                                measure_type_ = "numeric_overall"
                                data_grouping_ = "authors"
                            elif measure_type == "second_numeric_overall":  # authors from messages
                                measure_type_ = "second_numeric_overall"
                                data_grouping_ = "authors_messages"

                            elif measure_type == "numeric":  # sectors from data_grouping = strings
                                measure = [measure]
                                measure_type_ = "numeric_overall_high"  # high quando o valor eh associado ao setor
                                data_grouping_ = "sectors_strings"
                            elif measure_type == "second_numeric_low":  # sectors from data_grouping = sectors_texts,
                                measure = [measure]
                                measure_type_ = "second_numeric_overall_low_high"
                                data_grouping_ = "sectors_texts"
                            elif measure_type == "second_numeric":  # sectors from data_grouping = authors
                                measure = [measure]
                                measure_type_ = "second_numeric_overall_high"
                                data_grouping_ = "sectors_authors"
                            elif measure_type == "third_numeric":  # sectors from authors from messages from texts
                                measure = [measure]
                                measure_type_ = "third_numeric_overall_high"
                                data_grouping_ = "sectors_authors_messages"
                            else:
                                raise KeyError("data structure not understood")
                            all_texts_measures[data_grouping_][0][measure_group][measure_type_][measure_name] += measure
    for data_grouping in all_texts_measures:  # chars, tokens, sents
        for data_group in all_texts_measures["data_grouping"]:  # chars, tokens, sents
          for measure_group in data_group:  # chars, tokens, sents
            for measure_type in data_group[measure_group]:  # only list/tuple of strings at first
                for measure_name in all_texts_measures[measure_group][measure_type]:  # nchars, frac_x, known_words, etc
                    vals = all_texts_measures[measure_group][measure_type][measure_name]
                    mean_val = n.mean(vals)
                    std_val = n.std(vals)
                    mean_name = "M{}".format(measure_name)
                    std_name = "D{}".format(measure_name)
                    if measure_type == "lengths_overall":  # directly from strings, data_grouping  =  =  "strings"
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name] = std_val
                    elif measure_type == "numeric_overall_low":  # from messages, data_grouping  =  =  "texts"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][std_name] = std_val
                    elif measure_type == "numeric_overall":  # from authors, data_grouping  =  =  "authors"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name] = std_val
                    elif measure_type == "second_numeric_overall":  # from authors from messages, data_grouping = authors_messages
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][std_name] = std_val

                    elif measure_type == "numeric_overall_high":  # from sectors from sectors_strings, sectors_strings
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_high"][std_name] = std_val
                    elif measure_type == "second_numeric_overall_low_high":  # from sectords from texts, data_grouping = sectors_texts
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_low_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_low_high"][std_name] = std_val
                    elif measure_type == "second_numeric_overall_high":  # from sectors from authors, data_grouping = sectors_authors
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_high"][std_name] = std_val
                    elif measure_type == "third_numeric_overall_high":  # from authors from messages, data_grouping = authors_messages
                        all_texts_measures[data_grouping][0][measure_group]["fourth_numeric_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["fourth_numeric_high"][std_name] = std_val
                    else:
                        raise KeyError("data structure not understood")
    return all_texts_measures


def sectorsAnalyseAll(authors_analysis, sectorialized_agents):
    all_texts_measures = {}
    for sector in sectorialized_agents:
      for agent in sectorialized_agents[sector]:
          analysis = authors_analysis[sector][agent]["wordnet"]
          for data_grouping in analysis:
              for data_group in analysis[data_grouping]:
                  for measure_group in data_group:
                      for measure_type in data_group[measure_group]:
                          for measure_name in data_group[measure_group][measure_type]:
                              measure = data_group[measure_group][measure_type][measure_name]
                              if measure_type == "lengths_overall":  # directly from tokens
                                  measure_type_ = "lengths_overall"
                                  data_grouping_ = "strings"
                              elif measure_type in "numeric_overall":  # messages
                                  measure_type_ = "numeric_overall_low"
                                  data_grouping_ = "texts"
                              elif measure_type in "numeric":  # authors
                                  measure = [measure]
                                  measure_type_ = "numeric_overall"
                                  data_grouping_ = "authors"
                              elif measure_type == "second_numeric":  # authors from messages
                                  measure = [measure]
                                  data_grouping_ = "authors_messages"
                                  measure_type_ = "second_numeric_overall"
                              else:
                                  raise KeyError("data structure not understood")
                              all_texts_measures[data_grouping_][0][measure_group][measure_type_][measure_name] += measure
    for data_grouping in all_texts_measures:  # chars, tokens, sents
        for data_group in all_texts_measures["data_grouping"]:  # chars, tokens, sents
          for measure_group in data_group:  # chars, tokens, sents
            for measure_type in data_group[measure_group]:  # only list/tuple of strings at first
                for measure_name in all_texts_measures[measure_group][measure_type]:  # nchars, frac_x, known_words, etc
                    vals = all_texts_measures[measure_group][measure_type][measure_name]
                    mean_val = n.mean(vals)
                    std_val = n.std(vals)
                    mean_name = "M{}".format(measure_name)
                    std_name = "D{}".format(measure_name)
                    if measure_type == "lengths_overall":  # directly from strings, data_grouping  =  =  "strings"
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name] = std_val
                    elif measure_type == "numeric_overall_low":  # from messages, data_grouping  =  =  "texts"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][std_name] = std_val
                    elif measure_type == "numeric_overall":  # from authors, data_grouping  =  =  "authors"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name] = std_val
                    elif measure_type == "second_numeric_overall":  # from authors from messages, data_grouping = authors_messages
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][std_name] = std_val
    return all_texts_measures


def analyseAll(texts_list):
    """Make raw text analysis of all texts and of the merged text"""
    # medidas por mensagem
    texts_measures = {"each_text": []}
    for text in texts_list:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["chars"] = medidasChars(text)
        texts_measures["each_text"][-1]["tokens"] = medidasTokens(text)
        texts_measures["each_text"][-1]["sentences"] = medidasSentencasParagrafos(text, texts_measures[-1]["tokens"]["known_words_unique"])
    del text
    texts_measures.update(medidasMensagens2(texts_measures["each_text"]))
    return texts_measures


def medidasMensagens2(texts_measures):
    all_texts_measures = {}
    for data_group in texts_measures:  # each_text
        for measure_group in data_group:  # chars, tokens, sents
            for measure_type in data_group[measure_group]:  # numeric or list/tuple of strings
                for measure_name in data_group[measure_group][measure_type]:  # nchars, frac_x, known_words, etc
                    measure = data_group[measure_group][measure_type][measure_name]
                    if measure_type == "lengths":  # from overall text directly
                        measure_type = "lengths_overall"
                        data_grouping = "strings"
                    elif measure_type == "numeric":  # from each of the texts
                        measure = [measure]
                        measure_type = "numeric_overall"
                        data_grouping = "texts"
                    all_texts_measures[data_grouping][0][measure_group][measure_type][measure_name] += measure
    for data_grouping in all_texts_measures:  # "strings" ou "texts"
      for data_group in all_texts_measures[data_grouping]:
        for measure_group in data_group:  # chars, tokens, sents
            for measure_type in data_group[measure_group]:  # numeric or list/tuple of strings
                for measure_name in data_group[measure_group][measure_type]:  # nchars, frac_x, known_words, etc
                    vals = data_group[measure_group][measure_type][measure_name]
                    mean_name = "M{}".format(measure_name)
                    std_name = "M{}".format(measure_name)
                    if measure_type == "lengths_overall":  # from overall text directly
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name] = n.mean(vals)
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name] = n.std(vals)
                    elif measure_type == "numeric_overall":  # from each of the texts
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name] = n.mean(vals)
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name] = n.std(vals)
    return all_texts_measures


def medidasChars(T):
    """Medidas de letras TTM formatar para passagem como dicionário"""
    nchars = len(T)
    nspaces = T.count(" ")
    nletters = sum([t.isalpha() for t in T])
    nuppercase = sum([t.isupper() for t in T])
    nvowels = sum([t in ("a", "e", "i", "o", "u") for t in T])
    npunctuations = sum([t in string.punctuation for t in T])
    ndigits = sum([t.isdigit() for t in T])  # numerais
    frac_spaces = nspaces/nchars
    frac_letters = nletters/(nchars-nspaces)
    frac_vowels = nvowels/nletters
    frac_uppercase = nuppercase/nletters
    frac_punctuations = npunctuations/(nchars-nspaces)
    frac_digits = ndigits/(nchars-nspaces)
    del T, nspaces, nletters, nuppercase, nvowels, npunctuations, ndigits
    measures = {"numeric": locals()}
    return measures


def medidasTokens(T):
    """Medidas extensas sobre os tokens TTM"""
    atime = time.time()
    T = T.lower()
    tokens = k.tokenize.wordpunct_tokenize(T)
    del T
    tokens = [t.lower() for t in tokens]
    # known and unkown words
    known_words = []
    unknown_words = []
    punctuation_tokens = []
    stopwords = []
    for t in tokens:
        if t in WORDLIST:
            known_words.append(t)
        elif sum([tt in string.punctuation for tt in t]) == len(t):
            punctuation_tokens.append(t)
        else:
            unknown_words.append(t)
        if t in STOPWORDS:
            stopwords.append(t)
    del t
    stopwords_unique = set(stopwords)
    known_words_unique = set(known_words)
    unknown_words_unique = set(unknown_words)
    known_words_has_wnsynset = [i for i in known_words if wn.synsets(i)]
    known_words_has_wnsynset_unique = set(known_words_has_wnsynset)
    known_words_no_wnsynset = [i for i in known_words if i not in known_words_has_wnsynset_unique]
    known_words_no_wnsynset_unique = set(known_words_no_wnsynset)
    known_words_stopwords = [i for i in known_words if i in stopwords_unique]
    known_words_stopwords_unique = set(known_words_stopwords)
    known_words_not_stopwords = [i for i in known_words if i not in stopwords_unique]
    known_words_not_stopwords_unique = set(known_words_not_stopwords)
    unknown_words_stopwords = [i for i in unknown_words if i in stopwords_unique]
    known_words_stopwords_has_wnsynset = [i for i in known_words_has_wnsynset if i in stopwords_unique]
    # known words that dont return synsets and are stopwords
    known_words_stopwords_no_wnsynset = [i for i in known_words_no_wnsynset if i in stopwords_unique]
    c("MT6:")
    # words that are known, are not stopwords and do not return synset
    foo_ = known_words_no_wnsynset_unique.difference(stopwords_unique)
    known_words_not_stopword_no_wnsynset = [i for i in known_words if i in foo_]
    c("MT7:")
    # known words with synset that are not stopwords
    foo_ = known_words_has_wnsynset_unique.difference(stopwords_unique)
    known_words_not_stopword_has_synset = [i for i in known_words if i in foo_]
    known_words_not_stopword_has_synset_unique = set(known_words_not_stopword_has_synset)
    del foo_
    measures = P.measures.text.aux.mediaDesvio2(locals())
    measures["numeric"].update(tokensFracs(measures["strings"]))
    return measures


def tokensFracs(strings):
    ntokens = len(strings["tokens"])
    frac_punctuations = len(strings["punctuations"])/len(strings["tokens"])
    frac_known_words = len(strings["known_words"])/len(strings["tokens"])
    frac_stopwords = len(strings["stopwords"])/len(strings["known_words"])
    lexical_diversity = len(strings["known_words"])/len(strings["known_words_unique"])
    token_diversity = len(strings["tokens_unique"])/ntokens
    del strings
    return locals()


def medidasSentencasParagrafos(T, known_words_unique):
    """Medidas das sentenças TTM"""
    paragraphs = [i.strip() for i in T.split("\n")]
    nparagraphs_empty = len([i for i in paragraphs if not i])
    paragraphs = [i for i in paragraphs if i]

    sentences_paragraphs = [k.sent_tokenize(j) for j in paragraphs]
    tokens_paragraphs = [k.tokenize.wordpunct_tokenize(j) for j in paragraphs]  # Para os POS tags
    known_words_paragraphs = [[ii for ii in i if ii in known_words_unique] for i in tokens_paragraphs]
    known_words_not_stopwords_paragraphs = [[i for i in ts if (i not in STOPWORDS) and (i in WORDLIST)] for ts in tokens_paragraphs]
    stopwords_paragraphs = [[i for i in ts if i in STOPWORDS] for ts in tokens_paragraphs]
    punctuations_paragraphs = [[i for i in ts if
                                (len(i) == sum([(ii in string.punctuation) for ii in i]))]
                               for ts in tokens_paragraphs]
    sentences = k.sent_tokenize(T)
    del T
    nsentences_empty = len([i for i in sentences if not i])
    sentences = [i for i in sentences if i]
    tokens_sentences = [k.tokenize.wordpunct_tokenize(i) for i in sentences]  # Para os POS tags
    known_words_sentences = [[ii for ii in i if ii in known_words_unique] for i in tokens_sentences]
    known_words_not_stopwords_sentences = [[i for i in ts if (i not in STOPWORDS) and (i in WORDLIST)] for ts in tokens_sentences]
    stopwords_sentences = [[i for i in ts if i in STOPWORDS] for ts in tokens_sentences]
    punctuations_sentences = [[i for i in ts if
                               (len(i) == sum([(ii in string.punctuation) for ii in i]))]
                              for ts in tokens_sentences]

    measures = P.text.aux.mediaDesvio2(locals())
    measures["numeric"].update(sentenceFracs(measures["strings"]))
    return measures


def sentenceFracs(strings):
    frac_sentences_paragraph = len(strings["sentences"])/len(strings["paragraphs"])
    del strings
    return locals()


def medidasMensagens(texts_list):
    """Medidas das mensagens em si"""
    tokens_messages = [k.tokenize.wordpunct_tokenize(t) for t in texts_list]  # tokens
    known_words_messages = [[i for i in toks if (i not in STOPWORDS) and (i in WORDLIST)] for toks in tokens_messages]
    stopwords_messages = [[i for i in toks if i in STOPWORDS] for toks in tokens_messages]
    punctuations_messages = [[i for i in toks if
                              (len(i) == sum([(ii in string.punctuation) for ii in i]))]
                             for toks in tokens_messages]
    sentences_msgs = [k.sent_tokenize(t) for t in texts_list]  # tokens
    chars_messages = texts_list[:]
    nmessages = len(texts_list)
    del texts_list
    locals_ = locals()
    mvars = tuple(locals_.keys())
    medidas = P.measures.text.aux.mediaDesvio(mvars, locals())
    medidas.update(locals_)
    return medidas
