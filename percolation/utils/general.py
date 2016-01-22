from datetime import datetime
from string import ascii_lowercase
from random import randint, choice
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


