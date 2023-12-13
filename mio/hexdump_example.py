file = open('test.txt')
all = file.read()
print('Counter | Character | ASCII | HEX   |')
print('=====================================')
ctr = 0
for c in all:
    l = len(str(ord(c)))
    spaces = 4-l
    l2 = len(str(ctr))
    s2 = 6-l2
    print(ctr,s2*' ','|',c,'        |',ord(c),spaces*' ','|',hex(ord(c)),' |')
    ctr+=1