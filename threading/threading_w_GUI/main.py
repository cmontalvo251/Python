#!/usr/bin/python3

##THREADING
import threading
##TIME
import time
##QUEUE MANAGEMENT
import queue
inputs = queue.Queue()
#inputs.get()
#inputs.qsize() to check and see how large the queue is
##SYSTEM
import sys
#KEYBOARD
import keyboard

#GLOBAL VARIABLES
run = True

#Manager
print('Starting Manager....')
from manager import manager
MANt = threading.Thread(target=manager,args=(inputs,))
MANt.start()

##GUI IN USERCONTROL
#print('Starting GUI.....')
#from UserInterface import UserInterface
#UIt = threading.Thread(target=UserInterface)
#UIt.start()

while run == True:
    time.sleep(0.1)
    #Check for q
    if keyboard.is_pressed('q'):
        print('Quit Command Received')
        run = False
        inputs.put(False)
        
print('Main Loop End')
while MANt.is_alive():
    print('Waiting for Manager to quit',time.time())
    time.sleep(1.0)
MANt.join()
print('Program Quit')
