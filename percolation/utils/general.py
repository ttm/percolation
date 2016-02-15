from datetime import datetime
from string import ascii_lowercase
from random import randint, choice
import pickle, re
def randomNick():
    vowels="aeiouy"
    consonants="".join(i for i in ascii_lowercase if i not in vowels)
    nsyllables=randint(2,5)
    nick="".join(i for j in range(nsyllables) for i in (choice(consonants),choice(vowels)))
    if randint(0,1):
       nick=choice(vowels)+nick
    now=datetime.now()
    nick+=str(now.hour)+str(now.minute)
    return nick

def uniqueItems(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
def twitterReadPickle(filename):
    """pickle read for the Dumper class"""
    objs=[]
    with open(filename,"rb") as f:
        while 1:
            try:
                objs.append(pickle.load(f))
            except EOFError:
                break
    return objs
def twitterReadPickleChunck(filename=None,tweets=[],fopen=None,ntweets=5000):
    """Read ntweets from filename or fopen and add them to tweets list"""
    if not fopen:
        f=open(filename,"rb")
    else:
        f=fopen
    #while len(tweets)<9900:
    while len(tweets)<ntweets:
        try:
            tweets+=pickle.load(f)
        except EOFError:
            break
    return tweets,f
rstring="[{}]".format("".join(chr(i) for i in list(range(9))+list(range(11,32))+[127]))
reclean=re.compile(rstring)
def cleanText(text):
    return reclean.sub(r"",text)
