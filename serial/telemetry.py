import serial as S

class Telemetry():
  def __init__(BaudRate=115200,port="/dev/ttyUSB0"):
    self.SerialInit(port,BaudRate);
    #//Call this for higher level control
  def SerialInit(self,ComPortName,BaudRate) 
      self.hComm = S.Serial(ComPortName,BaudRate);
  def SerialGetc(self):
    rxchar = '0' #does nothing right now
    return rxchar;
  def SerialPutc(self,txchar):
    self.hComm.write(txchar)
  def SerialPutString(self,string):
    for s in string:
      self.SerialPutc(s)
  def SerialSendArray(self,number_array,num,echo=1):
    #union inparser inputvar; ##Need to look up how to do union inparser
    #in python and then convert the number to 8digit hex
    for n in number_array:
      #inputvar.floatversion = number_array[i];
      #int int_var = inputvar.inversion;
      #sprintf(outline,"H:%08x ",int_var);
      hexval='FFFFFFFF' ##Just for default
      outline='H:'+hexval+' '
      self.SerialPutString(outline);
      self.SerialPutc('\r');
  def SerialPutHello(self,echo=1):
    self.SerialPutc('w');
    self.SerialPutc('\r');
  
