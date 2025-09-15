import time

for i in range(0,1000):
    h = hex(i)
    c = chr(i)
    print('Letter in Character table = ',i,' Hex Value = ',h,' The Character = ',c)
    time.sleep(0.1)
    