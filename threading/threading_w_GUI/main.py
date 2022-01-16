#!/usr/bin/python3

##THREADING
import threading
##TIME
import time
##QUEUE MANAGEMENT
#import queue
#inputs = queue.Queue()
#inputs.put(True)
#inputs.get()
#inputs.qsize() to check and see how large the queue is
##SYSTEM
import sys
#KEYBOARD
import keyboard

##GLOBAL VARIABLES
run = True

#Manager
#print('Starting Manager....')
#from manager import manager
#MANt = threading.Thread(target=manager)
#MANt.start()

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
    ##Check to see if the GUI is still running. If it's not we break the code
    #if not UI_t.is_alive():
    #    print('KILLING ALL THREADS!!!!!!')
    #    print('Killing GUI')
    #    UI_t.join()
    #    print('Killing Aggregator')
    #    MAN_t.terminate()
    #    print('Ending Program')
    #    sys.exit()


print('Main Loop End')
