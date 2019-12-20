#!/usr/bin/python

import sys
import numpy as np
import sympy as sp

##Two ways to run
##you may run this by invoking
##$ python routh_hurwitz.py a2 a1 a0
##from the command line where a2 a1 a0 are the coefficients of the char poly
##or you may edit the string below

#varin = '3 (24-4*kp) (48-4*ki-28*kp) (8*kp-28*ki) (8*ki+168*kp) (168*ki)' ##change this to the coefficients of your char poly if
##you are not using the command line
#varin = '(3-4*kd) (24-28*kd-4*kp) (48+8*kd-28*kp) (8*kp+168*kd) (168*kp)'
#varin = '1 4*kd 4*kp'
#varin = '1 4 (4+40*kd) (40*kp+40*kd) 40*kp'
varin = '4 3 2 5'
#print(np.roots([1,0,5,0,4]))

#kp = 0.01
#kd = 0.05
#varin = '2.8 22.56 48.12 8.48 1.68'

###########DO NOT EDIT BELOW THIS LINE################

#####METHODS AND DEFINITIONS

def get_row(initial_column,length):
    col = initial_column
    row = []
    while col < len(coeff):
        row.append(coeff[col])
        col+=2
    ##Check and see if the last element of row is a zero. If not. append a
    ##zero
    if row[-1] != 0:
        row.append(0)
    #If this is the second row then the length of this row must be the
    #same as the first
    if length > 0:
        while len(row) != length:
            row.append(0)
    return row

def print_first_column(rh,coeff):
    #First get how many rows
    num_rows = len(rh)
    print('Routh Table Complete. Here is the first column.')
    first_column = []
    for x in range(0,num_rows):
        print(rh[x][0])
        print('.....')
        first_column.append(rh[x][0])
    ##If the coefficients are all floats, let's try and compute the
    ##roots
    try:
        roots = np.roots(coeff)
        print('Given polynomial is all floats')
        yesorno = 'yes'
        for x in first_column:
            if np.real(x) < 0:
                yesorno = 'no'
            if np.real(x) == 0:
                yesorno = 'no but could be marginal'
        print('Stable? :',yesorno)
        print('Computing Roots for Verification')
        print('roots = ',roots)
    except:
        print('If all the equations above are positive your system is stable')
    
def get_next_row(rh):
    ##This will take a routh table and compute the next row using
    ##determinants
    ##First we need to grab the last two rows
    last_row = rh[-1]
    second_to_last_row = rh[-2]
    #print('Last Two Rows',last_row,second_to_last_row)
    ##Then we loop through the number of columns and create
    ##determinants. Remember that the determinant is -(a*d - b*c)/e
    #for a routh table row, the a and c variables are always the same
    c = last_row[0]
    a = second_to_last_row[0]
    ##The number we divide by (I'll call it e) is also always the same
    e = last_row[0]
    ##The numbers b and d however change with column so this is where
    ##we loop
    next_row = []
    for column in range(0,len(last_row)):
        if column+1 < len(last_row):
            b = second_to_last_row[column+1]
            d = last_row[column+1]
            ##Once we have our numbers we compute the determinant
            # print(a,b)
            # print(c,d)
            # print(e)
            if e == 0:
                small_number = 1e-10
                print('Zero encountered in Routh Table. Replacing e with',small_number)
                e = small_number
            det = -(a*d - b*c)/e ##We need to be careful though.
            ##If e = 0 we can't do it. if column+1 > len(last_row) we can't do it.
            #If e = 0 we replace with a small number
        else:
            det = 0.
        next_row.append(det)
        
    return next_row

if len(sys.argv) > 1:
    print('Using command line arguments')
    #print(sys.argv[1:])
    coeff_str = ' '.join(map(str,sys.argv[1:]))
else:
    print('Using default value inside code')
    coeff_str = varin

###Extract Coefficients
coeff_split = coeff_str.split(' ')

##Get Order of system
order_system = len(coeff_split)-1

##Convert Coefficients to float if possible if not create variables
coeff = []
for var_str in coeff_split:
    try:
        var_new = np.float(var_str)
    except:
        print('Using symbolic tool box on var = ',var_str)
        var_new = sp.Symbol(var_str)
    coeff.append(var_new)

print('Coefficients of Characteristic Polynomial:',coeff)
print('Order of System = ',order_system)

###Generate Routh Table
routh_table = []

##You always need to generate first two rows even if it's first order
##To generate a row you start with the first element and loop until
##you overflow
first_row = get_row(0,-1)
print('s^',order_system,' Row = ',first_row)
second_row = get_row(1,len(first_row))
print('s^',order_system-1,' Row = ',second_row)

routh_table.append(first_row)
routh_table.append(second_row)

##If the system is first order you're done and you skip to printing
##the 1st column
if order_system == 1:
    print_first_column(routh_table,coeff)
    sys.exit()

##Otherwise it's time to do some determinants
#We're gonna make a method to do this
#We need to loop until order_system-iter is 0
iter = 2
while order_system-iter >= 0:
    next_row = get_next_row(routh_table)
    print('s^',order_system-iter,' Row = ',next_row)
    routh_table.append(next_row)
    iter+=1

#Once the table is complete we can now print the first column
print_first_column(routh_table,coeff)

