#!/usr/bin/python

from pdf import *
from Universe import *
import matplotlib.pyplot as plt

#This will plot the position of the planets on a given Julian Day

#Here is the Julian Day
#julian_day = 2458120. ##this is jan 1 2018
#julian_day = 2458485 ##this is jan 1 2019
julian_day = 2458485
# - 10 to get to the winter solstice
# + 79 to get to the spring equinox
# + 172 to get to the summer solstice
# + 265 to get to the fall equinox

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
