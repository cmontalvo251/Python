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
    def __init__(self,scoreboard):
        #Save scoreboard
        self.scoreboard = scoreboard
        #Create app
        self.app = tk.Tk()
        #Change title
        self.app.title('Gui Test')
        #Change Size
        self.app.geometry('200x200')
        ##Create Quit Button
        closebutton = tk.Button(self.app,text="Quit",command=self.close)
        closebutton.pack()
        ##Create Update Button
        #updatebutton = tk.Button(self.app,text="Update",command=self.update)
        #updatebutton.pack()
        ##Create Label
        self.var = tk.StringVar()
        label = tk.Label(self.app, textvariable=self.var, relief=tk.RAISED)
        ##Get score
        score = 0
        if self.scoreboard.qsize() > 0:
            command = self.scoreboard.get()
            if command != False:
                score = command
        self.var.set("Variable = "+str(score))
        label.pack()
        ##Run the update command the first time
        self.update()
        self.app.mainloop()

    def update(self):
        print('Checking Scoreboard Queue')
        if self.scoreboard.qsize() > 0:
            print('New Scoreboard Detected')
            newvar = np.round(np.float(self.scoreboard.get()),2)
            self.var.set("Variable = "+str(newvar))
        else:
            print('Queue empty')
        #Use the after command to run this loop idefinitely
        self.app.after(1000,self.update)

    def close(self):
        print('Closing GUI')
        self.app.destroy()

    
