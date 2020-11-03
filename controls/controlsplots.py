import control as ctl
import numpy as np
import json

##Pulled from this source
#https://github.com/python-control/python-control/blob/master/control/timeresp.py
def step_info(sys,T=None,T_step=None,SettlingTimeThreshold=0.02,RiseTimeLimits=(0.1, 0.9)):
    if T == None:
        ##Need to figure out slowest pole
        poles = ctl.pole(sys)
        real_component = np.real(poles)
        if np.sum(real_component > 0):
            print('System Unstable',poles,real_component,any(real_component))
            return 0
        ##This assumes all poles are negative
        slowest_pole = np.max(real_component)
        ##Settling time is then 4/(zeta*wn) = 4/(sigma)
        tfinal = -10.0*(4.0/slowest_pole) ##add 10 for a safety factor
        #minus sign because slowest pole is negative
        ##Now we make time
        if T_step == None:
            T_step = 0.01
        T = np.arange(0,tfinal,T_step)

    #Now we simulate the system
    tout,yout = ctl.step_response(sys,T)

    # Steady state value
    InfValue = yout[-1]

    # RiseTime
    tr_lower_index = (np.where(yout >= RiseTimeLimits[0] * InfValue)[0])[0]
    tr_upper_index = (np.where(yout >= RiseTimeLimits[1] * InfValue)[0])[0]
    RiseTime = T[tr_upper_index] - T[tr_lower_index]

    # SettlingTime
    sup_margin = (1. + SettlingTimeThreshold) * InfValue
    inf_margin = (1. - SettlingTimeThreshold) * InfValue
    # find Steady State looking for the first point out of specified limits
    for i in reversed(range(T.size)):
        if((yout[i] <= inf_margin) | (yout[i] >= sup_margin)):
            SettlingTime = T[i + 1]
            break

    PeakIndex = np.abs(yout).argmax()

    info = {
        'RiseTime': RiseTime,
        'SettlingTime': SettlingTime,
        'SettlingMin': yout[tr_upper_index:].min(),
        'SettlingMax': yout.max(),
        'Overshoot': 100. * (yout.max() - InfValue) / (InfValue - yout[0]),
        'Undershoot': yout.min(), # not very confident about this
        'Peak': yout[PeakIndex],
        'PeakTime':  T[PeakIndex],
        'SteadyStateValue': InfValue
        }

    print(json.dumps(info,indent=4))

    return info

def plot_margins(sys,omegaIN=None):
    if omegaIN is not None:
        mag,phase,omega = ctl.bode(sys,omega=omegaIN,dB=True,Plot=False)
    else:
        mag,phase,omega = ctl.bode(sys,dB=True,Plot=False)
    magdB = 20*np.log10(mag)
    phase_deg = phase*180.0/np.pi
    Gm,Pm,Wcg,Wcp = ctl.margin(sys)
    print('Gain Margin = ',Gm,' at frequency = ',Wcg)
    print('Phase Margin = ',Pm,' at frequency = ',Wcp)
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
    #Does the plot cross positive 180?
    if np.any(phase_deg > 180):
        ax2.plot(omega,180+0*omega,'k--',lineWidth=2)
        ##Plot the vertical line from -180 to 0 at Wcg
        ax2.plot([Wcg,Wcg],[-180,180],'r--',lineWidth=2)
        ##Plot the vertical line from -180+Pm to 0 at Wcp
        ax2.plot([Wcp,Wcp],[-180+Pm,180-Pm],'g--',lineWidth=2)
    else:
        ##Plot the vertical line from -180 to 0 at Wcg
        ax2.plot([Wcg,Wcg],[-180,0],'r--',lineWidth=2)
        ##Plot the vertical line from -180+Pm to 0 at Wcp
        ax2.plot([Wcp,Wcp],[-180+Pm,0],'g--',lineWidth=2)
    ##Plot the vertical line from min(magdB) to 0-GmdB at Wcg
    ax1.plot([Wcg,Wcg],[np.min(magdB),0-GmdB],'r--',lineWidth=2)
    ##Plot the vertical line from min(magdB) to 0db at Wcp
    ax1.plot([Wcp,Wcp],[np.min(magdB),0],'g--',lineWidth=2)
    return Gm,Pm,Wcg,Wcp,phase_deg,omega
