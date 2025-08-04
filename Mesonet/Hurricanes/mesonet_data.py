import numpy as np
import matplotlib.pyplot as plt

#data = np.loadtxt("mobileusaw_2020-10-27_2020-10-29_Clipped.csv",delimiter=',')

#fid = open("mobileusaw_2020-10-27_2020-10-29_.csv")
fid = open("mobileusaw_2020-10-27_2020-10-29_max.csv")

data = fid.readlines()

def getData(col,data,name):
	print('Getting Column = ',col," Name = ",name)
	ctr = 0
	out = []
	for line in data:
		row = line.split(',')
		if ctr == 0:
			print(row)
		else:
			f = row[col].strip("\"")
			g = f.rstrip('\n')
			h = g.rstrip('\"')
			out.append(float(h.rstrip('\n')))
		ctr+=1
		#hour = row[5]
		#minute = row[6]
		#speed2 = row[9]
		#speed10 = row[10]
	out = np.asarray(out)
	return out

def makePlot(x,y,xla,yla):
	plt.figure()
	plt.plot(x,y)
	plt.xlabel(xla)
	plt.ylabel(yla)
	plt.grid()

ms2mph = 2.23694

day = getData(3,data,"DAY")
hour = getData(5,data,"HOUR")
minute = getData(6,data,"MINUTE")

##_data
#speed2 = getData(9,data,"SPEED2")*ms2mph
#speed10 = getData(10,data,"SPEED10")*ms2mph
#windir2 = getData(7,data,"DIR2")
#windir10 = getData(8,data,"DIR10")

###_max data
speed10max = getData(7,data,"SPEED10MAX")*ms2mph

time = day + hour/24.0 + (minute/60.0)/24.0

#_data
#makePlot(time,speed2,"Time (day)","Speed @ 2m (mph)")
#makePlot(time,speed10,"Time (day)","Speed @ 10m (mph)")
#makePlot(time,windir2,"Time (day)","Direction @ 2 m")
#makePlot(time,windir10,"Time (day)","Direction @ 10 m")

#_max_data
makePlot(time,speed10max,"Time (day)","Speed @ 10m Maximum (mph)")

plt.show()