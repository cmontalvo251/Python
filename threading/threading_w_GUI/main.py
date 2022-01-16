#!/usr/bin/python3

##THREADING
import threading
##TIME
import time
##QUEUE MANAGEMENT
import queue
modulecommands = queue.Queue()
scoreboard = queue.Queue()
##SYSTEM
import sys
#KEYBOARD
import keyboard

#GLOBAL VARIABLES
mainloop = True
scoreboard.put(42)

#Manager
print('Starting Manager....')
from manager import manager
MANt = threading.Thread(target=manager,args=(modulecommands,scoreboard))
MANt.start()

##GUI IN USERCONTROL
print('Starting GUI.....')
from UserInterface import UserInterface
UIt = threading.Thread(target=UserInterface,args=(scoreboard,))
UIt.start()

###Infinite Main loop to prevent program from ending prematurely
while UIt.is_alive():
    time.sleep(1.0)
    #print('GUI is still running')

###GUI has ended
print('Main Loop End')
##Send false to module commands
print('GUI ended sending stop command to Manager')
modulecommands.put(False)

##Wait for manager to quit
while MANt.is_alive():
    print('Waiting for Manager to quit',time.time())
    time.sleep(1.0)
MANt.join()

##Wait for UI to quit
while UIt.is_alive():
    print('Waiting for GUI to quit',time.time())
    time.sleep(1.0)
UIt.join()

#Program end
print('Program Quit')
