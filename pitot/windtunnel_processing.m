function windtunnel_processing()
close all

data = csvread('datas.csv');

time = data(:,1);

%%%Strip time to less than 560
loc = time < 560;
time = time(loc);
vel = data(loc,2);
plot(time,vel)
hold on

start = 1;
averages = [];
for idx = 2:length(time)
  %%%Fit a regression line to it
  P = polyfit(time(start:idx),vel(start:idx),1);
  %%%P(1) is the slope
  if P(1) > 0.005 && length(start:idx) > 50 && abs(time(idx)-time(start)) >30
    %%%Compute average
    averages = [averages;mean(vel(start:idx))];
    %%%Plot some debugging
    makemyfit(P,start,idx,time);
    %%Start over
    start = idx-1;
  end
end
%%%Plot the last one
start = makemyfit(P,start,idx,time);
%%And get the last average
%%%Compute average
averages = [averages;mean(vel(start:idx))]

figure()
plot(0:5:40,averages,'b-*')


function start = makemyfit(P,start,idx,time)

%%%Create a fit
xfit = time(start:idx);
yfit = polyval(P,xfit);
%%%Plot it
plot(xfit,yfit,'r-')
%%%Plot start and end markers
%plot(xfit(1),yfit(1),'gs','MarkerSize',20)
%plot(xfit(end),yfit(end),'cs','MarkerSize',20)


