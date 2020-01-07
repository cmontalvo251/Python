#!/usr/bin/python

import numpy as np

class Catalog():
    def __init__(self,filename=None,delimiter=None,parent=None):
        self.isstudent = False
        self.delimiter = delimiter
        self.filename = filename
        self.courses = []
        if filename is not None:
            self.readCourses()
            self.computeCredits()

    def computeCredits(self):
        self.total_credits = 0.0
        self.in_progress = 0.0
        for c in self.courses:
            self.total_credits += c.credit_hr
            self.in_progress += c.in_progress
            
    def isCourse(self,row,flag):
        if flag == 2:
            if len(row) > 2:
                for x in [1,2]:
                    if row[x].find('|') != -1:
                        return x
                return -99
            else:
                return -99
        elif flag == 1:
            #Determine if the line is a course
            course_name = row[0]
            if len(course_name) > 3:
                if course_name[2] == ' ' or course_name[2] == 'i' or course_name[2] == 'n':
                    if course_name[0] != 'T':
                        return 0
            return -99

    def displayCourses(self):
        print('Courses:')
        for c in self.courses:
            c.display()
        print('Total Credits = ',self.total_credits)
        if self.isstudent:
            print('Credits In Progress = ',self.in_progress)

    def readCourses(self):
        file = open(self.filename,'r')
        for line in file:
            row = line.split(self.delimiter)
            if self.delimiter == ',':
                flag = 1
            elif self.delimiter == ' ':
                flag = 2
                self.isstudent = True
            x = self.isCourse(row,flag)
            if x != -99:
                self.courses.append(Course(row,x))

class Course():
    def __init__(self,data,idx=0,parent=None):
        #print(data)
        self.in_progress = 0.0
        if idx == 0:
            self.credit_hr = np.float(data[1][0])
        elif idx == 1:
            self.credit_hr = np.float(data[0])
        elif idx == 2:
            self.credit_hr = 0.0
            self.in_progress = np.float(data[1].strip('()'))
        self.course_name = data[idx]
        loc = self.course_name.find('|')
        if loc != -1:
            self.course_name = self.course_name[0:loc]
        
    def display(self):
        print('Course Name = ',self.course_name,'Credits = ',self.credit_hr)

def overlap(student,curriculum):
    ##Loop through the students courses
    remaining = Catalog()
    remaining.courses = curriculum.courses
    remaining.total_credits = curriculum.total_credits
    for c in student.courses:
        #Grab the course Prefix
        loc = 0
        for iter,x in enumerate(c.course_name):
            try:
                y = np.float(x)
            except:
                loc = iter
        #Get rid of lab courses
        if loc != 5: ##That's a lab
            print(c.course_name,c.course_name[0:loc+1],loc)
            #Determine if the course is Gen Ed or Sci
            
        

        
if __name__ == "__main__":

    #Read in the requirements for Mechanical Engineering
    ME = Catalog('ME_Req.csv',',')

    #Display ME required courses for kicks
    ME.displayCourses()

    #Read in the students courses
    student = Catalog('ssc2.txt',' ')

    ##Display Courses Student has taken
    student.displayCourses()
    
    remaining = overlap(student,ME)
    
