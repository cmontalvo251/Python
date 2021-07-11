import serial as S
import struct

class Telemetry():
  def __init__(self,BaudRate=115200,port="/dev/ttyUSB0"):
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
      self.hComm.write(txchar)
  def SerialPutString(self,string):
    for s in string:
      self.SerialPutc(s)
  def SerialSendArray(self,number_array,echo=1):
    #union inparser inputvar; ##Need to look up how to do union inparser
    #in python and then convert the number to 8digit hex
    for n in number_array:
      #inputvar.floatversion = number_array[i];
      int_var = int(self.binary(n),2)
      print("Sending = " + str(n) + " " + str(int_var))
      #sprintf(outline,"H:%08x ",int_var);
      hexval=hex(int_var)
      hexval = hexval.replace('0x','')
      outline='H:'+hexval+' '
      print("Hex = " + outline)
      self.SerialPutString(outline);
      self.SerialPutc('\r');
  def binary(self,num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))
  def SerialPutHello(self,echo=1):
    self.SerialPutc('w');
    self.SerialPutc('\r');
  
if __name__ == '__main__':
  ser = Telemetry(115200,"/dev/ttyACM0") 
  number_array = [3.4,-2.3,0.4,-0.1,5.8,300.0,-300.0]
  ser.SerialSendArray(number_array)