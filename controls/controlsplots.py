import control as ctl

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
