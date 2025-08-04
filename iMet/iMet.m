clear
clc
close all

%all = importdata('March_5_Flight_Test/20160305-112407-00037232.csv');
%all = importdata('April_20_Flight_Test/20160420-141621-00037232.csv');
all = importdata('Flight_Tests/April_20_2016/truncated_file.csv');
%all = importdata('20151120-124023-00037232.csv');
%all = importdata('20160304-213055-00037232.csv');
data = all.data;
[r,c] = size(data);
for idx = 1:r
    temp(idx) = str2num(all.textdata{idx,4})/100;
    time_raw = all.textdata{idx,7};
    time(idx) = NMEA_TIME(time_raw,'hrs')-5; %%Mean Greenwich Time
                                             %+5 (Daylight savings
                                             %time can move this)
    pressure(idx) = str2num(all.textdata{idx,3})/1000;
end

lat = data(:,1)/10^7; %%%May have to come back to this by using NMEA_LAT_LON? Actually this looks ok 5/26/2016. I checked with the Google.
lon = data(:,2)/10^7;
altitude = data(:,3)/1000;

plottool(1,'iMet_Example',18,'Latitude (deg)','Longitude (deg)','Temperature (C)');
%plot3(lat,lon,temp,'b-*')
plot3color(lat,lon,temp)

%%%%Temp vs Altitude is going to have 2 data streams. We
%%%%need to separate the two
m = find(altitude == max(altitude));
altL = altitude(1:m);
altR = altitude(m+1:end);
TL = temp(1:m);
TR = temp(m+1:end);

plottool(1,'Alt_Time',18,'Time (Hrs)','Altitude (m)');
plot(time(1:m),altL,'b*-')
hold on
plot(time(m+1:end),altR,'r*-')
legend('Ascent','Descent')
xlim([min([time]) max([time])])

%%%%Throw out the ground points
mn1 = min(altL);
mn2 = min(altR);
mn = min([mn1 mn2]);
tol = 3; %%%GPS accurate to 3 m
fL = altL<mn+2*tol;
fR = altR<mn+2*tol;
TL(fL) = [];
TR(fR) = [];
altL(fL) = [];
altR(fR) = [];
plottool(1,'Temp_Alt',18,'Temp (C)','Altitude (m)');
plot(TL,altL,'b*-')
hold on
plot(TR,altR,'r*-')
legend('Ascent','Descent')

%%%%Pressure vs Altitude is going to have 2 data streams. We
%%%%need to separate the two as well
PL = pressure(1:m);
PR = pressure(m+1:end);
%%%%Throw out the ground points
PL(fL) = [];
PR(fR) = [];
plottool(1,'Pressure_Alt',18,'Pressure (kPa)','Altitude(m)');
plot(PL,altL,'b*-')
hold on
plot(PR,altR,'r*-')
legend('Ascent','Descent')
xlim([min([PL PR]) max([PL PR])])

%%%%Get windspeed from pitot senor
[time_pitot,speed_pitot] = process_pitot_data('../FASTPitot/ZEIGLER_PARK1.TXT');


%%%%Interpolate to get points you need
%%%time is from iMet and is in NMEA_TIME hrs. pitot time is 
%in seconds and is set to start at a certain time. Theoretically
%everything should line up properly.
pitot_start = 14+7.2/60;
time_pitot_hrs = pitot_start + time_pitot/3600;
altitude_pitot = interp1(time,altitude,time_pitot_hrs);

%%%Plot to make sure Altitude and time match up
plottool(1,'Time Altitude Pitot',18,'Time (hrs)','Altitude (m)');
plot(time_pitot_hrs,altitude_pitot)
xlim([time_pitot_hrs(1) time_pitot_hrs(end)])

%%%%Plot Altitude as a function of speed
plottool(1,'Speed_Alt',18,'Wind Speed (m/s)','Altitude (m)');
m = find(altitude_pitot == max(altitude_pitot));
skip = 50;
altLp = altitude_pitot(1:skip:m);
altRp = altitude_pitot(m+1:skip:end);
speedL = speed_pitot(1:skip:m);
speedR = speed_pitot(m+1:skip:end);
%plot(speed_pitot,altitude_pitot)
plot(speedL,altLp,'b*-')
plot(speedR,altRp,'r*-')
legend('Ascent','Descent')
