import numpy as np 
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import mpl_toolkits.mplot3d as a3
import matplotlib.patches as patch

##In order to import this toolbox into a python script you need to 
##do the following. Copy the following lines of code below
# import sys
# sys.path.append('/home/carlos/Dropbox/BlackBox/plotting')
# from plotting import *

# or

# In order to get python to search for all of your lovely blackbox 
# python routines. Add this to your .bashrc file

# for d in /home/carlos/Dropbox/BlackBox/*/; do
# 	PYTHONPATH+=:$d
# done
# export PYTHONPATH

def xlim_auto(x0,xf,x,y):
    plt.xlim([x0,xf])
    lims = plt.gca().get_xlim()
    i = np.where( (x > lims[0]) &  (x < lims[1]) )[0]
    miny = np.min(y[i])
    if miny < 0:
        miny *= 1.15
    else:
        miny *= 0.85
    plt.ylim([miny,1.15*np.max(y[i])])

def plottool(fontsize,xlabel,ylabel,title):
    # print(type(fontsize))
    # print(type(str))
    if type(fontsize) != type('s'):
        plt.rcParams.update({'font.size': fontsize})
    fig = plt.figure()
    rect = fig.patch
    rect.set_facecolor('white')
    plti = fig.add_subplot(1,1,1)
    plti.grid()
    plti.set_xlabel(xlabel)
    plti.set_ylabel(ylabel)
    plti.set_title(title)
    plti.get_yaxis().get_major_formatter().set_useOffset(False)
    plti.get_xaxis().get_major_formatter().set_useOffset(False)
    if title == 'Latitude vs. Longitude':
        print('Fixing Left Axis')
        plt.gcf().subplots_adjust(left=0.18)
    return plti

def plotmesh(X,Y,Z,xlabel,ylabel,zlabel,title):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Plot the surface.
    # Make data.
    #X = np.arange(-5, 5, 0.01)
    #Y = np.arange(-5, 5, 0.01)
    #X, Y = np.meshgrid(X, Y)
    #R = np.sqrt(X**2 + Y**2)
    #Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,linewidth=1, antialiased=False)
    ax.scatter(X, Y, Z)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=5)
    return ax

def plotwire(X,Y,Z,xlabel,ylabel,zlabel,title):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Plot the surface.
    # Make data.
    #X = np.arange(-5, 5, 0.01)
    #Y = np.arange(-5, 5, 0.01)
    #X, Y = np.meshgrid(X, Y)
    #R = np.sqrt(X**2 + Y**2)
    #Z = np.sin(R)
    surf = ax.plot_wireframe(X, Y, Z, cmap=cm.coolwarm,linewidth=1, antialiased=False)
    ax.scatter(X, Y, Z)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # Add a color bar which maps values to colors.
    #fig.colorbar(surf, shrink=0.5, aspect=5)
    return ax

def scatter(X,Y,Z,xlabel,ylabel,zlabel,title):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Plot the surface.
    # Make data.
    #X = np.arange(-5, 5, 0.01)
    #Y = np.arange(-5, 5, 0.01)
    #X, Y = np.meshgrid(X, Y)
    #R = np.sqrt(X**2 + Y**2)
    #Z = np.sin(R)
    ax.scatter(X, Y, Z)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    # Add a color bar which maps values to colors.
    # fig.colorbar(surf, shrink=0.5, aspect=5)
    return ax

def plottool3(title,x,y,z,xlabel,ylabel,zlabel):
    fig = plt.figure('3-D')
    ax = fig.add_subplot(111,projection='3d')
    ax.plot(x,y,z, color = 'blue', linestyle = 'solid')
    plt.title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    return ax #just in case they want access to the ax variable

def MakePatch(x,y,z,ax,color):
    verts = [zip(x,y,z)]
    patch = a3.art3d.Poly3DCollection(verts)
    patch.set_color(color)
    patch.set_edgecolor('k')
    ax.add_collection3d(patch)

def CubeDraw(ax,dx,dy,dz,xc,yc,zc,phi,theta,psi,color):
    xb = np.array([1.,1.,-1.,-1.,1.,1.,-1.,-1.])*dx/2;
    yb = np.array([-1.,1.,1.,-1.,-1.,1.,1.,-1.])*dy/2;
    zb = np.array([-1.,-1.,-1.,-1.,1.,1.,1.,1.])*dz/2;
    
    T = R123(phi,theta,psi);
    
    m = len(xb)

    rc = np.array([xc,yc,zc])

    for idx in range(0,m):
        xs = xb[idx]
        ys = yb[idx]
        zs = zb[idx]
        
        xyz = np.array([xs,ys,zs])
        
        xyz_trans = rc + np.dot(T,xyz)

        xb[idx] = xyz_trans[0];
        yb[idx] = xyz_trans[1];
        zb[idx] = xyz_trans[2];

    x1 = xb[0:4]
    y1 = yb[0:4]
    z1 = zb[0:4]
    MakePatch(x1,y1,z1,ax,color)

    x2 = np.hstack([xb[0:2],xb[5],xb[4]])
    y2 = np.hstack([yb[0:2],yb[5],yb[4]])
    z2 = np.hstack([zb[0:2],zb[5],zb[4]])
    MakePatch(x2,y2,z2,ax,color)

    x3 = np.hstack([xb[1:3],xb[6],xb[5]])
    y3 = np.hstack([yb[1:3],yb[6],yb[5]])
    z3 = np.hstack([zb[1:3],zb[6],zb[5]])
    MakePatch(x3,y3,z3,ax,color)

    x4 = np.hstack([xb[2:4],xb[7],xb[6]])
    y4 = np.hstack([yb[2:4],yb[7],yb[6]])
    z4 = np.hstack([zb[2:4],zb[7],zb[6]])
    MakePatch(x4,y4,z4,ax,color)

    x5 = np.hstack([xb[0],xb[3],xb[7],xb[4]])
    y5 = np.hstack([yb[0],yb[3],yb[7],yb[4]])
    z5 = np.hstack([zb[0],zb[3],zb[7],zb[4]])
    MakePatch(x5,y5,z5,ax,color)

    x6 = xb[4:8]
    y6 = yb[4:8]
    z6 = zb[4:8]
    MakePatch(x6,y6,z6,ax,color)


# Copyright - Carlos Montalvo 2016
# You may freely distribute this file but please keep my name in here
# as the original owner
