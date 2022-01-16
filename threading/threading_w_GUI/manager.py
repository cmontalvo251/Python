#TIME
import time

class manager():
    def __init__(self,modulecommands,scoreboard):        
        print("Initializing Manager")
        self.run = True
        ##Then run the manager
        self.loop(modulecommands,scoreboard)

    def loop(self,modulecommands,scoreboard):
        tstart = time.monotonic()
        ##Kick off infinite while loop to manage data
        while self.run == True:
            ##Get current time from computer
            t = time.monotonic()-tstart

            #Print to home
            print('Manager Time = ',t)
    
            ##Check queue
            if modulecommands.qsize() > 0:
                print('Command detected from main loop')
                self.run = modulecommands.get()

            ##Check scoreboard
            if scoreboard.qsize() == 0:
                print('Populating Scoreboard with time = ',t)
                scoreboard.put(t)

            ##A bunch more stuff is needed 
            ##but for now just going to sleep
            time.sleep(0.1)

        print('Manager Program Ended')
