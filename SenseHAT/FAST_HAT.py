#Import the sense_hat module
from sense_hat import SenseHat as S
import time
import datetime
import os.path
import sys
import os

def ShortenDigits(val):
    s_val = str(val)
    s_split = s_val.split('.')
    decimals = '0'
    if len(s_split) > 1:
        decimals = s_split[1]
        if len(decimals) > 2:
            decimals = decimals[0:2]
    return s_split[0] + '.' + decimals

def getPTH():
    pressure = sense.get_pressure()
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    return pressure,temperature,humidity


#Now we need a while loop to loop forever for now let's set a counter and only do 10 steps
#this controls the leds 
X = [255,0,0]
O = [0, 0 ,0]

matrix = [
X,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
]

matrix2 = [
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
O,O,O,O,O,O,O,O,
]

#Initialize the sensor
sense = S()
sense.clear()

#Open a file for writing
file_found = 0
ctr = 0
max_filename = 1000
while not file_found:
    ctr += 1
    if max_filename == ctr:
        sense.show_message("Ran out of filenames")
        sys.exit()
    filename = '/home/pi/Desktop/PTH_DATA/PTH'+str(ctr)+'.txt'
    print(filename)
    if os.path.isfile(filename):
        print('File exists...skipping')
    else:
        file_found = 1
print('File Found ',filename)

#All systems go
sense.show_message('PTH'+str(ctr))

outfile = open(filename,'w+') #+ means append

#time.sleep(2) #Sleep for 2 seconds to make sure

#Poll pressure, temperature and humidity and spit to show_message to make sure everything is working
pressure = 0.0
while abs(pressure) < 500:
	pressure,temperature,humidity = getPTH()
sense.show_message(ShortenDigits(pressure))
sense.show_message(ShortenDigits(temperature))
sense.show_message(ShortenDigits(humidity))

ctr = 0
sp = " "
button_pressed = False
#Initialize timer
t0 = time.time()
while not button_pressed:
    ctr += 1
    p,t,h = getPTH()
    elapsed_time = time.time()-t0
    print(elapsed_time,p,t,h)
    output = str(elapsed_time) + sp + str(p) + sp + str(t) + sp + str(h) + sp + '\n'
    outfile.write(output)
    outfile.flush()
    #Check for button press
    for event in sense.stick.get_events():
	button_pressed = True
    if ctr % 10 == 0: #makes the red led blink every 100 data points recorded
        sense.set_pixels(matrix)
    else:
        sense.set_pixels(matrix2)

outfile.close()

sense.show_message("File Closed")

os.system('shutdown now')
