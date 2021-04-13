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
import matplotlib.pyplot as plt
import igrf

###Functions
def RiemannSum(x,t):
    out = 0.0
    for i in range(1,len(t)):
        out += x[i]*(t[i]-t[i-1])
    return out

def Grav(x,Mass,Grav_Coeff,Mass_Earth,Rad_Earth): 
    Grav_Accel = Grav_Coeff*Mass_Earth/(Rad_Earth + x*1000.0)**2 #Is altitude in m or km???
    #print(Grav_Accel)
    Grav_Force = Grav_Accel*Mass
    #print(Grav_Force)
    return Grav_Force

###Class
class CubeSat():
    def __init__(self,FS,Ixx,Iyy,Izz,wmax,length,width,height,Mission_Duration,CD,rp,ra,Mass_Sat):
        self.FS = FS
        self.Ixx = Ixx
        self.Iyy = Iyy
        self.Izz = Izz
        self.wmax = wmax
        self.length = length
        self.width = width
        self.height = height
        self.Mission_Duration = Mission_Duration
        self.CD = CD
        self.rp = rp
        self.ra = ra
        self.Mass_Sat = Mass_Sat
        self.Orbit_Analysis()
        #self.Magnetic_Field_Model_Comparison()
        self.Disturbance_Torques()
        self.Reaction_Wheel_Analysis()
        #self.Magnetorquer_Analysis()
        
    def Orbit_Analysis(self):
        #Make sure this is working properly
        orbit = O.Earth_Orbit(self.ra,self.rp)
        orbit.Numerical_Orbit(1000)
        #Get time as a vector to use later on
        self.time = orbit.t #sec
        self.altitude = orbit.alt
        self.Grav_Coeff = orbit.G
        self.Mass_Earth = orbit.MEarth
        self.Rad_Earth = orbit.REarth
        #Print plots of orbit
        #orbit.make_plots()
        return self.time,self.altitude
        
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
        Surface_Area = self.height*self.width #m^2
        solar_rad_force = Surface_Area*rad_pressure #N
        solar_rad_torque = solar_rad_force*np.max([self.height/2.0,self.width/2.0]) #Nm
        ang_accel_solar = solar_rad_torque/self.Ixx #rad/s^2
        gamma = ang_accel_solar*self.time
        ang_vel_solar = RiemannSum(gamma,self.time)
        print(ang_vel_solar)
        #plt.figure()
        #plt.plot(self.time,gamma)
        #plt.grid()
        #plt.xlabel('Time (sec)')
        #plt.ylabel('Angular Velocity (rad/s)')
        #plt.show()        
        ##aerodynamic torques
        
        ##gravity gradient torque
        Grav_Force = Grav(self.altitude,self.Mass_Sat,self.Grav_Coeff,self.Mass_Earth,self.Rad_Earth)
        print(Grav_Force)
        plt.figure()
        plt.plot(self.altitude/1000.0,Grav_Force)
        plt.grid()
        plt.xlabel('Altitude (km)')
        plt.ylabel('Gravitational Force (N)')
        plt.show()
        
        ##magnetic resonance dipole
        
        ##disturbance torques per axis
        Disturbance_Torques = solar_rad_torque#+aero_torque+grav_torque+mag_res_dipole
        Disturbance_Torques_per_axis = Disturbance_Torques/np.sqrt(3)
        self.d_torques = np.asarray([Disturbance_Torques_per_axis,Disturbance_Torques_per_axis,Disturbance_Torques_per_axis])
        return self.d_torques
        
    def Reaction_Wheel_Analysis(self):
        ##Compute reaction wheels that will provide the necessary momentum storage
        wx = self.wmax*np.pi/180.0
        wy = self.wmax*np.pi/180.0
        wz = self.wmax*np.pi/180.0      
        I = np.asarray([self.Ixx,self.Iyy,self.Izz])
        w = np.asarray([wx,wy,wz])
        H = I*w
        self.Hreq = H*self.FS
        ##Based on disturbance torques
        ##Can compute number of times during mission to desaturate?
        Hreq_X = self.Hreq[0]
        Hreq_Y = self.Hreq[1]
        Hreq_Z = self.Hreq[2]    
        #X-axis
        Disturbance_Torques_X = self.d_torques[0]
        Angular_Accel_X = Disturbance_Torques_X/self.Ixx #rad/s
        Max_Angular_Velocity_X = Hreq_X/self.Ixx #rad/s
        Time_to_Sat_sec_X = Max_Angular_Velocity_X/Angular_Accel_X #sec
        Time_to_Sat_Months_X = ((Time_to_Sat_sec_X/3600.0)/24.0)/30.0 #months
        Number_of_Desat_Man_X = self.Mission_Duration/Time_to_Sat_Months_X
        Number_of_Desat_Man_Estimation_X = np.ceil(Number_of_Desat_Man_X)   
        #Y-axis
        Disturbance_Torques_Y = self.d_torques[1]
        Angular_Accel_Y = Disturbance_Torques_Y/self.Iyy #rad/s
        Max_Angular_Velocity_Y = Hreq_Y/self.Iyy #rad/s
        Time_to_Sat_sec_Y = Max_Angular_Velocity_Y/Angular_Accel_Y #sec
        Time_to_Sat_Months_Y = ((Time_to_Sat_sec_Y/3600.0)/24.0)/30.0 #months
        Number_of_Desat_Man_Y = self.Mission_Duration/Time_to_Sat_Months_Y
        Number_of_Desat_Man_Estimation_Y = np.ceil(Number_of_Desat_Man_Y)
        #Z-axis
        Disturbance_Torques_Z = self.d_torques[2]
        Angular_Accel_Z = Disturbance_Torques_Z/self.Izz #rad/s
        Max_Angular_Velocity_Z = Hreq_Z/self.Izz #rad/s
        Time_to_Sat_sec_Z = Max_Angular_Velocity_Z/Angular_Accel_Z #sec
        Time_to_Sat_Months_Z = ((Time_to_Sat_sec_Z/3600.0)/24.0)/30.0 #months
        Number_of_Desat_Man_Z = self.Mission_Duration/Time_to_Sat_Months_Z
        Number_of_Desat_Man_Estimation_Z = np.ceil(Number_of_Desat_Man_Z)
        #Print Momentum Storage of RW
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

Mass_Sat = example_inputs[12]

##Run the function above
GNC = CubeSat(FS,Ixx,Iyy,Izz,wmax,length,width,height,Mission_Duration,CD,rp,ra,Mass_Sat)