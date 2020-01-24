###Import modules
import numpy as np
import control as ctl
import matplotlib.pyplot as plt

##Functions
def plot_margins(sys):
    mag,phase,omega = ctl.bode(sys,dB=True,Plot=False)
    magdB = 20*np.log10(mag)
    phase_deg = phase*180.0/np.pi
    Gm,Pm,Wcg,Wcp = ctl.margin(sys)
    GmdB = 20*np.log10(Gm)
    ##Plot Gain and Phase
    f,(ax1,ax2) = plt.subplots(2,1)
    ax1.semilogx(omega,magdB)
    ax1.grid(which="both")
    ax1.set_xlabel('Frequency (rad/s)')
    ax1.set_ylabel('Magnitude (dB)')
    ax2.semilogx(omega,phase_deg)
    ax2.grid(which="both")
    ax2.set_xlabel('Frequency (rad/s)')
    ax2.set_ylabel('Phase (deg)')
    ax1.set_title('Gm = '+str(np.round(GmdB,2))+' dB (at '+str(np.round(Wcg,2))+' rad/s), Pm = '+str(np.round(Pm,2))+' deg (at '+str(np.round(Wcp,2))+' rad/s)')
    ###Plot the zero dB line
    ax1.plot(omega,0*omega,'k--',lineWidth=2)
    ###Plot the -180 deg lin
    ax2.plot(omega,-180+0*omega,'k--',lineWidth=2)
    ##Plot the vertical line from -180 to 0 at Wcg
    ax2.plot([Wcg,Wcg],[-180,0],'r--',lineWidth=2)
    ##Plot the vertical line from -180+Pm to 0 at Wcp
    ax2.plot([Wcp,Wcp],[-180+Pm,0],'g--',lineWidth=2)
    ##Plot the vertical line from min(magdB) to 0-GmdB at Wcg
    ax1.plot([Wcg,Wcg],[np.min(magdB),0-GmdB],'r--',lineWidth=2)
    ##Plot the vertical line from min(magdB) to 0db at Wcp
    ax1.plot([Wcp,Wcp],[np.min(magdB),0],'g--',lineWidth=2)
    return Gm,Pm,Wcg,Wcp
    
#%%%Actuator Dynamics
A = ctl.tf([3],[1,3])
wn = 20.0
G = ctl.tf([5*wn**2],[1,2,wn**2])*A
#G = ctl.tf([1],[1,2,1,0])
Gm,Pm,Wcg,Wcp=plot_margins(G)
#%%%The Margins are
print('Gain Margin = ',Gm)
print('Phase Margin = ',Pm)

#%%%The gain margin tells us how much gain the system
#%%%The system can handle. Since our gain margin is positive
#%%%It means we need to LOWER the bode plot. This means we 
#%%%Need to multiply our plot by a number less than 1.
#%%%%In this case we can use our gain margin to determine
#%%%What we can make K to stabilize the system
#%%multiply by 99% to reduce it just 
#%%%under the stability boundary
K = Gm*0.99; 
GCL = ctl.minreal(K*G/(1+K*G))

#%%%As can be seen by this step response
plt.figure()
tout,yout = ctl.step_response(GCL)
plt.plot(tout,yout)
plt.grid()


#%%%%And this pzmap
ctl.pzmap(GCL)


#%%%To see a more detailed view you can run rlocus
ctl.rlocus(G)
#%%%Click on the locus where the poles cross the imaginary
#%%%axis and you'll see that when K = Gm the system goes unstable
#%%%%Notice that if K > Gm the system is unstable

#%%%The negative phase means that are system is lagging
#%%%Behind by 34 degrees. There is no way to simply increase
#%%%phase. Lead lag filters are the best at adding phase
#%%%to a system
#%%%Using the equations from Brian Douglas we can 
#%%%Tune a lead/lag filter
#%https://www.youtube.com/watch?v=rH44ttR3G4Q&list=PLUMWjy5jgHK24TCFwngV5MeiruHxt1BQR&index=7
#%%%We're just going to add the phase margin to the frequency at which the
#%%%phase margin occurs
phi_max = Pm*np.pi/180.0; 
wm = Wcp;
#%sind(phi_max) = (a2-1)/(a2+1)
#%a2*sind(phi_max) + sind(phi_max) = a2 - 1
#%a2*(sind(phi_max) - 1) = -sind(phi_max) - 1
a2 = (-np.sin(phi_max) - 1)/(np.sin(phi_max) - 1)
tau = 1/(wm*np.sqrt(a2))
#%%%Then build the compensator
C = ctl.tf([a2*tau,1],[tau,1])

#%%%Then create a new open loop system
CG = C*G
#%%%And compute the bode plot again
Gm,Pm,Wcg,Wcp=plot_margins(CG)
#%%%The Margins are
print('Gain Margin = ',Gm)
print('Phase Margin = ',Pm)


#%%%Now the system has an infinite phase margin
#%%%The good news is that we now have a gain margin that is greater than 1
#%%%Which means that we can make K bigger than 1
#%%%under the stability boundary
K = Gm*0.99; 
GCL = ctl.minreal(K*CG/(1+K*CG))

#%%%As can be seen by this step response
plt.figure()
tout,yout = ctl.step_response(GCL)
plt.plot(tout,yout)
plt.grid()

#%%%%And this pzmap
ctl.pzmap(GCL)

#%%%To see a more detailed view you can run rlocus
ctl.rlocus(CG)
#%%%Click on the locus where the poles cross the imaginary
#%%%axis and you'll see that when K = Gm the system goes unstable

#%%%%Notice that if K > Gm the system is unstable
plt.show()