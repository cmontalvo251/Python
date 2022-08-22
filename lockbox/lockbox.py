##Ok give me all the combinations of '01234' of length 2
possible_digits = '01234'
print('Possible Digits',possible_digits)
max_length = 3
print('Maximum Code length = ',max_length)

print('Possible Combinations')
##Length of 2 so let's grab the first digit
combinations = []
for first_digit in possible_digits:
    combination = first_digit
    #We can't press the same key twice so we need to remove the first digit
    remaining_digits = possible_digits.replace(first_digit,'')
    for second_digit in remaining_digits:
        ##Again can't press the same key twice so we remove the first digit
        rem_remaining_digits = remaining_digits.replace(second_digit,'')
        for third_digit in rem_remaining_digits:
            ##We need to sort so we remove repeats
            combination = sorted(first_digit+second_digit+third_digit)
            combo  = ''
            for c in combination:
                combo+=c
            combinations.append(combo)

##Need to remove repeats
#First zero out the repeats
ctr = 0
for combo in combinations:
    second_ctr = 0
    for repeat_combo in combinations:
        if ctr != second_ctr and combo == repeat_combo:
            combinations[second_ctr] = '00'
        second_ctr+=1
    ctr+=1
##Then remove the '00'
nonrepeat_combos = []
for combo in combinations:
    if combo != '00':
        nonrepeat_combos.append(combo)

##Then print result!
for combo in nonrepeat_combos:
    print(combo)