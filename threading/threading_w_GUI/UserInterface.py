import sys
import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkst
from datetime import datetime
from tkinter.constants import WORD
from tkinter.constants import INSERT
import numpy as np
import sys
import time
import multiprocessing
import copy as C

class UserInterface():
    def __init__(self):
        print('Initializing UI Threads')
        print('Generating App....')
        self.app = App()
        print('Opening Window....')
        self.app.update_t = multiprocessing.Process(target=self.app.updateloop)
        self.app.update_t.start()
        self.app.mainloop()
            
class Frame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.window = container
        # setup the grid layout manager - each column will be the same size as the rest
        #the buttons will go in column 1 and 2 to center them
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        #Stop
        ttk.Button(self, text='Stop', command=self.close).grid(column=1, row=0)

        #Start
        ttk.Button(self, text='Start', command=self.start).grid(column=2,row=0)
       
        for widget in self.winfo_children():
            widget.grid(padx=5, pady=15)

    #close function in Python
    def close(self):
        print('Closing Window')
        self.window.destroy()
        print('Closing Update loop')
        self.window.update_t.terminate()
        print('Exiting GUI')
        sys.exit()

    #Empty function in Python
    def start(self):
        print('Starting something....')

# main routine
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TKINTER TEST')
        self.geometry('450x450')
        self.resizable(0, 0)
        # windows only (remove the minimize/maximize button)
        #self.attributes('-toolwindow', True)
        
        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.__create_widgets()

    def __create_widgets(self):
        # create the control frame
        self.frame = Frame(self)
        self.frame.grid(column=0, row=0)

    def updateloop(self):
        ctr = 0
        while True:
            print('Updating....')
            time.sleep(1.0)
            ctr+=1
            #if ctr==2:
            #    self.frame.status[0].config(background='Yellow')
            
