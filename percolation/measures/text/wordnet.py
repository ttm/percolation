import collections as c
import numpy as n
import percolation as P
# from nltk.corpus import wordnet as wn
__doc__ = "text analysis with wordnet"


def systemAnalyseAll(sectors_analysis):
    all_texts_measures = {}
    for sector in sectors_analysis:
        for data_grouping in sectors_analysis[sector]["wordnet"]:
            for data_group in sectors_analysis[sector]["wordnet"][data_grouping]:
                for measure_group in data_group:
                    for measure_type in data_group[measure_group]:
                        for measure_name in data_group[measure_group][measure_type]:
                            measure = data_group[measure_group][measure_type][measure_name]
                            if measure_type == "lexnames_overall":  # directly from tokens
                                measure_type_ = "lexnames_overall"
                                data_grouping_ = "strings"
                            elif measure_type == "lengths_overall":  # directly from tokens
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
                    if measure_type != "lexnames_overall":
                        mean_val = n.mean(measure)
                        std_val = n.std(measure)
                        mean_name = "M{}".format(measure_name)
                        std_name = "D{}".format(measure_name)
                    if measure_type == "lexnames_overall":  # directly from strings, data_grouping  ==  "strings"
                        lex_histogram = c.Counter(measure)
                        lex_histogram_normalized = {}
                        if lex_histogram:
                            factor = 100.0/sum(lex_histogram.values())
                            for i in lex_histogram:
                                lex_histogram_normalized[i] = lex_histogram[i]*factor
                        all_texts_measures[data_grouping][0][measure_group]["numeric"].update(lex_histogram_normalized)
                    elif measure_type == "lengths_overall":  # data_grouping  ==  "strings"
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name] = std_val
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
        analysis = authors_analysis[agent]["wordnet"]
        for data_grouping in analysis:
            for data_group in analysis[data_grouping]:
                for measure_group in data_group:
                    for measure_type in data_group[measure_group]:
                        for measure_name in data_group[measure_group][measure_type]:
                            measure = data_group[measure_group][measure_type][measure_name]
                            if measure_type == "lexnames_overall":  # directly from tokens
                                measure_type_ = "lexnames_overall"
                                data_grouping_ = "strings"
                            elif measure_type == "lengths_overall":  # directly from tokens
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
    for data_grouping in all_texts_measures:  # strings, texts, authors, authors_messages
        for data_group in all_texts_measures[data_grouping]:
          for measure_group in data_group:  # pos
            for measure_type in data_group[measure_group]:  # only list/tuple of numbers at first
                for measure_name in all_texts_measures[measure_group][measure_type]:  # `pos tag`, the_tagged_tokens
                    measure = all_texts_measures[measure_group][measure_type][measure_name]
                    if measure_type != "lexnames_overall":
                        mean_val = n.mean(measure)
                        std_val = n.std(measure)
                        mean_name = "M{}".format(measure_name)
                        std_name = "D{}".format(measure_name)
                    if measure_type == "lexnames_overall":  # directly from strings, data_grouping  ==  "strings"
                        lex_histogram = c.Counter(measure)
                        lex_histogram_normalized = {}
                        if lex_histogram:
                            factor = 100.0/sum(lex_histogram.values())
                            for i in lex_histogram:
                                lex_histogram_normalized[i] = lex_histogram[i]*factor
                            lex_histogram_normalized = c.OrderedDict(sorted(lex_histogram_normalized.items(), key=lambda x: -x[1]))
                        all_texts_measures[data_grouping][0][measure_group]["numeric"].update(lex_histogram_normalized)
                    elif measure_type == "lengths_overall":  # data_grouping  ==  "strings"
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][mean_name] = mean_val
                        all_texts_measures[data_grouping][0][measure_group]["numeric"][std_name] = std_val
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


def analyseAll(pos_analysis):
    """Make wordnet text analysis of all texts and of the merged text"""
    # texts_measures=[]
    texts_measures = {"each_text": []}
    for each_pos_analysis in pos_analysis["texts_measures"]["each_text"]:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["wordnet_context"] = contextWordnet(each_pos_analysis['pos']["tagged_tokens"]["the_tagged_tokens"])
        texts_measures["each_text"][-1].update(medidasWordnetPOS(texts_measures['each_text'][-1]["wordnet_context"]))
    del each_pos_analysis
    texts_measures.update(medidasMensagens2(texts_measures['each_text']))
    return locals()


def medidasMensagens2(texts_measures):
    all_texts_measures = {}
    for data_group in texts_measures:  # each_text
        for measure_group in data_group:  # wordnet_context, pos_tag_n _as _v _b
            for measure_type in data_group[measure_group]:  # numeric or list/tuple of strings
                if measure_type == "strings":
                    continue
                for measure_name in data_group[measure_group][measure_type]:  # nchars, frac_x, known_words, etc
                    measure = data_group[measure_group][measure_type][measure_name]
                    if measure_type == "numeric":
                        measure = [measure]
                        measure_type_ = "numeric_overall"
                        data_grouping = "texts"
                    elif measure_type == "lengths":
                        measure_type_ = "legths_overall"
                        data_grouping = "strings"
                    elif measure_type == "lexnames":
                        measure_type_ = "lexnames_overall"
                        data_grouping = "strings"
                    else:
                        raise KeyError("unidentified measure_type")
                    all_texts_measures[data_grouping][0][measure_group][measure_type_][measure_name] += measure

    for data_grouping in all_texts_measures:  # "strings" or "texts"
      for data_group in all_texts_measures[data_grouping]:  # only one group
        for measure_group in data_group:  # wordnet_context, pos_tag_X
            for measure_type in data_group[measure_group]:  # numeric_overall, lengths_overall, lexnames_overall
                for measure_name in data_group[measure_group][measure_type]:
                    measure = data_group[measure_group][measure_type][measure_name]
                    if measure_type == "lexnames_overall":
                        tags_histogram = c.Counter(measure)
                        tags_histogram_normalized = {}
                        if tags_histogram:
                            factor = 100.0/sum(tags_histogram.values())
                            for i in tags_histogram:
                                tags_histogram_normalized[i] = tags_histogram[i]*factor
                            tags_histogram_normalized = c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1]))
                        all_texts_measures[data_grouping][0][measure_group]["numeric"].update(tags_histogram_normalized)
                    else:  # numeric_overall or lengths_overall
                        mean_name = "M{}".format(measure_name)
                        std_name = "D{}".format(measure_name)
                        mean_val = n.mean(measure)
                        std_val = n.std(measure)
                    if measure_type == "lengths_overall":
                        all_texts_measures[measure_group]["numeric"][mean_name] = mean_val
                        all_texts_measures[measure_group]["numeric"][std_name] = std_val
                    elif measure_type == "numeric_overall":
                        all_texts_measures[measure_group]["second_numeric"][mean_name] = mean_val
                        all_texts_measures[measure_group]["second_numeric"][std_name] = std_val
    return all_texts_measures


def contextWordnet(pos_tagged_tokens):
    """Wordnet pos tags"""
    pos_tagged_tokens_lowercase = [(i[0].lower(), i[1]) for i in pos_tagged_tokens]
    tokens_lists = P.measures.text.aux.filtro(pos_tagged_tokens_lowercase)
    tokens_pos_tagger_wordnet_ok = []
    tokens_pos_tagger_wordnet_not_ok = []
    for token in tokens_lists["token_com_synset"]:
        synset = token[2]
        wordnet_pos_tag = [i.pos() for i in synset]
        pos_tag = P.measures.text.aux.traduzPOS(token[1])
        found_ok_wordnet_pos_tag = [(pp in pos_tag) for pp in wordnet_pos_tag]
        if sum(found_ok_wordnet_pos_tag):
            tindex = found_ok_wordnet_pos_tag.index(True)
            tokens_pos_tagger_wordnet_ok.append((token[0], synset[tindex]))
        else:
            tokens_pos_tagger_wordnet_not_ok.append(token)
    wordnet_pos_tags_ok = [i[1].pos() for i in tokens_pos_tagger_wordnet_ok]
    wordnet_pos_tags_ok_histogram_normalized = [100*wordnet_pos_tags_ok.count(i)/len(tokens_pos_tagger_wordnet_ok)
                                                for i in ('n', 's', 'a', 'r', 'v')]
    wordnet_pos_tags_ok_histogram_normalized[1] += wordnet_pos_tags_ok_histogram_normalized[2]
    wordnet_pos_tags_ok_histogram_normalized = wordnet_pos_tags_ok_histogram_normalized[0:2]+wordnet_pos_tags_ok_histogram_normalized[3:]
    # wordnet_pos_tags_ok_histogram_normalized = c.OrderedDict(sorted(wordnet_pos_tags_ok_histogram_normalized.items(), key=lambda x: -x[1]))
    measures = {"tokens_wnsynsets": {}, "numeric": {}}
    measures["tokens_wnsynsets"]["words_pos_tagger_wordnet_ok"] = tokens_pos_tagger_wordnet_ok
    # measures["strings"]["tokens_pos_tagger_wordnet_not_ok"]=tokens_pos_tagger_wordnet_not_ok
    measures["numeric"] = {i: j for i, j in zip(('n', 'sa', 'r', 'v'), wordnet_pos_tags_ok_histogram_normalized)}
    measures["numeric"].update({"frac_pos_tagger_wordnet_ok": len(tokens_pos_tagger_wordnet_ok)/len(pos_tagged_tokens)})
    return measures


def medidasWordnetPOS(wordnet_context, pos_tags=("n", "as", "v", "r")):
    """Make specific measures to each POS tag found TTM"""
    wordnet_measures = {}
    for pos_tag in pos_tags:
        wordnet_measures["pos_tag_"+pos_tag] = medidasWordnet(wordnet_context, pos_tag)
    return wordnet_measures


def medidasWordnet(wordnet_context, pos_tag=None):
    """Medidas das categorias da Wordnet sobre os verbetes TTM"""
    tagged_words = wordnet_context['tokens_wnsynsets']["words_pos_tagger_wordnet_ok"]
    if pos_tag:
        tagged_words_chosen = [i[1] for i in tagged_words if i[1].pos() in pos_tag]
    else:
        tagged_words_chosen = [i[1] for i in tagged_words]
    hyperpaths_word = [i.hypernym_paths() for i in tagged_words_chosen]
    hyperpaths = [i for j in hyperpaths_word for i in j]
    lemmas = [i.lemmas() for i in tagged_words_chosen]

    tmember_holonyms = [i.member_holonyms() for i in tagged_words_chosen]
    part_holonyms = [i.part_holonyms() for i in tagged_words_chosen]
    substance_holonyms = [i.substance_holonyms() for i in tagged_words_chosen]
    holonyms = [i+j+l for i, j, l in zip(tmember_holonyms, part_holonyms, substance_holonyms)]

    tmember_meronyms = [i.member_meronyms() for i in tagged_words_chosen]
    part_meronyms = [i.part_meronyms() for i in tagged_words_chosen]
    substance_meronyms = [i.substance_meronyms() for i in tagged_words_chosen]
    meronyms = [i+j+l for i, j, l in zip(tmember_meronyms, part_meronyms, substance_meronyms)]

    region_domains = [i.region_domains() for i in tagged_words_chosen]
    topic_domains = [i.topic_domains() for i in tagged_words_chosen]
    usage_domains = [i.usage_domains() for i in tagged_words_chosen]
    domains = [i+j+l for i, j, l in zip(region_domains, topic_domains, usage_domains)]

    hypernyms = [i.hypernyms() for i in tagged_words_chosen]
    instance_hypernyms = [i.instance_hypernyms() for i in tagged_words_chosen]
    hypernyms_all = [i+j for i, j in zip(hypernyms, instance_hypernyms)]

    hyponyms = [i.hyponyms() for i in tagged_words_chosen]
    instance_hyponyms = [i.instance_hyponyms() for i in tagged_words_chosen]
    hyponyms_all = [i+j for i, j in zip(hyponyms, instance_hyponyms)]

    entailments = [i.entailments() for i in tagged_words_chosen]
    similar = [i.similar_tos() for i in tagged_words_chosen]
    verb_groups = [i.verb_groups() for i in tagged_words_chosen]

    loc = locals().copy()
    del loc['tagged_words_chosen']
    measures = P.measures.text.aux.mediaDesvio2(loc)
    max_depth = [i.max_depth() for i in tagged_words_chosen]
    min_depth = [i.min_depth() for i in tagged_words_chosen]
    tdict = {"tmax_depth": max_depth, "tmin_depth": min_depth}
    measures["lengths"].update(tdict)
    measures["numeric"].update(P.measures.text.aux.mediaDesvioNumbers(tdict))

    top_hypernyms = [i[:7] for i in hyperpaths]  # para fazer histograma por camada
    measures["extra"] = {}
    measures["extra"]["top_hypernyms"] = top_hypernyms

    lexnames = ["tlex_"+i.lexname().split('.')[1] for i in tagged_words_chosen]  # rever
    measures["lexnames"] = {}
    measures["lexnames"].update({"the_lexnames": lexnames})
    lex_histogram = c.Counter(lexnames)
    lex_histogram_normalized = {}
    if lex_histogram:
        factor = 100.0/sum(lex_histogram.values())
        for i in lex_histogram:
            lex_histogram_normalized[i] = lex_histogram[i]*factor
    measures["numeric"].update(lex_histogram_normalized)

    return measures
