import os
import pickle
import string
import numpy as n
import nltk as k

STOPWORDS = set(k.corpus.stopwords.words('english'))

wn = k.corpus.wordnet

tpath = os.path.abspath(__file__).replace(os.path.basename(__file__), '')
if 'words.txt' not in os.listdir(tpath):
    print('downloading english words list')
    os.system('wget https://raw.githubusercontent.com/dwyl/english-words/master/words.txt -P {}'.format(tpath))
    # os.system('wget https://raw.githubusercontent.com/dwyl/english-words/master/words.txt {}words.txt'.format(tpath))
    print('finished download')
with open(tpath + 'words.txt') as f:
    WORDLIST = set(f.read())

f = open(tpath+"brill_taggerT2M1", "rb")
brill_tagger = pickle.load(f)


def makeRoom(all_texts_measures, data_grouping, measure_group, measure_type_, measure_name=None):
    '''Make sure the dictionary has the keys for input'''
    if data_grouping not in all_texts_measures:
        all_texts_measures[data_grouping] = [{}]
    if measure_group not in all_texts_measures[data_grouping][0]:
        all_texts_measures[data_grouping][0][measure_group] = {}
    if measure_type_ not in all_texts_measures[data_grouping][0][measure_group]:
        all_texts_measures[data_grouping][0][measure_group][measure_type_] = {}
    if measure_name and measure_name not in all_texts_measures[data_grouping][0][measure_group][measure_type_]:
        all_texts_measures[data_grouping][0][measure_group][measure_type_][measure_name] = []
    return all_texts_measures


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


def textFromAuthors(author_messages, sectorialized_agents):
    authors = set([i[0] for i in author_messages])
    authors_texts = {}
    for author in authors:
        authors_texts[author] = []
    for author, text in author_messages:
        authors_texts[author] += [text]
    return authors_texts


def filtro(pos_tagged_words_lowercase):
    """faz separação dos tokens para analise com wordnet TTM"""
    stopword_sem_synset = []
    stopword_com_synset = []
    token_com_synset = []
    token_sem_synset = []
    pontuacao = []
    token_exotico = []
    for pos_tagged_word in pos_tagged_words_lowercase:
        synset = wn.synsets(pos_tagged_word[0])
        if synset:
            if pos_tagged_word[0] in STOPWORDS:
                stopword_com_synset.append(pos_tagged_word)
            else:
                token_com_synset.append((pos_tagged_word[0], pos_tagged_word[1], synset))
        elif sum([tt in string.punctuation for tt in pos_tagged_word[0]]) == len(pos_tagged_word[0]):
            pontuacao.append(pos_tagged_word)
        elif pos_tagged_word[0] in STOPWORDS:
            stopword_sem_synset.append(pos_tagged_word)
        elif pos_tagged_word[0] in WORDLIST:
            token_sem_synset.append(pos_tagged_word)
        else:
            token_exotico.append(pos_tagged_word)
    del pos_tagged_word, synset, pos_tagged_words_lowercase
    return locals()


def mediaDesvioNumbers(adict={"stringkey": "strings_list"}):
    tdict = {}
    for key in adict:
        tdict["m"+key] = n.mean(adict[key])
        tdict["d"+key] = n.std(adict[key])
    return tdict


def traduzPOS(astring):
    """Traduz as POS tags usadas para a convenção do Wordnet"""
    if astring in ("NOUN", "NNS", "NN", "NUM"):
        return wn.NOUN
    elif astring in ("VERB", "VBG"):
        return wn.VERB
    elif astring in ("ADJ", "JJ", "ADP"):
        return wn.ADJ+wn.ADJ_SAT
    elif astring in ("ADV", "RB", "PRT"):
        return wn.ADV
    else:
        return "NOPOS"
