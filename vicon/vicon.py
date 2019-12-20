#!/usr/bin/python

from pdf import *
import sixdof as sdof
import plotting as P
import mio as I
import sys
import mymath as M

class Body():
    def __init__(self,numMarkers):
        self.numMarkers = numMarkers
        self.frame = []
        self.t = []
        self.x = []
        self.y = []
        self.z = []
        self.xdot = []
        self.ydot = []
        self.zdot = []
        self.phi = []
        self.theta = []
        self.psi = []
        self.p = []
        self.q = []
        self.r = []
        self.markers = []
        for i in range(0,numMarkers):
            m = Marker()
            self.markers.append(m)
            
    def rigid_body(self):
        #For X,Y,Z we should be able to just average all the markers
        self.x = np.copy(self.markers[0].x)
        for i in range(1,self.numMarkers):
            self.x += self.markers[i].x
        self.x /= self.numMarkers        

        self.y = np.copy(self.markers[0].y)
        for i in range(1,self.numMarkers):
            self.y += self.markers[i].y
        self.y /= self.numMarkers

        self.z = np.copy(self.markers[0].z)
        for i in range(1,self.numMarkers):
            self.z += self.markers[i].z
        self.z /= self.numMarkers

        #However, Once we do that we need to substract the cg otherwise our phi,theta psi algorithm
        #won't work
        for i in range(0,self.numMarkers):
            self.markers[i].x -= self.x[0]
            self.markers[i].y -= self.y[0]
            self.markers[i].z -= self.z[0]
        #we then need to do the same with x y z
        self.x -= self.x[0]
        self.y -= self.y[0]
        self.z -= self.z[0]

        #Same with xdot,ydot,zdot
        self.xdot = np.copy(self.markers[0].xdot)
        for i in range(1,self.numMarkers):
            self.xdot += self.markers[i].xdot
        self.xdot /= self.numMarkers
        #self.xdot -= self.xdot[0]

        self.ydot = np.copy(self.markers[0].ydot)
        for i in range(1,self.numMarkers):
            self.ydot += self.markers[i].ydot
        self.ydot /= self.numMarkers
        #self.ydot -= self.ydot[0]

        self.zdot = np.copy(self.markers[0].zdot)
        for i in range(1,self.numMarkers):
            self.zdot += self.markers[i].zdot
        self.zdot /= self.numMarkers
        #self.zdot -= self.zdot[0]

        #Same with xddot,yddot,zddot
        self.xddot = np.copy(self.markers[0].xddot)
        for i in range(1,self.numMarkers):
            self.xddot += self.markers[i].xddot
        self.xddot /= self.numMarkers
        #self.xddot -= self.xddot[0]

        self.yddot = np.copy(self.markers[0].yddot)
        for i in range(1,self.numMarkers):
            self.yddot += self.markers[i].yddot
        self.yddot /= self.numMarkers
        #self.yddot -= self.yddot[0]

        self.zddot = np.copy(self.markers[0].zddot)
        for i in range(1,self.numMarkers):
            self.zddot += self.markers[i].zddot
        self.zddot /= self.numMarkers
        #self.zddot -= self.zddot[0]

        #Now we need to get phi_theta_psi
        #First we need to generate the matrix R of markers
        self.RB = np.zeros([3,self.numMarkers])
        self.vec3 = np.zeros([3])
        #What we do is assume the first frame is at 0,0,0
        for i in range(0,self.numMarkers):
            self.vec3[0] = self.markers[i].x[0]
            self.vec3[1] = self.markers[i].y[0]
            self.vec3[2] = self.markers[i].z[0]
            self.RB[:,i] = self.vec3
        #print self.RB

        #To figure out the stuffs below we need to compute (RB^T)*(RB*RB^T)^-1
        #Here we go
        self.RVICON = np.matmul(np.transpose(self.RB),np.linalg.inv(np.matmul(self.RB,np.transpose(self.RB))))
        #print(self.RVICON)

        #Ok now we need to loop through all frames and compute phi-theta-psi
        self.Rhat = np.zeros([3,self.numMarkers])
        self.vec3 = np.zeros([3])
        for f in range(0,len(self.x)):
            #print 'Frame = ',f
            #So the algorithm goes likes this
            #TIB_star = (Rhat - Rcg)*(RB^T)*(RB*RB^T)^-1
            #RB is the vector from the cg to the Body frame which is a constant and
            #has been obtained above. Since RB is a constant (RB^T)*(RB*RB^T)^-1 we
            #can compute it above
            #Rhat is the vector of current markers
            #so let's generate that now. thing is we can just substract Rcg right away
            for i in range(0,self.numMarkers):
                self.vec3[0] = self.markers[i].x[f]-self.x[f]
                self.vec3[1] = self.markers[i].y[f]-self.y[f]
                self.vec3[2] = self.markers[i].z[f]-self.z[f]
                self.Rhat[:,i] = self.vec3
            #print self.Rhat
            #Ok now that we have Rhat we can compute TIB_star
            self.TIB = np.matmul(self.Rhat,self.RVICON)
            #print self.TIB
            #Ok now we just need to run the TIB matrix through the sixdof extraction
            #routine. Keep in mind that extract_Euler needs TBI and not TIB so you
            #need to throw in a transpose
            ptp = sdof.extract_Euler(np.transpose(self.TIB))
            #print('Phi,Theta,Psi=',ptp)
            self.phi.append(ptp[0])
            self.theta.append(ptp[1])
            self.psi.append(ptp[2])

        self.phi = np.asarray(self.phi)*180.0/np.pi
        self.theta = np.asarray(self.theta)*180.0/np.pi
        self.psi = np.asarray(self.psi)*180.0/np.pi

        self.phi = M.interpolateNans(self.phi)
        self.theta = M.interpolateNans(self.theta)        
        self.psi = M.interpolateNans(self.psi)

        #Turns out that phi and theta super noisy because of z? so let's filter these
        wc = 3
        self.phi_filtered,self.t_filtered = M.LowPass(self.phi,self.t,wc)
        self.theta_filtered,self.t_filtered = M.LowPass(self.theta,self.t,wc)

        #np.set_printoptions(precision=2,suppress=True)
        #np.set_printoptions(threshold='nan')
        #print self.psi

class Marker():
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        self.xdot = []
        self.ydot = []
        self.zdot = []
        self.xddot = []
        self.yddot = []
        self.zddot = []

def plot_rbd(data,pp):
    print 'Plotting Rigid Body States'
    pltx = P.plottool(12,'Time (sec)','X CG (m)','Rigid Body Position')
    pltx.plot(data.t,data.x)
    pp.savefig()
    plty = P.plottool(12,'Time (sec)','Y CG (m)','Rigid Body Position')
    plty.plot(data.t,data.y)
    pp.savefig()
    pltz = P.plottool(12,'Time (sec)','Z CG (m)','Rigid Body Position')
    pltz.plot(data.t,data.z)
    pp.savefig()

    plt_phi = P.plottool(12,'Time (sec)','Phi (deg)','Rigid Body Attitude')
    plt_phi.plot(data.t,data.phi)
    plt_phi.plot(data.t,data.phi_filtered,color='red')
    pp.savefig()

    plt_theta = P.plottool(12,'Time (sec)','Theta (deg)','Rigid Body Attitude')
    plt_theta.plot(data.t,data.theta)
    plt_theta.plot(data.t,data.theta_filtered,color='red')
    pp.savefig()

    plt_psi = P.plottool(12,'Time (sec)','Psi (deg)','Rigid Body Attitude')
    plt_psi.plot(data.t,data.psi)
    pp.savefig()

    pltxdot = P.plottool(12,'Time (sec)','Xdot CG (m/s)','Rigid Body Position')
    pltxdot.plot(data.t,data.xdot)
    pp.savefig()
    pltydot = P.plottool(12,'Time (sec)','Ydot CG (m/s)','Rigid Body Position')
    pltydot.plot(data.t,data.ydot)
    pp.savefig()
    pltzdot = P.plottool(12,'Time (sec)','Zdot CG (m/s)','Rigid Body Position')
    pltzdot.plot(data.t,data.zdot)
    pp.savefig()

    pltxddot = P.plottool(12,'Time (sec)','Xddot CG (m/s^2)','Rigid Body Position')
    pltxddot.plot(data.t,data.xddot)
    pp.savefig()
    pltyddot = P.plottool(12,'Time (sec)','Yddot CG (m/s^2)','Rigid Body Position')
    pltyddot.plot(data.t,data.yddot)
    pp.savefig()
    pltzddot = P.plottool(12,'Time (sec)','Zddot CG (m/s^2)','Rigid Body Position')
    pltzddot.plot(data.t,data.zddot)
    pp.savefig()

def plot_markers(data,pp):
    print 'Plotting Markers'
    #Plot all markers on 1 figure
    pltxm = P.plottool(12,'Time (sec)','X Position (m)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltxm.plot(data.t,data.markers[i].x)
    pp.savefig()
    pltym = P.plottool(12,'Time (sec)','Y Position (m)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltym.plot(data.t,data.markers[i].y)
    pp.savefig()
    pltzm = P.plottool(12,'Time (sec)','Z Position (m)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltzm.plot(data.t,data.markers[i].z)
    pp.savefig()
    pltxdotm = P.plottool(12,'Time (sec)','Xdot Velocity (m/s)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltxdotm.plot(data.t,data.markers[i].xdot)
    pp.savefig()
    pltydotm = P.plottool(12,'Time (sec)','Ydot Velocity (m/s)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltydotm.plot(data.t,data.markers[i].ydot)
    pp.savefig()
    pltzdotm = P.plottool(12,'Time (sec)','Zdot Velocity (m/s)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltzdotm.plot(data.t,data.markers[i].zdot)
    pp.savefig()
    pltxddotm = P.plottool(12,'Time (sec)','Xddot Acceleration (m/s^2)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltxddotm.plot(data.t,data.markers[i].xddot)
    pp.savefig()
    pltyddotm = P.plottool(12,'Time (sec)','Yddot Acceleration (m/s^2)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltyddotm.plot(data.t,data.markers[i].yddot)
    pp.savefig()
    pltzddotm = P.plottool(12,'Time (sec)','Zddot Acceleration (m/s^2)','Position of Markers')
    for i in range(0,data.numMarkers):
        pltzddotm.plot(data.t,data.markers[i].zddot)
    pp.savefig()
        
def get_vicon_data(fileName,numMarkers):

    try:
        with open(fileName) as file:
            fileExists = True
    except IOError as e:
        print ('Unable to open Vicon File',fileName)
        fileExists = False
        return 0

    fid = open(fileName,"r")

    #Create the Markers and the body
    rbd = Body(numMarkers)

    ctr = 0
    print 'Reading File'
    for line in fid:
        ctr+=1
        #ignore the first 6 lines of code
        if ctr == 2:
            frame_rate = int(line)
        if ctr > 8:
            if len(line) > 4:
                this_line = line.split(',')
                #The first column is frame
                rbd.frame.append(int(this_line[0]))
                rbd.t.append((int(this_line[0])-1)/200.0)
                #second column is dummy
                #this_line[1]
                #third_column and all following are the markers x,y,z
                for i in range(0,rbd.numMarkers):
                    try:
                        x = np.float(this_line[3*i+2])/1000.0 #Convert to m
                        #X is also backwards
                        x*=-1
                    except:
                        pass
                    rbd.markers[i].x.append(x)
                    try:
                        y = np.float(this_line[3*i+3])/1000.0
                    except:
                        pass
                    rbd.markers[i].y.append(y)
                    try:
                        z = np.float(this_line[3*i+4])/1000.0
                        #Turns out z is up in vicon
                        z*=-1
                    except:
                        pass
                    rbd.markers[i].z.append(z)
                    try:
                        xdot = np.float(this_line[rbd.numMarkers*3+3*i+2])/1000.0
                        #Rotate back to vicon lab
                        xdot*=-1
                    except:
                        pass
                    rbd.markers[i].xdot.append(xdot)
                    try:
                        ydot = np.float(this_line[rbd.numMarkers*3+3*i+3])/1000.0
                    except:
                        pass
                    rbd.markers[i].ydot.append(ydot)
                    try:
                        zdot = np.float(this_line[rbd.numMarkers*3+3*i+4])/1000.0
                        #Same as z
                        zdot*=-1
                    except:
                        pass
                    rbd.markers[i].zdot.append(zdot)
                    try:
                        xddot = np.float(this_line[rbd.numMarkers*6+3*i+2])/1000.0
                        #x is backwards
                        xddot*=-1
                    except:
                        pass
                    rbd.markers[i].xddot.append(xddot)
                    try:
                        yddot = np.float(this_line[rbd.numMarkers*6+3*i+3])/1000.0
                    except:
                        pass
                    rbd.markers[i].yddot.append(yddot)
                    try:
                        zddot = np.float(this_line[rbd.numMarkers*6+3*i+4])/1000.0
                        zddot*=-1 #Z is backwards from aero convention
                    except:
                        pass
                    rbd.markers[i].zddot.append(zddot)
                    
    print 'Converting to Numpy arrays'
    #Convert everything to numpy arrays
    rbd.t = np.asarray(rbd.t)
    for i in range(0,rbd.numMarkers):
        rbd.markers[i].x = np.asarray(rbd.markers[i].x)
        rbd.markers[i].y = np.asarray(rbd.markers[i].y)
        rbd.markers[i].z = np.asarray(rbd.markers[i].z)
        rbd.markers[i].xdot = np.asarray(rbd.markers[i].xdot)
        rbd.markers[i].ydot = np.asarray(rbd.markers[i].ydot)
        rbd.markers[i].zdot = np.asarray(rbd.markers[i].zdot)
        rbd.markers[i].xddot = np.asarray(rbd.markers[i].xddot)
        rbd.markers[i].yddot = np.asarray(rbd.markers[i].yddot)
        rbd.markers[i].zddot = np.asarray(rbd.markers[i].zddot)

    print 'Convert to Rigid Body'
    #Convert the markers to a rigid body
    rbd.rigid_body()
        
    return rbd

if __name__ == "__main__":

    SHOWPLOTS = 0
    pp = PDF(SHOWPLOTS,plt)
    
    if len(sys.argv) > 2:
        fileName = sys.argv[1]
        numMarkers = int(sys.argv[2])
    elif len(sys.argv) == 2:
        print('Filename given but need number of markers')
        sys.exit()
    else:
        #print(sys.argv)
        print('No Filename found or given. Also need number of markers')
        sys.exit()

    #fileName = "Data_Files/10_25_2016/FlightALL.log"
    #fileName = "Data_Files/11_29_2016/Flight2.log"

    vicon_data = get_vicon_data(fileName,numMarkers)

    #Let's just plot the markers
    plot_markers(vicon_data,pp)

    #Now let's plot the rigid body states
    plot_rbd(vicon_data,pp)

    pp.close()

    

