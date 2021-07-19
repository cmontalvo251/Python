import serial as S ##python3 -m pip install pyserial
import struct
import random

class Telemetry():
  def __init__(self,BaudRate=57600,port="/dev/ttyAMA0",period=1.0):
    self.lastTime = 0.0
    self.period = period #in seconds
    self.SerialInit(port,BaudRate);
    #//Call this for higher level control
  def SerialInit(self,ComPortName,BaudRate):
    try:
      self.hComm = S.Serial(ComPortName,BaudRate);
    except:
      self.hComm = None
  def SerialGetc(self):
    rxchar = '0' #does nothing right now
    return rxchar;
  def SerialPutc(self,txchar):
    if self.hComm is not None:
      print("Sending ASCII Code = " + str(ord(txchar)))
      self.hComm.write(txchar.encode("ascii"))
  def SerialPutString(self,string):
    for s in string:
      self.SerialPutc(s)
  def SerialSendArray(self,number_array,echo=1):
    #union inparser inputvar; ##Need to look up how to do union inparser
    #in python and then convert the number to 8digit hex
    i = 0
    for n in number_array:
      #inputvar.floatversion = number_array[i];
      int_var = int(self.binary(n),2)
      print("Sending = " + str(n) + " " + str(int_var))
      #sprintf(outline,"n:%08x ",int_var);
      hexval=hex(int_var)
      hexval = hexval.replace('0x','')
      outline=str(i)+':'+hexval
      print("Hex = " + outline)
      self.SerialPutString(outline);
      self.SerialPutc('\r');
      i+=1
  def binary(self,num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))
  def SerialPutHello(self,echo=1):
    self.SerialPutc('w');
    self.SerialPutc('\r');
  
if __name__ == '__main__':
  ser = Telemetry(57600,"/dev/ttyAMA0")
  number_array = [0,0]
  for n in range(0,2):
    number_array[n] = random.randint(1,100)
  ser.SerialSendArray(number_array)
