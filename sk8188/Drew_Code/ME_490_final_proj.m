clear
clc
close all
%%% extracts the data from the excel file
[num,txt,all] = xlsread('Ultraskate_results.xls');
%%% finds the number of rows and columns of data
[row col] = size(all);

for idx = 2:row
    %%% creates a structure with all of the needed parameters
    rider(idx-1).position = all{idx,1};
    rider(idx-1).name = all{idx,3};
    rider(idx-1).time = all{idx,4};
    rider(idx-1).age = all{idx,7};
    rider(idx-1).gender = all{idx,8};
    rider(idx-1).city = all{idx,10};
    rider(idx-1).state = all{idx,11};
    rider(idx-1).country = all{idx,12};
    rider(idx-1).laps = all{idx,13};
    rider(idx-1).fastest_lap = all{idx,14};
    rider(idx-1).average_lap_time = all{idx,16};
    rider(idx-1).distance = all{idx,17};
    dist(idx-1) = all{idx,17};
    %%% routine for calculating the average speed of each skater
    if length(rider(idx-1).time) == 8
        hour_ride = str2num(rider(idx-1).time(1:2));
        min_ride = str2num(rider(idx-1).time(4:5));
        sec_ride = str2num(rider(idx-1).time(7:8));
        min_dec = min_ride/60;
        sec_dec = sec_ride/3600;
        time_dec = min_dec + sec_dec;
        ride_hours = hour_ride + time_dec;
        avg_vel = rider(idx-1).distance/ride_hours;
        rider(idx-1).average_speed = avg_vel;
        velocity(idx-1) = avg_vel;
    else 
        hour_ride = str2num(rider(idx-1).time(1));
        min_ride = str2num(rider(idx-1).time(3:4));
        sec_ride = str2num(rider(idx-1).time(6:7));
        min_dec = min_ride/60;
        sec_dec = sec_ride/3600;
        time_dec = min_dec + sec_dec;
        ride_hours = hour_ride + time_dec;
        avg_vel = rider(idx-1).distance/ride_hours;
        rider(idx-1).average_speed = avg_vel;
        velocity(idx-1) = avg_vel;
    end
    
    
    
end
%%% counter variable intialization
speed_age_011_count = 0;
speed_age_1021_count = 0;
speed_age_2031_count = 0;
speed_age_3041_count = 0;
speed_age_4051_count = 0;
speed_age_5061_count = 0;
%%% finds the speeds for all riders in each age group and their position in
%%% the array
for idx = 1:length(rider)

   age = rider(idx).age;
   speed = rider(idx).average_speed;
   if age > 0 && age < 11
    speed_age_011_count = speed_age_011_count + 1;
    speed_mat_011(1,speed_age_011_count) = speed;
    speed_mat_011(2,speed_age_011_count) = idx;
   elseif age > 10 && age < 21
    speed_age_1021_count = speed_age_1021_count + 1;
    speed_mat_1021(1,speed_age_1021_count) = speed;
    speed_mat_1021(2,speed_age_1021_count) = idx;
   elseif age > 20 && age < 31
    speed_age_2031_count = speed_age_2031_count + 1;
    speed_mat_2031(1,speed_age_2031_count) = speed;
    speed_mat_2031(2,speed_age_2031_count) = idx;
   elseif age > 30 && age < 41
    speed_age_3041_count = speed_age_3041_count + 1;
    speed_mat_3041(1,speed_age_3041_count) = speed;
    speed_mat_3041(2,speed_age_3041_count) = idx;
   elseif age > 40 && age < 51
    speed_age_4051_count = speed_age_4051_count + 1;
    speed_mat_4051(1,speed_age_4051_count) = speed;
    speed_mat_4051(2,speed_age_4051_count) = idx;
   elseif age > 50 && age < 61    
    speed_age_5061_count = speed_age_5061_count + 1;
    speed_mat_5061(1,speed_age_5061_count) = speed;
    speed_mat_5061(2,speed_age_5061_count) = idx;
   end
end
%%% finds the youngest aged person in the competition and their position in
%%% the array
young_age = min(num(:,7));
young_pos = find(num(:,7) == young_age);

%%% Displays the youngest riders in the competition
for idx = 1:length(young_pos)
    disp('Youngest Riders')
    rider(young_pos(idx)-1)
end
%%% finds the oldest aged person in the competition and their position in
%%% the array
old_age = max(num(:,7));
old_pos = find(num(:,7) == old_age);
%%% Displays the oldest riders in the competition
for idx = 1:length(old_pos)
    disp('Oldest Riders')
    rider(old_pos(idx)-1)
end
%%% finds the array location of the fastest skater in each age group
speed_011_loc = speed_mat_011(2,find(speed_mat_011(1,:) == max(speed_mat_011(1,:))));
speed_1021_loc = speed_mat_1021(2,find(speed_mat_1021(1,:) == max(speed_mat_1021(1,:))));
speed_2031_loc = speed_mat_2031(2,find(speed_mat_2031(1,:) == max(speed_mat_2031(1,:))));
speed_3041_loc = speed_mat_3041(2,find(speed_mat_3041(1,:) == max(speed_mat_3041(1,:))));
speed_4051_loc = speed_mat_4051(2,find(speed_mat_4051(1,:) == max(speed_mat_4051(1,:))));
speed_5061_loc = speed_mat_5061(2,find(speed_mat_5061(1,:) == max(speed_mat_5061(1,:))));
%%% Puts the rider structures into age groups based on decades
for idx = 1:length(rider)
    
    age  = rider(idx).age;
    
    if age > 0 && age < 11
        disp('Age Group 1-10')
        if idx == speed_011_loc
           disp('Fastest Rider in Current Age Group'); 
        end
        rider(idx)
    end
end

for idx = 1:length(rider)
    
    age  = rider(idx).age;
    
    if age > 10 && age < 21
        disp('Age Group 11-20')
        if idx == speed_1021_loc
           disp('Fastest Rider in Current Age Group'); 
        end        
        rider(idx)
    end
end

for idx = 1:length(rider)
    
    age  = rider(idx).age;
    
    if age > 20 && age < 31
        disp('Age Group 21-30')
        if idx == speed_2031_loc
           disp('Fastest Rider in Current Age Group'); 
        end        
        rider(idx)
    end
end

for idx = 1:length(rider)
    
    age  = rider(idx).age;
    
    if age > 30 && age < 41
        disp('Age Group 31-40')
        if idx == speed_3041_loc
           disp('Fastest Rider in Current Age Group'); 
        end        
        rider(idx)
    end
end

for idx = 1:length(rider)
    
    age  = rider(idx).age;
    
    if age > 40 && age < 51
        disp('Age Group 41-50')
        if idx == speed_4051_loc
           disp('Fastest Rider in Current Age Group'); 
        end        
        rider(idx)
    end
end

for idx = 1:length(rider)
    
    age  = rider(idx).age;
    
    if age > 50 && age < 61
        disp('Age Group 51-60')
        if idx == speed_5061_loc
           disp('Fastest Rider in Current Age Group'); 
        end        
        rider(idx)
    end
end
%%% minute and second variable initialization
pos_min = 100;
pos_sec = 100;
%%% finds the rider with the fastest lap time
for idx = 1:length(rider)

    if length(rider(idx).fastest_lap) < 5
        
        if str2num(rider(idx).fastest_lap(1)) < pos_min
            
            if str2num(rider(idx).fastest_lap(3:4)) < pos_sec
            
                pos_min = str2num(rider(idx).fastest_lap(1));
                pos_sec = str2num(rider(idx).fastest_lap(3:4));
                rider_num = idx;
            end
        end
    end
end
disp('Fastest Lap Rider')
rider(rider_num)
%%% finds the number of countries that participated in the competition and
%%% their names and then constructs a pie chart of that information
countries = all(2:end,12);
country_cat = categorical(countries);
[count,countries] = hist(country_cat);
disp('Countries that participated in the Competition');
countries
disp('Number of countries that participated in the Competition');
length(count)
figure();
pie(count)
title('Pie Chart of Countries Participating in UltraSkate 2016','FontSize',18)
legend(countries,'Location','EastOutside','Orientation','Vertical')
%%% creates a histogram for the distances rode by the skaters
figure();
hist(dist)
xlabel('Distance Rode (miles)','FontSize',18)
ylabel('Frequency','FontSize',18)
title('Histogram of Distances Rode in UltraSkate 2016','FontSize',18)
%%% creates a histogram for the average speeds of the skaters
figure();
hist(velocity)
xlabel('Average Speed (mph)','FontSize',18)
ylabel('Frequency','FontSize',18)
title('Histogram of Average Speeds in UltraSkate 2016','FontSize',18)


