########################################################
#   NAME OF SOFTWARE
#   WHO WROTE IT
#   LAST EDIT DATE
#   LIST OF INPUTS
#   LIST OF OUTPUTS
#   DIRECTIONS ON HOW TO RUN
#   DESCRIPTION OF SOFTWARE
#########################################################

###Modules
import numpy as np
import Orbit as O

###Classes
class CubeSat():
    def __init__(self,FS,Ixx,Iyy,Izz,wmax,length,width,height,Mission_Duration,CD,rp,ra):
        self.Orbit_Analysis()
        #self.Magnetic_Field_Model_Comparison()
        self.Disturbance_Torques()
        self.Reaction_Wheel_Analysis()
        #self.Magnetorquer_Analysis()
        
    def Orbit_Analysis(self):
        orbit = O.Earth_Orbit(ra,rp)
        orbit.Numerical_Orbit(1000)
        orbit.make_plots()
        
    #def Magnetic_Field_Model_Comparison(self):
        ##do we need this?
        ## IGRF vs WMM2015
        ##After doing some research, it seems the WMM is the best option.
        ##This is because the WMM is produced for the US and UK defense agencies with guaranteed support and updates.
        ##https://www.ngdc.noaa.gov/geomag/faqgeom.shtml#:~:text=What%20is%20the%20difference%20between%20IGRF%20and%20WMM%20models%3F,-The%20World%20Magnetic&text=The%20WMM%20is%20a%20predictive,for%20the%20years%201900.0%20%2D%202020.0.

    def Disturbance_Torques(self):
        ##Compute the disturbance torques based on orbit
        ##solar radiation pressure
        rad_pressure = 4.5e-6 # Pa
        ##use this to compute torque on body
        Surface_Area = height*width
        solar_rad_force = Surface_Area*rad_pressure
        solar_rad_torque = solar_rad_force*np.max([height/2.0,width/2.0])
        #print('Solar Rad Torque = ',solar_rad_torque)
        ##aerodynamic torques
        
        ##gravity gradient torque
        
        ##magnetic resonance dipole
        
        ##disturbance torques per axis
        Disturbance_Torques = solar_rad_torque#+aero_torque+grav_torque+mag_res_dipole
        Disturbance_Torques_per_axis = Disturbance_Torques/np.sqrt(3)
        self.d_torques = np.asarray([Disturbance_Torques_per_axis,Disturbance_Torques_per_axis,Disturbance_Torques_per_axis])
        return self.d_torques
        
    def Reaction_Wheel_Analysis(self):
        ##Given inertia
        ##Compute reaction wheels that will provide the necessary momentum storage
        wx = wmax*np.pi/180.0
        wy = wmax*np.pi/180.0
        wz = wmax*np.pi/180.0
        
        I = np.asarray([Ixx,Iyy,Izz])
        w = np.asarray([wx,wy,wz])
        H = I*w
        self.Hreq = H*FS
        ##Based on disturbance torques
        ##Can compute number of times during mission to desaturate?
        Hreq_X = self.Hreq[0]
        Hreq_Y = self.Hreq[1]
        Hreq_Z = self.Hreq[2]
        
        #X-axis
        Disturbance_Torques_X = self.d_torques[0]
        Angular_Accel_X = Disturbance_Torques_X/Ixx #rad/s
        Max_Angular_Velocity_X = Hreq_X/Ixx #rad/s
        Time_to_Sat_sec_X = Max_Angular_Velocity_X/Angular_Accel_X #sec
        Time_to_Sat_Months_X = ((Time_to_Sat_sec_X/3600.0)/24.0)/30.0 #months
        Number_of_Desat_Man_X = Mission_Duration/Time_to_Sat_Months_X
        Number_of_Desat_Man_Estimation_X = np.ceil(Number_of_Desat_Man_X)
        
        #Y-axis
        Disturbance_Torques_Y = self.d_torques[1]
        Angular_Accel_Y = Disturbance_Torques_Y/Iyy #rad/s
        Max_Angular_Velocity_Y = Hreq_Y/Iyy #rad/s
        Time_to_Sat_sec_Y = Max_Angular_Velocity_Y/Angular_Accel_Y #sec
        Time_to_Sat_Months_Y = ((Time_to_Sat_sec_Y/3600.0)/24.0)/30.0 #months
        Number_of_Desat_Man_Y = Mission_Duration/Time_to_Sat_Months_Y
        Number_of_Desat_Man_Estimation_Y = np.ceil(Number_of_Desat_Man_Y)
        
        #Z-axis
        Disturbance_Torques_Z = self.d_torques[2]
        Angular_Accel_Z = Disturbance_Torques_Z/Izz #rad/s
        Max_Angular_Velocity_Z = Hreq_Z/Izz #rad/s
        Time_to_Sat_sec_Z = Max_Angular_Velocity_Z/Angular_Accel_Z #sec
        Time_to_Sat_Months_Z = ((Time_to_Sat_sec_Z/3600.0)/24.0)/30.0 #months
        Number_of_Desat_Man_Z = Mission_Duration/Time_to_Sat_Months_Z
        Number_of_Desat_Man_Estimation_Z = np.ceil(Number_of_Desat_Man_Z)
        
        self.Desat_Mans = np.asarray([Number_of_Desat_Man_Estimation_X,Number_of_Desat_Man_Estimation_Y,Number_of_Desat_Man_Estimation_Z])
        print('Momentum Required (Nms) = ',self.Hreq)
        print('Number of Desaturation Maneuvers = ',self.Desat_Mans)
        return self.Hreq,self.Desat_Mans

    #def Magnetorquer_Analysis(self):
        ###Given inertia and orbit compute mag effectivness over 
        ###1 orbit

        ##First compute reaction wheel size

        ##Then figure out how much momentum is in the wheels when saturated

        ##Then compute the minimum size magTorquers that will remove momentum from the RWs in 1 orbit

        ##Then add a safety factor so they actually detumble in a reasonable amount of time.

        ##This is the range where the magTs are effective

        #return self.effectiveness

##Inputs
example_inputs = np.loadtxt('ABEX_Data_File.txt')

FS = example_inputs[0] #factor of safety

Ixx = example_inputs[1] #kg-m^2
Iyy = example_inputs[2]
Izz = example_inputs[3]

wmax = example_inputs[4] #deg/s - Not sure where this comes from

length = example_inputs[5]/100.0 #meters
width = example_inputs[6]/100.0
height = example_inputs[7]/100.0

Mission_Duration = example_inputs[8] #months

CD = example_inputs[9] #Drag

rp = example_inputs[10] #perigee
ra = example_inputs[11] #apogee

##Run the function above
GNC = CubeSat(FS,Ixx,Iyy,Izz,wmax,length,width,height,Mission_Duration,CD,rp,ra)