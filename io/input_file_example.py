import numpy as np

def get_num(row):
    split = row.split('!')
    num = np.float(split[0])
    return num

def get_user_inputs():
    file = open('Input.txt','r')
    all = file.read()
    rows = all.split('\n')
    #print(rows)
    speed = get_num(rows[0]) 
    heading = get_num(rows[1])
    vx = get_num(rows[2])
    vy = get_num(rows[3])
    v = [vx,vy]
    waypoints = int(get_num(rows[4]))
    counter = 5
    xy = []
    for idx in range(0,waypoints):
        #print('Getting waypoint',idx+1)
        coordinate = []
        coordinate.append(get_num(rows[counter]))
        coordinate.append(get_num(rows[counter+1]))
        xy.append(coordinate)
        counter+=2
    return speed,heading,waypoints,xy,v

####BEGINNING OF CODE
speed,heading,waypoints,xy,v = get_user_inputs()
print('Speed (mph) = ',speed)
print('Heading (deg) = ',heading)
print('Number of Waypoints = ',waypoints)
print(xy)
print('Actual Current (mph) = ',v)

###ESTIMATE THE CURRENT
vxguess = v[0] + np.random.normal(0,2)
print('Vx Guess = ',vxguess)