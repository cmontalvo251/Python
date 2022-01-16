#TIME
import time

class manager():
    def __init__(self,inputs):        
        print("Initializing Manager")
        self.run = True
        ##Then run the manager
        self.loop(inputs)

    def loop(self,inputs):
        tstart = time.monotonic()
        ##Kick off infinite while loop to manage data
        while self.run == True:
            ##Get current time from computer
            t = time.monotonic()-tstart

            #Print to home
            print('Manager Time = ',t)
            
            ##A bunch more stuff is needed 
            ##but for now just going to sleep
            time.sleep(1.0)

            ##Check queue
            if inputs.qsize() > 0:
                print('Command detected from main loop')
                self.run = inputs.get()

        print('Manager Program Ended')
