#!/usr/bin/python

from pdf import *
import plotting as P
import mio as I
import sys
from mymath import unwrap
import numpy as np
#import plot_HAT as S
sys.path.append('FASTPitot/')
import pitot as Pit
sys.path.append('Mesonet/')
import mesonet as M
sys.path.append('Anemometer/')
import anemometer as ANEM 
import gps as GPS

pp = PDF(0,plt) #0 = pdf and 1 = show them here

dataANEM0 = I.dlmread('/home/carlos/Desktop/11_29_2017_SIDEWALK_EXPERIMENT/ANEM0.TXT',' ')
dataANEM1 = I.dlmread('/home/carlos/Desktop/11_29_2017_SIDEWALK_EXPERIMENT/ANEM1.TXT',' ')
dataFP4H = I.dlmread('/home/carlos/Desktop/11_29_2017_SIDEWALK_EXPERIMENT/FP4H.TXT',' ')
dataFP4V = I.dlmread('/home/carlos/Desktop/11_29_2017_SIDEWALK_EXPERIMENT/FP4V.TXT',' ')

plti = P.plottool(12,'Time (sec)','Temperature (C)','Temperature vs. Time')
plti.plot(dataANEM0[:,0],dataANEM0[:,8],label='R2.0')
plti.plot(dataANEM1[:,0],dataANEM1[:,8],label='R1.0+UpsideDown')
plti.plot(dataFP4H[:,0],dataFP4H[:,10],label='R1.0')
plti.plot(dataFP4V[:,0],dataFP4V[:,10],label='None')
plti.legend(loc='best')
pp.savefig()

plti = P.plottool(12,'Time (sec)','Pressure (mb)','Pressure vs. Time')
plti.plot(dataANEM0[:,0],dataANEM0[:,9],label='R2.0')
plti.plot(dataANEM1[:,0],dataANEM1[:,9],label='R1.0+UpsideDown')
plti.plot(dataFP4H[:,0],dataFP4H[:,11],label='R1.0')
plti.plot(dataFP4V[:,0],dataFP4V[:,11],label='None')
plti.legend(loc='best')
pp.savefig()

plti = P.plottool(12,'Time (sec)','Humidity (%)','Humidity vs. Time')
plti.plot(dataANEM0[:,0],dataANEM0[:,10],label='R2.0')
plti.plot(dataANEM1[:,0],dataANEM1[:,10],label='R1.0+UpsideDown')
plti.plot(dataFP4H[:,0],dataFP4H[:,12],label='R1.0')
plti.plot(dataFP4V[:,0],dataFP4V[:,12],label='None')
plti.legend(loc='best')
pp.savefig()


pp.close()

