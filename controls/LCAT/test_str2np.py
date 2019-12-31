import numpy as np
import ast

def tostring(input):
    print('Numpy = ',input)
    out = str(input)
    print('String = ',out)
    return out

def tostr(input):
    print('Numpy = ',input)
    s = np.shape(input)
    if len(s) == 1:
        r = s[0]
        c = 0
    else:
        r = s[0]
        c = s[1]
    output = '['
    for ri in range(0,r):
        if ri > 0:
            output+=','
        if c > 0:
            output += '['
            for ci in range(0,c):
                if ci > 0:
                    output += ','
                output+= str(input[ri][ci])
                
            output += ']'
        else:
            output += str(input[ri])
    output+= ']'
    print('String = ',output)
    return output

def tonumpy(input):
    print('String = ',input)
    #Replace commas with space just in case user used commas
    #Replace newline with space
    #We need to remove the brackets no matter what
    blacklist = ['\n',',','[',']']
    for char in blacklist:
        input = input.replace(char,' ')
    try:
        #Try to use the built in function
        output = np.fromstring(input,sep=' ')
    except:
        #If the above does not work it means the input is probably 1d.
        try:
            #Convert to a numpy float
            int_np = np.float(input)
            #Then convert to an array
            output = np.asarray([int_np])
        except:
            #If that didn't work it means the input is bad
            output = None
    print('Output = ',output)
    return output

def toarray(input):
    print('String = ',input)
    input_ = input.replace(' ',',')
    output = np.asarray(ast.literal_eval(input_))
    print('Numpy = ',output)
    return output



oned_np = np.asarray([1])
twod_np = np.asarray([2,3])
array_np = np.asarray([[4,5],[6,7]])

#oned_str = tostring(oned_np)
#twod_str = tostring(twod_np)
#array_str = tostring(array_np)

oned_str = tostr(oned_np)
twod_str = tostr(twod_np)
array_str = tostr(array_np)

#oned_str_np = tonumpy(oned_str)
#twod_str_np = tonumpy(twod_str)
#array_str_np = tonumpy(array_str)

oned_str_np = toarray(oned_str)
twod_str_np = toarray(twod_str)
array_str_np = toarray(array_str)