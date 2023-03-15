import numpy as np

##Ok I figured it out.
#We need a function that return the possible
#combinations of a set of digits but using recursion
# for example if the possibilities are '012'
# the possible combinations are [0 + combos('12'),1 + combos('02'),2 + combos('01')]

def combos(digits):

    #First, all we do is loop through the keys
    possibilities = []
    for d in digits:
        possibilities.append(d)
        print('Pressing the ',d,' key')
        remaining_digits = digits.replace(d,'')
        print('Remaining Digits',remaining_digits)
        #Then if there are remaining digits we need to loop through combinations
        #of those keys but only if the length of the remaining digits is greater than
        #1
        if len(remaining_digits) >= 1:
            possibilities.append(combos(remaining_digits))
    return possibilities

##Let's test it
possible_digits = '012'
print('Possible Keys')
print(possible_digits)
#print('Possible Combinations')
possibilities = combos(possible_digits)
print(combos(possible_digits))
        
