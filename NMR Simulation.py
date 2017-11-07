# -*- coding: utf-8 -*-
"""
Created on Fri Sep 9 17:34:31 2016
@author: Arnold Choa
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import matplotlib.animation as animation

gProton = 2.675E8 # gyromagnetic ratio of a proton in rad/s
BEarth = 60E-6
period = 2*np.pi/(gProton*BEarth) # period in seconds

def BField(t):
    # Piecewise function for the Magnetic Field
    # Takes in time and outputs a unit vector in direction
    # of magnetic field
    omega = gProton*BEarth # Angular Frequency. Change for cases
    N = 100 #Scaling Magnitude Kick for Precession. Change for cases
    k = 3E8 #Steepness of Sigmoid curves
    Bx = (( 1/(1+ np.exp(-k*(t-10*period)))) - \
    ( 1/(1+ np.exp(-k*(t-60*period)))))*(BEarth*(np.sin(omega*t))/N)
    """# Spinning one
    return np.array([BEarth*(np.sin(2*np.pi*t/period))/100,0,BEarth])
    """
    """ #Constant Efield
    return np.array([0,0,BEarth])
    """
    """#Switching Field
    if(t<3.5*period):
    return np.array([0,0,BEarth])
    else:
    return np.array([0,BEarth,0])
    """
    """#Piecewise
    if(t<10*period):
    return np.array([0,0,BEarth])
    elif(t<60*period):
    return np.array([BEarth*(np.sin(omega*t))/N,0,BEarth])
    else:
    return np.array([0,0,BEarth])
    """
    #Sigmoid Function to Replicate Piecewise
    return np.array([Bx,0,BEarth])

def dmdt(m,t):
    return gProton*np.cross(m,BField(t))

class spinDirection:
    """Spin Direction Properties
    Unit vector
    x = spin direction in x-direction
    y = spin direction in y direction
    z = spin direction in z-direction
    g = gyromagnetic ratio
    """
    
    def __init__(self,
        x = 1.,
        y = 0.,
        z = 0.,
        g = 0.5,
        ):
        # Initializing Function of spinDirection
        x,y,z = ((x/(np.sqrt(x**2 + y**2 + z**2))),
        (y/(np.sqrt(x**2 + y**2 + z**2))),
        (z/(np.sqrt(x**2 + y**2 + z**2)))
        )
        self.spin = np.array([x, y, z])
        self.g = g
        self.historyt = []
        self.historyx = []
        self.historyy = []
        self.historyz = []
        self.historytheta = []
        self.historyphi=[]
        
    def odeForTime(self,init,final):
        y0 = self.spin
        t0 = init
        tf = final
        steps = 10000 #Number of step I want odeint to do
        self.historyt = np.linspace(t0,tf,steps)
        a = odeint(dmdt, y0, self.historyt)
        x = a[:,0]
        y = a[:,1]
        z = a[:,2]
        r = (x**2 + y**2 + z**2)**0.5
        self.historyx = x
        self.historyy = y
        self.historyz = z
        self.historyphi = np.arccos(z/r)
        self.historytheta = np.arctan(y/x)
    
"""Initialize spin direction
"""
spin = spinDirection(0,0,1,gProton) #Initial Position at (0,0,1)
spin.odeForTime(0, 70*period) # My now crucial step
titles = r"$\omega \ =\ 1.0\gamma B_{E}\ ;\ N\ =\ 100$"# Title of Graphs
plt.figure(0)
plt.plot(spin.historyt,spin.historyx, label = "x")
plt.plot(spin.historyt,spin.historyy, label = "y")
plt.plot(spin.historyt,spin.historyz, label = "z")
plt.legend()
plt.title(titles)
plt.figure(1)
plt.plot(spin.historyt,spin.historytheta, label = "theta")
plt.plot(spin.historyt,spin.historyphi, label = "phi")
plt.legend()
plt.title(titles)
print("Drawing")
fig = plt.figure(2)
ax = fig.gca(projection='3d')
ax.set_xlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_zlim3d(-1, 1)
ax.plot(spin.historyx, spin.historyy, spin.historyz)
plt.title(titles)

def hello():
    x, y, z = spin.historyx[0::10], spin.historyy[0::10], spin.historyz[0::10]
    particle = np.vstack((x, y, z))
    return particle

def animate(num, dataLines, lines) :
    for line, data in zip(lines, dataLines) :
        line.set_data(data[0:2, :num])
        line.set_3d_properties(data[2,:num])
    return lines

# Attach 3D axis to the figure
fig2 = plt.figure(3)
ax2 = fig2.gca(projection ='3d')
data = [hello()]
lines = [ax2.plot(data[0][0,0:1], data[0][1,0:1], data[0][2,0:1], '-')[0]]
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
q = np.outer(np.cos(u), np.sin(v))
w = np.outer(np.sin(u), np.sin(v))
e = np.outer(np.ones(np.size(u)), np.cos(v))
ax2.plot_surface(q, w, e, rstride=6, cstride=6, color='orange')
# Set the axes properties
ax2.set_xlim3d([-1.0, 1.0])
ax2.set_xlabel('X')
ax2.set_ylim3d([-1.0, 1.0])
ax2.set_ylabel('Y')
ax2.set_zlim3d([-1.0, 1.0])
ax2.set_zlabel('Z')
ax2.set_title(titles)
# Creating the Animation object
ani = animation.FuncAnimation(fig2, animate, frames = len(spin.historyt),
fargs=(data, lines), interval=1E-5, blit=False)
plt.show()