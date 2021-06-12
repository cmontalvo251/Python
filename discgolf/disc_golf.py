import numpy as np
import matplotlib.pyplot as plt

###Class for Courses
class Course():
	def __init__(self,data_array):
		if len(data_array) == 0:
			#print('Skip empty course')
			self.coursename = None
		else:
			self.coursename = data_array[0][3].rstrip('\n')
			#print('Course Name = ',self.coursename)
			self.holes = []
			##Create holes
			for row in data_array:
				new_hole = Hole(row)
				self.holes.append(new_hole)
	def totalpar(self):
		self.totalpar = 0
		for hole in self.holes:
			self.totalpar += hole.par
		return self.totalpar

	def totallength(self):
		self.totallength = 0
		for hole in self.holes:
			self.totallength += hole.length
		return self.totallength

	def totalholes(self):
		self.totalholes = 0
		for hole in self.holes:
			self.totalholes+=1
		return self.totalholes

	def lengths(self):
		self.lengths = []
		for hole in self.holes:
			self.lengths.append(hole.length)
		self.lengths = np.array(self.lengths)
		return self.lengths

	def pars(self):
		self.pars = []
		for hole in self.holes:
			self.pars.append(hole.par)
		self.pars = np.array(self.pars)
		return self.pars


class Hole():
	def __init__(self,row):
		self.number = row[0]
		self.length = int(row[1])
		self.par = int(row[2])
		#print('New Hole = ',self.number,'Length (ft) = ',self.length,'Par = ',self.par)

####Import Text File of Courses
def importdata(filename):
	courses = []
	file = open(filename)
	data_array = []
	current_course = ''
	for line in file:
		row = line.split('\t')
		coursename = row[3].rstrip('\n')
		if current_course != coursename:
			#print('New Course!!')
			###Send Data Array to Course class
			new_course = Course(data_array)
			if new_course.coursename != None:
				courses.append(new_course)
			###Reset VARS
			current_course = coursename
			data_array = []
		data_array.append(row)
	return courses

###Import text file
courses = importdata('Mobile_Courses.txt')
print('Courses Imported')

###Process a Few things and create numpy arrays for plotting

###PAR LENGTH
totalpar = []
totallength = []
par_length_fig = plt.figure()
par_length_plt = par_length_fig.add_subplot(1,1,1)
par_length_plt.set_xlabel('Total Par')
par_length_plt.set_ylabel('Total Length (ft)')

###INDIVIDUAL HOLES
holes_fig = plt.figure()
holes_plt = holes_fig.add_subplot(1,1,1)
holes_plt.set_xlabel('Hole Length (ft)')
holes_plt.set_ylabel('Par')
holes_plt.grid()


ctr = 0
marker = ['s','o','+','x','D','v','*']
for course in courses:
	print('Course = ',course.coursename)
	print('Total Par = ',course.totalpar())
	print('Total Length (ft) = ',course.totallength())
	print('Total Number of Holes = ',course.totalholes())
	###Plotting Total Par and Length
	totalpar.append(course.totalpar)
	totallength.append(course.totallength)
	par_length_plt.plot(totalpar[-1],totallength[-1],'b*')
	par_length_plt.text(totalpar[-1],totallength[-1],str(course.coursename)+str(' ')+str(course.totalholes))
	###Plotting All the Holes
	holes_plt.plot(course.lengths(),course.pars(),marker[ctr],label=course.coursename)
	ctr+=1
	###Add Text
	for hole in course.holes:
		holes_plt.text(hole.length,hole.par,hole.number)

###LAST BIT OF CLEAN UP
holes_plt.legend()

##CONVERT TO NUMPY ARRAYS
totalpar = np.array(totalpar)
totallength = np.array(totallength)


##MAKE PLOTS
plt.show()
