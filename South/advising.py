#!/usr/bin/python

import numpy as np
from PyQt4 import QtGui, QtCore
import sys
from mainwindow import Ui_MainWindow
import copy as cpy

class MainWindow(QtGui.QMainWindow):
    '''Main window class responsible for managing user interface'''
    def __init__(self,v=True,parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.verbose = v
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Read in the requirements for Mechanical Engineering
        self.ME = Catalog('ME Curriculum','ME_Req.csv',',')
        self.ME.addCourse('CH131L',0)

        #Display ME required courses for kicks
        #self.ME.displayCourses()

        self.student = False

        #Fill textEdits
        self.fillTextEdits()
        
        #Connect Slots
        QtCore.QObject.connect(self.ui.pushButton,QtCore.SIGNAL('clicked()'),self.IMPORT)

    def IMPORT(self):
        value = str(QtGui.QFileDialog.getOpenFileNameAndFilter(caption='Select Desired Transcript for import',filter='txt (*.txt)')[0]).rstrip()
        #Read in the students courses
        self.student = Catalog('Student',value,' ')

        ##Display Courses Student has taken
        #student.displayCourses()

        #Compute courses which still need to be taken
        self.remaining = overlap(self.student,self.ME)
        #remaining.displayCourses()
        
        self.fillTextEdits()
        
    def fillTextEdits(self):
        self.ui.textEdit.setText('')
        text = ''
        for c in self.ME.courses:
            text+=c.course_name+'\n'
        self.ui.textEdit.setText(text)
        if self.student:
            self.ui.textEdit_2.setText('')
            text2 = ''
            for c in self.student.courses:
                text2+=c.course_name+'\n'
            self.ui.textEdit_2.setText(text2)
            self.ui.textEdit_3.setText('')
            text3 = ''
            for c in self.remaining.courses:
                text3+=c.course_name+'\n'
            self.ui.textEdit_3.setText(text3)

class Catalog():
    def __init__(self,name,filename=None,delimiter=None,parent=None):
        self.name = name
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

    def addCourse(self,course_name,credit_hr):
        data = [str(credit_hr),course_name]
        self.courses.append(Course(data,1))
            
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
        print(self.name + ':')
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

    def pop(self,check):
        pop = False
        #print('Checking = ',check)
        for iters,d in enumerate(self.courses):
            if d.course_name in check:
                #print('Science Elective')
                self.courses.pop(iters)
                self.total_credits -= d.credit_hr
                pop = True
                break
        return pop

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
        self.course_name = self.course_name.replace(' ','')
        
    def display(self):
        print('Course Name = ',self.course_name,'Credits = ',self.credit_hr)

def overlap(student,curriculum):
    ##Loop through the students courses
    intersection = Catalog('Remaining Courses')
    intersection.courses = cpy.deepcopy(curriculum.courses)
    intersection.total_credits = cpy.deepcopy(curriculum.total_credits)
    for c in student.courses:
        #Grab the course Prefix
        loc = 0
        for iter,x in enumerate(c.course_name):
            try:
                y = np.float(x)
                break
            except:
                loc = iter
        #Get rid of lab courses
        if loc != 6: ##That's a lab
            prefix = c.course_name[0:loc+1]
            core = False
            gen_ed = False
            scitech_el = False
            ##Determine what block the class falls in
            if prefix in ['EH','MA','PH','MA','ME','CH','CA','EG']:
                core = True
            elif prefix in ['HY','ARS','CAS','ECO','MUS','PSC','MUL']:
                gen_ed = True
            elif prefix in ['CSC','CIS','ST']:
                scitech_el = True
            me_el = False
            pop = False
            if core:
                core = False
                #print('Core Course Detected')
                #Search through the courses until you find it
                pop = intersection.pop([c.course_name])
                if pop:
                    core = True
                if not core:
                    #print('Not a core')
                    #These are going to have to be hardcoded on a case by case basis with
                    #substitutions. This is where things get complex
                    #So far here are the discrepancies
                    #EH225,EH215 - this is actually a gen_ed course
                    if c.course_name in ['EH225','EH215']:
                        #print('Actually Gen Ed')
                        #print('EH225 found')
                        core = False
                        gen_ed = True
                    #MA113 and MA112 are remedial math courses and don't count towards anything
                    if c.course_name in ['MA112','MA113']:
                        #print('Remedial Math')
                        core = False
                    if c.course_name in ['CA100']:
                        #print('Not sure what CA100 is')
                        #I think CA100 is EG101?
                        pop = intersection.pop(['EG101'])
                    if prefix == 'ME':
                        #This is a ME Elective
                        me_el = True
            if gen_ed:
                #print('Checking Gen Ed',gen_ed)
                pop = intersection.pop(['GenEd*','GenEd'])
            if scitech_el:
                #print('Checking Science and Tech Electives')
                pop = intersection.pop(['ScienceElective+'])
            if me_el:
                pop = intersection.pop(['MEElective**','MEElectiveorTechnicalElective'])
            if not pop:
                print('Missed this course')
                print(c.course_name,c.course_name[0:loc+1],c.credit_hr,core,gen_ed,scitech_el)
    return intersection    
        
if __name__ == "__main__":

    ##Create Main Window
    app = QtGui.QApplication(sys.argv)
    main = MainWindow(False) ##Set false so we supress the output
    main.show()
    main.raise_()

    #quit program on exit
    sys.exit(app.exec_())

    
