import numpy as np
import random as rdm

###Alright let's do this whole thing in python
weeks = 15
num_of_students = 35
max_capacity = 15

###Red, White and Blue schedule (Red = attend on odd weeks (1,3, 5), White = attend on even weeks (2,4,6), Blue = random selection of students per week will stay home)
#Create the student list
student_list = np.arange(1,num_of_students+1)
print(student_list)

student_number = 1
yesnosemester = []
for w in range(0,weeks):
    students = []
    print('Week Number = ',w)
    for s in range(0,max_capacity):
        students.append(student_number)
        student_number+=1
        if student_number > num_of_students:
            student_number = 1
    print(students)
    active_group = students
    active_group.sort()
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
    print(yesnoweek)
    yesnosemester.append(yesnoweek)
    
file = open('Semester.csv','w')
for l in yesnosemester:
    for yn in l:
        file.write(yn)
        file.write(' ')
    file.write('\n')
file.close()
        