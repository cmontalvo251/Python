import numpy as np

###RECURSION FUNCTIOn
def getCombos(possible_digits,max_length,pressed_digits):
    ##First we check to see what the maximum length is
    if max_length == 0:
        #Once we are at a maximum length of 0 it means we've pressed all the keys
        #First we sort the keys pressed from 0 to 1 but this returns a list
        combination = sorted(pressed_digits)
        #combination = pressed_digits
        #So we need to make a string
        combo = ''
        for c in combination:
            combo+=c
        return combo+',' #Return an array for the append routine
    else:
        combinations = ''
        for digit in possible_digits:
            current_combo = pressed_digits + digit
            #We can't press the same key twice so we need to remove the first digit
            remaining_digits = possible_digits.replace(digit,'')
            #Then get the combinations with the remaining digits
            combinations += getCombos(remaining_digits,max_length-1,current_combo)
        #Once the loop is over we return the combinations
        return combinations

def inverse(possible_digits,combo):
    icombo = possible_digits
    for c in combo:
        icombo = icombo.replace(c,'')
    return icombo

def printSpecificLength(possible_digits,max_length,numcombo,invert):
    ##Ok give me all the combinations of 'xyz' of length a
    print('Maximum Length = ',max_length)
    print('Getting Combinations....')
    combinations = getCombos(possible_digits,max_length,'').split(',')
    combinations.pop()
    print('Done.')
    ####Need to remove repeats
    nonrepeat_combos = [*set(combinations)]
    ##Then print result!
    icom = 1
    for combo in nonrepeat_combos:
        ##If invert is true we need to invert each combination
        if invert:
            icombo = inverse(possible_digits,combo)
            print(numcombo,' ',combo,' (',icombo,') ',icom)
        else:
            print(numcombo,' (',combo,') ',icom)
        icom+=1
        numcombo+=1
    return numcombo

######################
#possible_digits = '0123456789*'
possible_digits = '134780*'
length = len(possible_digits)
print('Possible Digits',possible_digits)
numcombo = 1
for l in range(1,length+1):
    if length-l < np.floor(length/2):
        print('Running Inverse')
        numcombo = printSpecificLength(possible_digits,length-l,numcombo,1)
    else:
        numcombo = printSpecificLength(possible_digits,l,numcombo,0)
