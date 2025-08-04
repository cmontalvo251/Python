clc
close all
clear

%#Read data from file
fid = fopen('Data_Files/Mesonet_Data_Files/2_14_2017/GPSLOG04.TXT');

%%%First figure out how many lines are in the data file
numlines = 0;
width = 0;
line = 0;
while line ~= -1
    line = fgetl(fid);
    if length(line) > 1 
        numlines = numlines + 1;
        %%%Figure out the number of columns
        if width == 0
            line(line==':') = ' ';
            %%%Then we can just do a straight conversion to double
            width = length(str2num(line));
        end
    end
    if isempty(line)
        line = 0;
    end
end
fclose(fid);

%%%Then allocate memory for data
data = zeros(numlines,width);
%%%and reopen the file
fid = fopen('Data_Files/Mesonet_Data_Files/2_14_2017/GPSLOG04.TXT');
line = 0;
idx = 1;
while line ~= -1
    line = fgetl(fid);
    if length(line) > 1 
      %%%Parse data by replacing all colons with spaces
      line(line==':') = ' ';
      %%%Then we can just do a straight conversion to double
      data(idx,:) = str2num(line);
      idx = idx + 1;
    end
    if isempty(line)
        line = 0;
    end
end

%%%At this point we can extract useful information
raw_np = data(:,10:13); %%%raw bits
time_np = data(:,4); %%this is arduino time. If you want to use GPS
                     %time that's a bit more complex.

%###CONVERT RAW SIGNAL TO VOLTS - The raw signal is a 10-bit register
%###so you need to convert it to volts. 2^10 = 1024 so basically 1024 =
%###5 volts - it's completely linear
voltage = raw_np*(5.0/1023.0);

%#//2.5 volts should equal zero kPa. Should probably just calibrate
%#this every time instead of storing a random number
%#Apprarently this gives pressure in kPa which means the voltage is a
%#function of pressure
%find meanVoltage from 1:10 seconds
meanV = mean(voltage(time_np<10,:)); %%%This is a 1x4 vector 
pressure = voltage-ones(numlines,1)*meanV; %%voltage (Nx4) - (Nx1)*(1x4)

%####Q is kPa converted to atmospheres
q = pressure/101.325;

%####This equation here comes from bernoulli
%There is a potential here for k to be less than 1. 
%If that happens, the sqrt goes imaginary
k = (q+1.0).^(2.0/7.0);
%%%So we need to add a fix here
k(k<1) = 1;

%#This is the rest of the equation from bernoulli. 343.2 is the speed of
%#sound at sea-level
%Sqrt(gamma*R*T) - Replace with this from iMet sensor
%T is in Kelvin
%R is 286 ideal gas constant
%Gamma is the adiabatic index = 1.4
tempC = 20;
tempK = tempC + 273.15;
a_inf = sqrt(1.4*286*tempK);
airspeed_ms = a_inf*( sqrt( 5.0*(k-1.0) ) );

%##Run signal through a complimentary filter
sigma = 0.03;
airspeed_ms_filtered = zeros(length(airspeed_ms),4);
airspeed_ms_filtered(1,:) = airspeed_ms(1,:);
for idx = 1:(length(airspeed_ms)-1)
  airspeed_ms_filtered(idx+1,:) = (1-sigma)*airspeed_ms_filtered(idx,:) + sigma*airspeed_ms(idx,:);
end

%#Because conversion from Voltage to speed
%#is still noisy we need to calibrate one more
%#time
%meanU = mean(airspeed_ms_filtered(time_np<10,:));
%airspeed_ms_filtered = airspeed_ms_filtered - ones(numlines,1)*meanU;
    
figure()
plot(time_np,raw_np)
xlabel('Time (sec)')
ylabel('Raw Signal')
grid on

figure()
%plot(time_np,airspeed_ms)
hold on
plot(time_np,airspeed_ms_filtered,'-')
xlabel('Time (sec)')
ylabel('Speed (m/s)')
grid on




    
    

    
