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

##Ok give me all the combinations of 'xyz' of length a
possible_digits = '01234'
max_length = 2
print('Possible Digits = ',possible_digits)
print('Maximum Length = ',max_length)
combinations = getCombos(possible_digits,max_length,'').split(',')
combinations.pop()
#combinations.sort()
res = [*set(combinations)]

#print(combinations)
print(res)