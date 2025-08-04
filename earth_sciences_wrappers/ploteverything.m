clear
clc
close all
%%%This code assumes you have run pitot.py and quad.py
%%%run ploteverything.py (wrapper.py is ok) and created
%%%Two logfiles. One for the quad and one for the pitot
%%%Data

%%%Get pitot data
%%0 is FASTQuad with FP4 on it and 1 is Sytske Quad with FP4V
pitot_data = dlmread('Compiled_Data/Mesonet_Results/4_13_2017/Pitot_Data0.out'); 

%%%Get quad data
quad_data = dlmread('Compiled_Data/Mesonet_Results/4_13_2017/Quad_Data0.out');

%%%%%PARAMETERS%%%%%%
TRUNCATION_THRESHOLD = 2;
%WC = 0.25;
WC = 1.0;
wc_xy = 10000.0;
CAL_TIMES = [-99,0];
MUCHO_PLOTS = 0;
SIG = 0.03;
ROTATION = 1;
INERTIAL = 1;
TRANSLATION = 1;

%%%Each of these files has 23 columns
%%% 1 - GPS time in hrs 
%%% 2 - Latitude
%%% 3 - Longitude
%%% 4 - Altitude (this is Pressure altitude offset by GPS) meters
%%% 5 - Phi - rad
%%% 6 - theta - rad
%%% 7 - psi - rad
%%% 8 - Lateral Speed GPS - Note FP4 outputs -99 for this
%%% 9 - Lateral Speed GPS - Lateral speed is NOT xdot or ydot
%%% 10 - Vertical Speed (m/s) - FP4 outputs -99 for this as well
%%% 11 - P rad/s 
%%% 12 - Q rad/s - FP4 outputs -99 for all angular rates
%%% 13 - R rad/s
%%% 14 - Ax m/s^2 
%%% 15 - Ay m/s^2 - FP4 outputs -99 for all accelerations
%%% 16 - Az m/s^2 
%%% 17 - A0 - A0 through A3 are the raw analog signals from the pitot probe
%%% 18 - A1 - I elected to output raw data in case we wanted to mess with
%%% 19 - A2 - the filtering in here. It will make this code a bit more
%%% 20 - A3 - complex but it should be ok.
%%% 21 - Temperature (C) - Quad outputs -99 for this
%%% 22 - Pressure (kPa)
%%% 23 - Humidity (%) - Quad outputs -99 for this

%%%Ok so what do we do?
nhat = [1 0 -1 0;0 1 0 -1;0 0 0 0]; %%%direction of pitots
l = (2/12)/3.28; %%%distance from center to tip of pitot
h = (4.5/12)/3.2; %%%height above quad
rQP = [l 0 -l 0;0 l 0 -l;h h h h];
%%%Get time for interpolations
pitot_time = pitot_data(:,1);
quad_time = quad_data(:,1);
%%%%Get omega from quad
pqr = quad_data(:,11:13)';
if ROTATION
    plottool(1,'PQR',18,'Time (Hr)','PQR (rad/s)');
    plot(quad_time,pqr)
end
%%%Get phi theta psi from quad
ptp = quad_data(:,5:7)';
if INERTIAL
    plottool(1,'PTP',18,'Time (Hr)','PTP (deg)');
    plot(quad_time,ptp(1:2,:)*180/pi)
    legend('Roll','Pitch')
end
%%%Now we need a 3x3 TIB matrix for all data points. Hmm might be better to
%%%do this in the loop? 
%%%We also need xyzdot from the quad.
zdot = quad_data(:,10); %%zdot is no big deal. I think I looked up CLIMB_RATE from the 
%%%documentation of CTUN and CLIMB_RATE is in m/s
%%%How do we get xdot? We might need to use lateral speed and filter using
%%%the accelerometer data. We can cross that bridge later.
%%%Shit is GPS speed from the qaud in m/s or knots???
%%%This is in m/s. I made sure to check.
lat = quad_data(:,2);
lon = quad_data(:,3);
%%%Convert to X,Y
origin = [lat(1),lon(1)];
[x,y] = convertLATLON(lat,lon,origin);
%%%Run X and Y through derivative filter
%%%Make sure to multiply by 3600 to get to seconds
[tf,xdot_f] = DerivativeFilter(x,quad_time*3600,wc_xy,0,20);
[tf,ydot_f] = DerivativeFilter(y,quad_time*3600,wc_xy,0,20); 
xdot = quad_data(:,8);
ydot = quad_data(:,9);
xyzdot = [xdot_f';ydot_f';zdot'];
if TRANSLATION
    plottool(1,'Lat/Lon',18,'Latitude (deg)','Longitude (deg)');
    plot(lat,lon)
    plottool(1,'X/Y',18,'Time (Hr)','Position (m)');
    plot(quad_time,x)
    plot(quad_time,y,'r-')
    plottool(1,'X/Ydot',18,'Time (Hr)','Speed w/ Filter (m/s)');
    plot(quad_time,xdot_f)
    plot(quad_time,ydot_f,'g-')
    plot(quad_time,zdot,'r-')
    plottool(1,'Speed',18,'Time (hr)','Lateral Speed (m/s)');
    plot(quad_time,xyzdot)
    legend('X','Y','Z')
end

%%%%shit. We need to interpolate this too. 
xyzdot_interp = zeros(3,length(pitot_time));
ptp_interp = zeros(3,length(pitot_time));
for jdx = 1:3
    xyzdot_interp(jdx,:) = interp1(quad_time,xyzdot(jdx,:),pitot_time,'linear',0);
    ptp_interp(jdx,:) = interp1(quad_time,ptp(jdx,:),pitot_time,'linear',0);
end
%%%%Now we can loop through the pitot probes and add up the data
ctr = 1;
Vatm = zeros(3,length(pitot_time));

%%%%Ok let's kick off some plots
colors = ['b','r','g','k'];
if MUCHO_PLOTS
[figRaw,axRaw] = plottool(1,'Raw Bits',18,'Time (Hr)','Raw Bits (0-1023)');
end
[FIGwindspeed,AXwindspeed] = plottool(1,'Raw Windspeed',18,'Time (Hr)','Windspeed (m/s)');
[FIG_NESW,AX_NESW] = plottool(1,'North/East/South/West Windspeed (m/s)',18,'Time (hr)','Windspeed (m/s)');
[FIGwindspeed_rotation,AXwindspeed_rotation] = plottool(1,'Windspeed with Rotation of Vehicle',18,'Time (Hr)','Windspeed (m/s)');
[FIGwindspeed_inertial,AXwindspeed_inertial] = plottool(1,'Windspeed with Orientation of Vehicle',18,'Time (Hr)','Windspeed (m/s)');

for idx = 17:20
    %%%Step 1. Get measured pitot probe signals and convert to windspeed
    raw_bits = pitot_data(:,idx);

    if MUCHO_PLOTS
      plot(axRaw,pitot_time,raw_bits,colors(ctr))
    end
    
    %%%%Get Calibration Value
    if CAL_TIMES(1) == -99
      CAL_START = 0;
      CAL_END = 20;
    end
    
    %%Convert CAL_TIMES to hours
    CAL_START = CAL_START/3600;
    CAL_END = CAL_END/3600;
    s = find(pitot_time>CAL_START+pitot_time(1),1);
    l = find(pitot_time>CAL_END+pitot_time(1),1);
    average_bits = mean(raw_bits(s:l))
    
    %%%Run the raw bits through the truncation filter
    truncation_bits = raw_bits; %%%%UPDATE THIS
    truncation_bits(abs(truncation_bits-average_bits)<=TRUNCATION_THRESHOLD)=average_bits;

    %%%Run the truncation bits through a low pass filter
    [tfilter,filtered_bits] = LowPass(truncation_bits,pitot_time*3600,WC);
    
    %%%Convert raw bits to voltage
    raw_voltage = filtered_bits*5/1023;
        
    %%%Scale by a value
    v_offset = average_bits*5/1023; 
    calibrated_voltage = raw_voltage - v_offset;
    
    %%%%calibrated voltage is linearly proportional to pressure in Kpa
    pressure_kpa = calibrated_voltage;
    
    %%%%convert to atmospheres using the pressure of the ambient area
    ambient_pressure = pitot_data(:,22);
    % if ambient_pressure(1) ~= -99
    %     pressure_atm = pressure_kpa./ambient_pressure;
    % else
    pressure_atm = pressure_kpa/101.325;
    % end
        
    %%%Make sure anything less than -1 is truncated
    pressure_atm(pressure_atm<-1)=-1;
    %%%use bernoulli's to get k
    k = 5*((pressure_atm+1).^(2/7)-1);
    %%%make sure anything less than zero is truncated
    k(k<0) = 0;
    
    %%%PLOT the bits
    if MUCHO_PLOTS
      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)','Bits and Stuff');
      plot(pitot_time,raw_bits)
      plot(pitot_time,truncation_bits,'g-')
      plot(pitot_time,filtered_bits,'r-')
      legend('Raw Bits','Truncated Bits','Filtered Bits')
      
      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)','Voltage (V)');
      plot(pitot_time,raw_voltage)
      
      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)','Scaled Voltage (V)');
      plot(pitot_time,calibrated_voltage)

      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)',['Change in Ambient Pressure']);
      plot(pitot_time,ambient_pressure-ambient_pressure(1))
    
      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)','Pressure (kPA)');
      plot(pitot_time,pressure_kpa)
        
      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)','Pressure (ATM)');
      plot(pitot_time,pressure_atm)

      plottool(1,['Sensor =',num2str(ctr)],18,'Time (Hr)','K');
      plot(pitot_time,k)
    end
    
    %%%Get temperature
    temperature = pitot_data(:,21);
    if temperature(1) == -99
        temperature = 20;
    end
    
    %%%Get speed of sound
    a_inf = sqrt(1.4*286*temperature);
    %%%Convert to airspeed
    airspeed_ms = a_inf.*sqrt(k);
    
    %%%Zero out everything before cal_start
    airspeed_ms(1:s) = 0;
    %%%we then need to filter this through a complimentary filter but I'll
    %%%leave it for now
    airspeed_ms_filtered = Complimentary(airspeed_ms,SIG);
    %%%%ok now we multiply the signal by our nhat thingy
    Vpitot = nhat(:,ctr)*airspeed_ms_filtered';
    
    plot(AXwindspeed,pitot_time,airspeed_ms_filtered,colors(ctr));
    
    plot(AX_NESW,pitot_time,Vpitot)
    
    if ROTATION
      %%%From here we substract off omega x r
      qL = length(quad_data(:,11));
      omegacrossr = zeros(3,qL);
      for jdx = 1:qL
        omegacrossr(:,jdx) = cross(pqr(:,jdx),rQP(:,ctr));
      end
      %%%But unfortunately omegacrossr and Vpitot are from two different
      %%%sensors. So we have to interpolate first. ugh.
      omegacrossr_interp = zeros(3,length(pitot_time));
      for jdx = 1:3
        omegacrossr_interp(jdx,:) = interp1(quad_time,omegacrossr(jdx,:),pitot_time,'linear',0);
      end
      Vpitot = Vpitot - omegacrossr_interp;
    end
    
    plot(AXwindspeed_rotation,pitot_time,Vpitot)

    if INERTIAL
      %%%Alright. Now we can loop through pitot time and get Vpitot_intertial
      %%%Now we need to rotate the pitot probe to the inertial frame
      Vpitot_inertial = Vpitot;
      for jdx = 1:length(pitot_time)
        TIB = R123(ptp_interp(:,jdx));
        %TIB = eye(3);
        Vpitot_inertial(:,jdx) = TIB*Vpitot(:,jdx);
      end
    else
      Vpitot_inertial = Vpitot;
    end
    
    plot(AXwindspeed_inertial,pitot_time,Vpitot_inertial)
    
    Vatm = Vatm + Vpitot_inertial;
    
    ctr = ctr + 1;
end

if TRANSLATION
    %%%Finally we can substract off the velocity of the quad.
    %%%And add it to our Vatm vector
    Vatm = Vatm + (Vpitot_inertial - xyzdot_interp);
end

plottool(1,'Atmosphere',18,'Time (Hr)','Atmospheric Windspeed (m/s)');
plot(pitot_time,Vatm')

