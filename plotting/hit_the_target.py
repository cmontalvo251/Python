import numpy as np
import matplotlib.pyplot as plt
from pynput.keyboard import Key, Listener

##CREATE THE GAME ENGINE GLOBAL VARIABLE
GO = True
##Two keyboard functions
def on_press(key):
    print('{0} pressed'.format(key))
def on_release(key):
    global GO
    print('{0} release'.format(key))
    if key == Key.esc:
        GO = False
        print('Exiting....')
        return False #also kills the listener class
###Initial Conditions
x = 0.0
y = 0.0001
###Record Launch angle and speed from the user
launch_angle = np.float(input('Input the launch angle from the horizontal in degrees: '))
speed = np.float(input('How fast do you want to launch the ball? '))
#Decompose the vector into x and y
xdot = speed*np.cos(launch_angle*np.pi/180.0)
ydot = speed*np.sin(launch_angle*np.pi/180.0)
#Create a target
xT = 35.0
yT = 0.0

##Create the game window
plt.plot(xT,yT,'r*')
plt.grid()
plt.xlim([-1,xT*1.5])
plt.ylim([-1,xT*1.5])
##Kick off the listener
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
###Phyics Simulation
dt = 0.1
g = 9.81
while y > 0 and GO:
    ##Perform Euler's Method
    x = x + xdot*dt
    y = y + ydot*dt
    xdbldot = 0.0
    ydbldot = -g
    xdot = xdot + xdbldot*dt
    ydot = ydot + ydbldot*dt
    print(x,y,GO)
    plt.plot(x,y,'b*')
    plt.pause(0.001)
if abs(x - xT) < 5:
    print("YOU WIN!!!!!!")
plt.show()