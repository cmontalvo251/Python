#!/usr/bin/python3

##THREADING
import multiprocessing
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

##GLOBAL VARIABLES
boolean = True

#DataAGGREGATOR
from manager import manager
MAN_t = multiprocessing.Process(target=manager)
MAN_t.start()

##GUI IN USERCONTROL
print('Starting GUI.....')
from UserInterface import UserInterface
UI_t = multiprocessing.Process(target=UserInterface)
UI_t.start()

while True:
    time.sleep(1.0)
    ##Check to see if the GUI is still running. If it's not we break the code
    if not UI_t.is_alive():
        print('KILLING ALL THREADS!!!!!!')
        print('Killing GUI')
        UI_t.terminate()
        print('Killing Aggregator')
        MAN_t.terminate()
        print('Ending Program')
        sys.exit()
