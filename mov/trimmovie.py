#!/usr/bin/python

import sys
import datetime as D
import os

if len(sys.argv) < 4:
   print('Need Filename, start time and end time in HH:MM:SS')
   sys.exit()

print('Filename = ',sys.argv[1])
print('Start Time = ',sys.argv[2])
print('End Time = ',sys.argv[3])

##Need to compute duration
start_vec = sys.argv[2].split(':')
print(start_vec)
end_vec = sys.argv[3].split(':')

start_time = D.datetime(2000,01,01,int(start_vec[0]),int(start_vec[1]),int(start_vec[2]))
end_time = D.datetime(2000,01,01,int(end_vec[0]),int(end_vec[1]),int(end_vec[2]))

print(start_time)
print(end_time)

duration = end_time - start_time

print(duration)

seconds_duration = duration.seconds

hours_duration = int(seconds_duration/3600.0)

seconds_duration -= 3600*hours_duration

minutes_duration = int(seconds_duration/60.0)

seconds_duration -= 60*minutes_duration

print(hours_duration)
print(minutes_duration)
print(seconds_duration)

duration_str = str(hours_duration) + ':' + str(minutes_duration) + ':' + str(seconds_duration)

print(duration_str)

trim_command = 'ffmpeg -ss ' + sys.argv[2] + ' -i ' + sys.argv[1] + ' -to ' + duration_str + ' -c copy trimmed_file.MP4'

print(trim_command)
#ffmpeg -ss $2 -i $1 -to $duration -c copy trimmed_file.MP4

os.system(trim_command)
