#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:18:31 2020

@author: toddlillian
"""

#originally based on: https://matplotlib.org/3.1.1/gallery/widgets/slider_demo.html
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from scipy import signal
import control



Time = np.arange(0.0, 20.0, 0.001)#time range of interest
U=Time*0+1#command input of interest
Omega=np.logspace(-2,2,1000)#frequency range of interest

plantsys=control.tf(1,[1,2*.01,1])#system of interest

#control system definition/initialize gains
kp0 = 1
ki0 = 1
kd0 = 1
sysp=kp0#proportional
sysi=control.tf(ki0,[1,0])#integral
sysd=control.tf([kd0,0],1)#derivative
sys=control.feedback(plantsys*(sysp+sysi+sysd),1)#assembled closed loop system

#set up the plot for the response in the time domain
fig1, ax1 = plt.subplots(num=1)
ax1.margins(x=0)
plt.subplots_adjust(left=0.15, bottom=0.3)
plt.ylim((0,1.5))

#plot the command input
plt.plot(Time,U,'r')

#solve for and plot the response in the time domain using initilized gains
Y=control.forced_response(sys,Time,U)[1]
l, = plt.plot(Time, Y, lw=2)

#set up sliders for the gains
axcolor = 'lightgoldenrodyellow'
axkp	 = plt.axes([0.15, 0.2, 0.75, 0.03], facecolor=axcolor)
axki = plt.axes([0.15, 0.15, 0.75, 0.03], facecolor=axcolor)
axkd = plt.axes([0.15, 0.1, 0.75, 0.03], facecolor=axcolor)

skp = Slider(axkp, 'kp', 0, 10, valinit=1, valstep=.1)
ski = Slider(axki, 'ki', 0, 10, valinit=1, valstep=.1)
skd = Slider(axkd, 'kd', 0, 10, valinit=1, valstep=.1)

#set up the bode plots
fig2, ax2 = plt.subplots(2,1,num=2)


#solve for and plot the bode data
mag,phase,omega=control.bode_plot(sys,Plot=False,omega=Omega)
plt.subplot(2,1,1)
m,=plt.semilogx(omega,20*np.log10(mag))
plt.subplot(2,1,2)
p,=plt.semilogx(omega,np.degrees(phase))

#function to update data upon moving sliders
def update(val):
	#control system definition
	kp = skp.val#proportional gain
	ki = ski.val#integral gain
	kd = skd.val#derivative gain
	sysp=kp#proportional
	sysi=control.tf(ki,[1,0])#integral
	sysd=control.tf([kd,0],1)#derivative
	sys=control.feedback(plantsys*(sysp+sysi+sysd),1)#assembled closed loop system
	
	#solve for and update the plot of the response in the time domain
	Y=control.forced_response(sys,Time,U)[1]
	l.set_ydata(Y)
	fig1.canvas.draw_idle()
	
	#solve for and update the plot of the bode data
	
	mag,phase,omega=control.bode_plot(sys,Plot=False,omega=Omega)
	m.set_ydata(20*np.log10(mag))
	p.set_ydata(np.degrees(phase))
	fig2.canvas.draw_idle()
	
	

#call the update function upon movine a slider
skp.on_changed(update)
ski.on_changed(update)
skd.on_changed(update)

plt.figure(fig1.number)
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

#define reset button
def reset(event):
	skp.reset()
	ski.reset()
	skd.reset()
button.on_clicked(reset)

# rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
# radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


# def colorfunc(label):
# 	l.set_color(label)
# 	fig.canvas.draw_idle()
# radio.on_clicked(colorfunc)




plt.show()


