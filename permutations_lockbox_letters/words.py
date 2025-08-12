###What letters are we permutating????
letters = 'ACEeLORSs'

##Let's figure out how many permutations we have
total_letters = len(letters)
import math as m
permutations = m.factorial(total_letters)
combinations = ['']*permutations

#We need a function to remove letters from letters
def removelettersfromletters(letters,removethese):
    #Ok so we have a list
    #print('All the letters = ',letters)
    #and we need to remove these
    #print('and we need to remove these = ',removethese)
    #Aww crap. but what about eel? That has two e's
    #Return list
    returnlist = letters
    #We need to instead go through the removethese list and remove them from the letters list
    for l in removethese:
        if l in returnlist:
            #This means we found that letter in returnlist
            returnlist = returnlist.replace(l,'',1) #remove that letter only once
    #print('So we are left with these letters = ',returnlist)
    return returnlist

##Ok I think I've got it.

##Add a letter one at a time
for l in range(0,total_letters):
    print('Adding ', l+1 , ' letter')
    ##Loop through all permutations and add a letter to it
    
    #Start at the first letter
    current_letter = 0
    #But the letters are not all the letters right away
    letters2add = letters[l:]
    
    ##Recompute duplicity each time
    duplicity = m.factorial(total_letters-l-1)
    letter_duplicates = 1
    
    for p in range(0,permutations):
        ##Which letter am I adding?
        #print('Adding letter = ',letters2add[current_letter],' Letter Duplicity = ',letter_duplicates,' Adding these letters = ',letters2add)
        combinations[p] += letters2add[current_letter]
        #print(combinations[p],letter_duplicates,duplicity)
        ##Eventually we need to switch to the next letter if we've reached max duplicity
        letter_duplicates += 1
        if letter_duplicates > duplicity:
            current_letter += 1
            letter_duplicates = 1
            #However if we've reached the maximum letters in this loop we need to reset current letter back to zero
            if current_letter == len(letters2add) and p != permutations-1:
                current_letter = 0
                #But also get different letters
                #What we need to do is take combinations[p+1] and remove all those letters from
                #Letters to add. I'm having trouble making this script so let's make a function
                letters2add = removelettersfromletters(letters,combinations[p+1])

##Print to user
print('For the following letters: ',letters)
print('There are ',permutations,' total possibilities')
print('The possibilities are.... ')
print('Too many so we are printing to a file')
print('Before we do that though, some letter combos just do not make sense')
print('So we are going to remove those first....')
combinations_dc = []
for p in combinations:
    remove = False
    if p.find('s') < p.find('S'):
        remove = True
    if p.find('e') < p.find('E'):
        remove = True
    p = p.upper()
    if p[0:2] == 'RS':
        remove = True
    if p[0:2] == 'LR':
        remove = True
    if p[0:2] == 'RL':
        remove = True
    if p[0:2] == 'LS':
        remove = True
    if p[0:2] == 'LC':
        remove = True
    if p[0:2] == 'RC':
        remove = True
    if p[0:3] == 'SLS' or p[0:3] == 'SLC':
        remove = True
    if p[0:4] == 'ACLR':
        remove = True
    if p[0:2] == 'CS' or p[0:2] == 'EE':
        remove = True
    if p[0:2] == 'SS':
        remove = True
    if remove == False:
        combinations_dc.append(p)
print('After removing a few combinations there are')
print(len(combinations_dc),' possibilities')
print('Printing those to file....')
filename = 'words0.txt'
print('Opening = ',filename)
fid = open(filename,'w')
count = 0
filenumber = 0
for p in combinations_dc:
    fid.write(p+'\n')
    count += 1
    if count > 1000000000:
        filenumber += 1
        count = 0
        fid.close()
        filename = 'words'+str(filenumber)+'.txt'
        fid = open(filename,'w')
        print('Opening = ',filename)
fid.close()

"""
if p[0] == 'C' and p[1] == 'D':
        remove = True
    if p[0] == 'N' and p[1] == 'S':
        remove = True
    if p[0] == 'D' and p[1] == 'C':
        remove = True
    if p[0] == 'T' and p[1] == 'S':
        remove = True
    if p[0] == 'C' and p[1] == 'N':
        remove = True
    if p[0] == 'C' and p[1] == 'C':
        remove = True
    if p[0] == 'C' and p[1] == 'S':
        remove = True
    if p[0] == 'C' and p[1] == 'T':
        remove = True
    if p[0] == 'N' and p[1] == 'D':
        remove = True
    if p[0] == 'D' and p[1] == 'N':
        remove = True
"""
