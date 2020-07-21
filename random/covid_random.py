import numpy as np
import random as rdm

###Alright let's do this whole thing in python
weeks = 15
num_of_students = 26
max_capacity = 15

###Red, White and Blue schedule (Red = attend on odd weeks (1,3, 5), White = attend on even weeks (2,4,6), Blue = random selection of students per week will stay home)
#Create the student list
student_list = np.arange(1,num_of_students+1)
print(student_list)

##Shuffle list
shuffled_list = student_list
rdm.shuffle(shuffled_list)

print(shuffled_list)

###Select RED group
midpoint = int(num_of_students/2)
red = shuffled_list[0:midpoint]
white = shuffled_list[midpoint:]


###In the case where both groups only have 15 students you can proceed otherwise you'll have to randomly choose

##Let's sort the red and white arrays
red.sort()
print('red = ',red)
white.sort()
print('white = ',white)
yesnosemester = []
for w in range(1,weeks+1):
    print('Week Number = ',w)
    if w % 2 == 0:
        ##Even week
        ##White
        active_group = white
    else:
        ##Odd week
        ##Red
        active_group = red
    yesnoweek = []
    ctr = 1
    num_yeses = 0
    for a in active_group:
        while ctr < a:
            yesnoweek.append('no')
            ctr+=1
        yesnoweek.append('yes')
        num_yeses+=1
        ctr+=1
    while len(yesnoweek) < num_of_students:
        yesnoweek.append('no')
    if num_yeses > max_capacity:
        print('Overflow')
        blue = len(active_group) - max_capacity
        print('blue = ',blue)
    print(yesnoweek)
    yesnosemester.append(yesnoweek)
    
#print(yesnosemester)

file = open('Semester.csv','w')
for l in yesnosemester:
    for yn in l:
        file.write(yn)
        file.write(' ')
    file.write('\n')
file.close()
        