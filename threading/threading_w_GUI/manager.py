#TIME
import time

class manager():
    def __init__(self):
        print("Initializing Manager")
        ##Then run the manager
        self.run()

    def run(self):
        tstart = time.monotonic()
        ##Kick off infinite while loop to manage data
        while True:
            ##Get current time from computer
            t = time.monotonic()-tstart

            ##A bunch more stuff is needed and you can check the SysML model
            ##but for now just going to sleep
            time.sleep(1.0)

            ##Check for Stopcommand
            #if stopcommand == True:
            #    print('Stopping Manager')
            #   sys.exit()
