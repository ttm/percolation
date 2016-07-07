import collections as c
import numpy as n
from percolation.measures.text.aux import WORDLIST, brill_tagger
import percolation as P
__doc__ = "text analysis with POS tags"


def systemAnalyseAll(sectors_analysis):
    all_texts_measures = {}
    for sector in sectors_analysis:
        for data_grouping in sectors_analysis[sector]["pos"]:
            for data_group in sectors_analysis[sector]["pos"][data_grouping]:
                for measure_group in data_group:
                    for measure_type in data_group[measure_group]:
                        for measure_name in data_group[measure_group][measure_type]:
                            measure = data_group[measure_group][measure_type][measure_name]
                            if measure_type == "pos_tags_overall":  # directly from tokens
                                measure_type_ = "pos_tags_overall"
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
                            elif measure_type == "numeric":  # sectors from data_grouping=strings
                                measure = [measure]
                                measure_type_ = "numeric_overall_high"  # high quando o valor eh associado ao setor
                                data_grouping_ = "sectors_strings"
                            elif measure_type == "second_numeric_low":  # sectors from data_grouping=sectors_texts,
                                measure = [measure]
                                measure_type_ = "second_numeric_overall_low_high"
                                data_grouping_ = "sectors_texts"
                            elif measure_type == "second_numeric":  # sectors from data_grouping=authors
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
                for measure_name in all_texts_measures[measure_group][measure_type]:
                    measure = all_texts_measures[measure_group][measure_type][measure_name]
                    if measure_type != "pos_tags_overall":
                        mean_val = n.mean(measure)
                        std_val = n.std(measure)
                        mean_name = "M{}".format(measure_name)
                        std_name = "D{}".format(measure_name)
                    if measure_type == "pos_tags_overall":  # directly from strings, data_grouping  ==  "strings"
                        tags_histogram = c.Counter(measure)
                        tags_histogram_normalized = {}
                        if tags_histogram:
                            factor = 100.0/sum(tags_histogram.values())
                            for i in tags_histogram:
                                tags_histogram_normalized[i] = tags_histogram[i]*factor
                            tags_histogram_normalized = c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1]))
                        all_texts_measures[data_grouping][0][measure_group]["numeric"].update(tags_histogram_normalized)
                    elif measure_type == "numeric_overall_low":  # from messages, data_grouping  ==  "texts"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][std_name] = std_val
                    elif measure_type == "numeric_overall":  # from authors, data_grouping  ==  "authors"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name] = std_val
                    elif measure_type == "second_numeric_overall":  # from authors from messages, data_grouping=authors_messages
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][std_name] = std_val
                    elif measure_type == "numeric_overall_high":  # from sectors from sectors_strings, sectors_strings
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_high"][std_name] = std_val
                    elif measure_type == "second_numeric_overall_low_high":  # from sectords from texts, data_grouping=sectors_texts
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_low_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_low_high"][std_name] = std_val
                    elif measure_type == "second_numeric_overall_high":  # from sectors from authors, data_grouping=sectors_authors
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric_high"][std_name] = std_val
                    elif measure_type == "third_numeric_overall_high":  # from authors from messages, data_grouping=authors_messages
                        all_texts_measures[data_grouping][0][measure_group]["fourth_numeric_high"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["fourth_numeric_high"][std_name] = std_val
                    else:
                        raise KeyError("data structure not understood")
    return all_texts_measures


def sectorsAnalyseAll(authors_analysis, sectorialized_agents):
    all_texts_measures = {}
    # for sector in sectorialized_agents:
    #   for agent in sectorialized_agents[sector]:
    for agent in sectorialized_agents:
          analysis = authors_analysis[agent]["pos"]
          for data_grouping in analysis:  # string or message/text
              for data_group in analysis[data_grouping]:  # whole blob or a message
                  for measure_group in data_group:
                      for measure_type in data_group[measure_group]:
                          for measure_name in data_group[measure_group][measure_type]:
                              measure = data_group[measure_group][measure_type][measure_name]
                              if measure_type == "pos_tags_overall":  # directly from tokens
                                  measure_type_ = "pos_tags_overall"
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
    for data_grouping in all_texts_measures:  # strings, texts, authors, authors_messages
        for data_group in all_texts_measures[data_grouping]:
          for measure_group in data_group:  # pos
            for measure_type in data_group[measure_group]:  # only list/tuple of numbers at first
                for measure_name in all_texts_measures[measure_group][measure_type]:  # `pos tag`, the_tagged_tokens
                    measure = all_texts_measures[measure_group][measure_type][measure_name]
                    if measure_type != "pos_tags_overall":
                        mean_val = n.mean(measure)
                        std_val = n.std(measure)
                        mean_name = "M{}".format(measure_name)
                        std_name = "D{}".format(measure_name)
                    if measure_type == "pos_tags_overall":  # directly from strings, data_grouping  ==  "strings"
                        tags_histogram = c.Counter(measure)
                        tags_histogram_normalized = {}
                        if tags_histogram:
                            factor = 100.0/sum(tags_histogram.values())
                            for i in tags_histogram:
                                tags_histogram_normalized[i] = tags_histogram[i]*factor
                            tags_histogram_normalized = c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1]))
                        all_texts_measures[data_grouping][0][measure_group]["numeric"] = tags_histogram_normalized
                    elif measure_type == "numeric_overall_low":  # from messages, data_grouping  ==  "texts"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric_low"][std_name] = std_val
                    elif measure_type == "numeric_overall":  # from authors, data_grouping  ==  "authors"
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name] = std_val
                    elif measure_type == "second_numeric_overall":  # from authors from messages, data_grouping=authors_messages
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["third_numeric"][std_name] = std_val
    return all_texts_measures


def analyseAll(raw_analysis):
    """Make POS tags analysis of all texts and of merged text"""
    texts_measures = {"each_text": []}
    for each_raw_analysis in raw_analysis["each_text"]:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["pos"] = medidasPOS(each_raw_analysis["sentences"]['strings']["sentences"])
    texts_measures.update(medidasMensagens2(texts_measures["each_text"]))
    del each_raw_analysis, raw_analysis
    return locals()


def medidasMensagens2(texts_measures):
    all_texts_measures_ = {}
    for data_group in texts_measures:  # each text
        for measure_group in data_group:  # pos
            for measure_type in data_group[measure_group]:  # numeric or list/tuple of strings
                for measure_name in data_group[measure_group][measure_type]:  # nchars, frac_x, known_words, etc
                    measure = data_group[measure_group][measure_type][measure_name]
                    if measure_type == "tagged_tokens":
                        measure = [i[1] for i in measure]
                        measure_type_ = "pos_tags_overall"
                        data_grouping = "strings"
                    elif measure_type == "numeric":
                        measure = [measure]
                        measure_type_ = "numeric_overall"
                        data_grouping = "texts"
                    else:
                        raise KeyError("unidentified measute_type")
                    all_texts_measures_ = P.measures.text.aux.makeRoom(all_texts_measures_, data_grouping, measure_group, measure_type_, measure_name)
                    all_texts_measures_[data_grouping][0][measure_group][measure_type_][measure_name] += measure
    all_texts_measures = {}
    for data_grouping in all_texts_measures_:  # "strings" ou "texts"
      for data_group in all_texts_measures_[data_grouping]:  # only one group
        for measure_group in data_group:  # pos
            for measure_type in data_group[measure_group]:  # numeric_overall or pos_tags_overall
                for measure_name in data_group[measure_group][measure_type]:
                    measure = data_group[measure_group][measure_type][measure_name]
                    if measure_type == "pos_tags_overall":
                        tags_histogram = c.Counter(measure)
                        tags_histogram_normalized = {}
                        if tags_histogram:
                            factor = 100.0/sum(tags_histogram.values())
                            for i in tags_histogram:
                                tags_histogram_normalized[i] = tags_histogram[i]*factor
                            tags_histogram_normalized = c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1]))
                        all_texts_measures = P.measures.text.aux.makeRoom(all_texts_measures, data_grouping, measure_group, 'numeric')
                        all_texts_measures[data_grouping][0][measure_group]["numeric"] = tags_histogram_normalized
                    if measure_type == "numeric_overall":
                        mean_name = "M{}".format(measure_name)
                        std_name = "D{}".format(measure_name)
                        all_texts_measures = P.measures.text.aux.makeRoom(all_texts_measures, data_grouping, measure_group, 'second_numeric')
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][mean_name] = n.mean(measure)
                        all_texts_measures[data_grouping][0][measure_group]["second_numeric"][std_name] = n.std(measure)
    return all_texts_measures


def medidasPOS(sentences_tokenized):
    """Measures of POS tags

    Receives a sequence of sentences,
    each as a sequence of tokens.
    Returns a set measures of POS tags,
    and the tagged sentences.

    Convention:
    VERB - verbs (all tenses and modes)
    NOUN - nouns (common and proper)
    PRON - pronouns
    ADJ - adjectives
    ADV - adverbs
    ADP - adpositions (prepositions and postpositions)
    CONJ - conjunctions
    DET - determiners
    NUM - cardinal numbers
    PRT - particles or other function words
    X - other: foreign words, typos, abbreviations
    . - punctuation

    See "A Universal Part-of-Speech Tagset"
    by Slav Petrov, Dipanjan Das and Ryan McDonald
    for more details:
        http://arxiv.org/abs/1104.2086"""
    tagged_sentences = brill_tagger.tag_sents(sentences_tokenized)
    # metric_type: tagged_sentences # metric_name: the_tagged_sentences, measure: `the tag sentences`
    tagged_tokens = [item for sublist in tagged_sentences for item in sublist]
    tags = [i[1] for i in tagged_tokens if i[0].lower() in WORDLIST]
    tags_histogram = c.Counter(tags)
    # metric_type: numeric metric_name: `the pos tag`, measure: percentage of usage
    tags_histogram_normalized = {}
    if tags_histogram:
        factor = 100.0/sum(tags_histogram.values())
        tags_histogram_normalized = {}
        for i in tags_histogram.keys():
            tags_histogram_normalized[i] = tags_histogram[i]*factor
        tags_histogram_normalized = c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1]))
    measures = {"tagged_tokens": {}}
    measures["tagged_tokens"]["the_tagged_tokens"] = tagged_tokens
    measures["numeric"] = tags_histogram_normalized
    return measures
