import numpy as np

words = ['increase','yesterday','acquaint','achievement','reproach','marrow','virtue','continue','betray','array','campaign','revenue','meadow','deceive','appeal','agreement','streamline','proceed','remainder','straight','mayonnaise','reasonable','conceited']

def num_occurences(word,v):
    num = 0
    loc = 0
    l = len(word)
    while loc != -1:
        loc = word.find(v)
        if loc != -1:
            num+=1
            if loc == len(word):
                loc = -1
            else:
                word = word[loc+1:]
    return num

def count_vowels(word):
    vowels = 'aeiou'
    num = 0
    for v in vowels:
        num+=num_occurences(word,v)
    return num

for word in words:
    #print(word)
    #Find the number of letter
    wt = len(word)
    ##Find the vowels
    num_vowels = count_vowels(word)
    #print('Number of Vowels = ',num_vowels)
    #Cononants are just the remainder
    consonants = wt - num_vowels
    #Compute Money
    money = num_vowels * 0.25 + consonants * 0.15
    print(word,num_vowels,consonants,money)
    