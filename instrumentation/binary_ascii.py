##Binary and Decimal
val_10 = 42
val_2 = bin(val_10)

print(str(val_10),' in binary is ',str(val_2))

val_b = '1011'
val_d = int(val_b,2)

print(str(val_b), ' in decimal is ',str(val_d))

##Ascii
phrase = 'Hey this is Carlos!'
print('The ascii for (',phrase,') is: ')
a = []
for letter in phrase:
    a.append(ord(letter))
print (a)

ascii_codes = [76,79,76]
p = []
for code in ascii_codes:
    p.append(chr(code))
print('The following ASCII codes represent this phrase: ',p)
    