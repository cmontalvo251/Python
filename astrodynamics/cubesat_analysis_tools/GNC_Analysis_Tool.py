########################################################
#   NAME OF SOFTWARE
#   WHO WROTE IT
#   LAST EDIT DATE
#   LIST OF INPUTS
#   LIST OF OUTPUTS
#   DIRECTIONS ON HOW TO RUN
#   DESCRIPTION OF SOFTWARE
#   
#########################################################

###Modules
import numpy as np

class CubeSat():
	def __init__(input):
		self.input = input
		self.Analysis()

	def Analysis(self):
		self.mag_report = self.Magnetorquer_Analysis()
		self.desat_report = self.Desaturization_Analysis()
		self.rw_report = self.Reaction_Wheel_Analysis()

	def Magnetic_Field_Model_Comparison(self):
		##do we need this?
		## IGRF vs WMM2015

	def Magnetorquer_Analysis(self):
		###Given inertia and orbit compute mag effectivness over 
		###1 orbit

		##First compute reaction wheel size

		##Then figure out how much momentum is in the wheels when saturated

		##Then compute the minimum size magTorquers that will remove momentum from the RWs in 1 orbit

		##Then add a safety factor so they actually detumble in a reasonable amount of time.

		##This is the range where the magTs are effective

		#return output
		return output

	def Desaturization_Analysis(self):
		return output

	def Orbit_Analysis(self):
		##Maybe?

	def Disturbance_Torques(self):
		##Compute the disturbance torques based on orbit
		self.d_torques = np.asarray([0,0,0])

	def Reaction_Wheel_Analysis(self):
		##Given inertia
		##Compute reaction wheels that will provide the necessary momentum storage
		##Based on disturbance torques
		##Can compute number of times during mission to desaturate?
		return output

####Example script

## Example Inputs
example_inputs = np.loadtxt('ABEX_Data_File.txt')

## Run the function above



### print the output