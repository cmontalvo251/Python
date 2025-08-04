function [time_np,airspeed_ms_filtered] = process_pitot_data(filename)

%clc
%close all

%#Generate "Truth" Signal
time_truth = linspace(0,140,100);
speed_truth = zeros((100),1);
data = [1.0,2.5,4.0,6.0,7.5]-0.5;
for x = 1:length(time_truth)
  if time_truth(x) < 20
    speed_truth(x) = 0;
  elseif time_truth(x) < 40
    speed_truth(x) = data(1);
  elseif time_truth(x) < 60
    speed_truth(x) = data(2);
  elseif time_truth(x) < 80
    speed_truth(x) = data(3);
  elseif time_truth(x) < 100
    speed_truth(x) = data(4);
  elseif time_truth(x) < 120
    speed_truth(x) = data(5);
  elseif time_truth(x) < 140
    speed_truth(x) = 0;
  end
end

%#Read data from file
%fid = fopen('Windtunnel_Calibration_Test.TXT');
fid = fopen(filename);
data = [];
line = 0;
while line ~= -1
    line = fgetl(fid);
    if length(line) > 1 && line(1) ~= 'D'
        data = [data;str2num(line)];
    end
    if isempty(line)
        line = 0;
    end
end
%data = dlmread('AIRSPEED.TXT');

raw_np = data(:,2);
time_np = data(:,1)./1000;

%###CONVERT RAW SIGNAL TO VOLTS - The raw signal is a 10-bit register
%###so you need to convert it to volts. 2^10 = 1024 so basically 1024 =
%###5 volts - it's completely linear
voltage = raw_np*(5.0/1023.0);

%#//2.5 volts should equal zero kPa. Should probably just calibrate
%#this every time instead of storing a random number
%#Apprarently this gives pressure in kPa which means the voltage is a
%#function of pressure
%find meanVoltage from 1:10 seconds
meanV = mean(voltage(time_np<10));
pressure = voltage-meanV;

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
airspeed_ms_filtered = zeros(length(airspeed_ms),1);
airspeed_ms_filtered(1) = airspeed_ms(1);
for idx = 1:(length(airspeed_ms)-1)
  airspeed_ms_filtered(idx+1) = (1-sigma)*airspeed_ms_filtered(idx) + sigma*airspeed_ms(idx);
end

%#Because conversion from Voltage to speed
%#is still noisy we need to calibrate one more
%#time
meanU = mean(airspeed_ms_filtered(time_np<10));

airspeed_ms_filtered = airspeed_ms_filtered - meanU;
    
%figure()
%plot(time_np,raw_np)
%xlabel('Time (sec)')
%ylabel('Raw Signal')
%grid on

figure()
%plot(time_truth,speed_truth)
hold on
%plot(time_np,airspeed_ms,'r-')
airspeed_ms_filtered(time_np<4) = 0;
plot(time_np,airspeed_ms_filtered,'r-')
xlabel('Time (sec)')
ylabel('Speed (m/s)')
grid on
%legend('Truth','Sampled')




    
    

    
