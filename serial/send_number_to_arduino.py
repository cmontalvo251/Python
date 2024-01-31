import serial as S
import struct
import numpy as np
import time

def binary(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))
def SerialPutString(hComm,string):
    for s in string:
      SerialPutc(hComm,s)
def SerialPutc(hComm,txchar):
    if hComm is not None:
      #print("Sending ASCII Code = " + str(ord(txchar)) + str(txchar))
      hComm.write(txchar.encode("ascii"))

def Serial_Init(ComPortName,BaudRate):
    try:
      print('Trying to open serial port.....',ComPortName,BaudRate)
      hComm = S.Serial(ComPortName,BaudRate);
      print('Success!!!!')
      hComm.flush()
    except:
      print('Failed')
      hComm = None
    return hComm


##INITIALIZE SERIAL PORT
#port = "/dev/ttyACM0"
port = "COM22"
BaudRate = 57600
hComm = Serial_Init(port,BaudRate)

degree_vec = np.linspace(0,145,20)

for deg in degree_vec:
    #df = 1.0
    int_deg = int(binary(deg),2)
    print("Sending = " + str(deg) + " " + str(int_deg))
    hex_deg = hex(int_deg)
    hex_deg = hex_deg.replace('0x','')
    outline = str(0)+':'+hex_deg
    print("Hex = ",outline)
    SerialPutString(hComm,outline)
    SerialPutc(hComm,'\r')
    time.sleep(1.0)

