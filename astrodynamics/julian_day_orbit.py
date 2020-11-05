#!/usr/bin/python

from pdf import *
from Universe import *
import matplotlib.pyplot as plt

#This will plot the position of the planets on a given Julian Day

#Here is the Julian Day
#julian_day = 2444240 ##this is jan 1 1980 #this was a leap year
#julian_day = 2445701 #this is jan 1 1984 #1984 was a leap year
julian_day = 2446796 ##this is jan 1 1987
#julian_day = 2447162 ##this is jan 1 1988 #1988 was a leap year
#julian_day = 2451545. ##this is jan 1 2000
#julian_day = 2458120. ##this is jan 1 2018
#julian_day = 2458485 ##this is jan 1 2019
#julian_day = 2458850 ##this is jan 1 2020
# + 275 October 2
# - 10 to get to the winter solstice
# + 79 to get to the spring equinox
# + 172 to get to the summer solstice
# + 245 to get to Sep 2nd
# + 265 to get to the fall equinox
julian_day += 245 #Sep 2nd

##Then compute all the planets using the JPL class
planets = JPL(julian_day)

#Finally compute all the orbits
planets.MilkyWay.Orbit()

##Finally Plot the Output of the Systems
print('Creating Plots')
pp = PDF(0,plt)

planets.MilkyWay.PlotOrbit(pp,-1)

##Only plot inner planets
planets.MilkyWay.numsatellites = 5
planets.MilkyWay.PlotOrbit(pp,-1)
pp.close()

##Use Mayavi if you're using Python3
planets.MilkyWay.numsatellites = 10
planets.MilkyWay.PlotMayavi()
