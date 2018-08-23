#%%Import packages
import numpy as np
from random import random
import matplotlib.pyplot as plt
from gekko import GEKKO

# noise level
noise = 0.2

#%% Process
p = GEKKO(remote=False)
p.time = [0,.5] #time discretization

#Parameters
p.u = p.MV()
p.K = p.Param(value=1.25) #gain
p.tau = p.Param(value=8) #time constant

#variable
p.y = p.CV(1) #measurement

#Equations
p.Equation(p.tau * p.y.dt() == -p.y + p.K * p.u)

#options
p.options.IMODE = 4
p.options.NODES = 4

def process_simulator(meas):
    if meas is not None:
        p.u.MEAS = meas
    p.solve(disp=False)
    
    return p.y.MODEL + (random()-0.5)*noise


#%% MPC Model
c = GEKKO(remote=False)
c.time = np.linspace(0,5,11) #horizon to 5 with discretization of 0.5

#Parameters
u = c.MV(lb=-10,ub=10) #input
K = c.Param(value=1) #gain
tau = c.Param(value=10) #time constant
#Variables
y = c.CV(1) 
#Equations
c.Equation(tau * y.dt() == -y + u * K)
#Options
c.options.IMODE = 6     #MPC
c.options.CV_TYPE = 1   #l1 norm
c.options.NODES = 3

y.STATUS = 1            #write MPC objective
y.FSTATUS = 1           #recieve measurements
y.SPHI = 3.1            
y.SPLO = 2.9

u.STATUS = 1            #enable optimization of MV
u.FSTATUS = 0           #no feedback
u.DCOST = 0.05          #discourage unnecessary movement

#%% Time loop
cycles = 50
time = np.linspace(0,cycles*.5,cycles) 
y_meas = np.empty(cycles)
u_cont = np.empty(cycles)

for i in range(cycles):
    #process 
    y_meas[i] = process_simulator(u.NEWVAL)
    
    #controller
    if i == 24: ##change setpoint half way through
        y.SPHI = 6.1
        y.SPLO = 5.9
    y.MEAS = y_meas[i]
    c.solve(disp=True,GUI=True)
    u_cont[i] = u.NEWVAL
    
#%% Plot results
plt.figure()
plt.subplot(2,1,1)
plt.plot(time,y_meas)
plt.ylabel('y')
plt.subplot(2,1,2)
plt.plot(time,u_cont)
plt.ylabel('u')
plt.xlabel('time')

#% add setpoint bars on graph
o = np.ones(int(cycles/2))
time1 = np.linspace(0,cycles*.25,int(cycles/2))
time2 = np.linspace(cycles*.25,cycles*.5,int(cycles/2))
plt.subplot(2,1,1)
plt.plot(time1,o*2.9,'k--')
plt.plot(time1,o*3.1,'k--')
plt.plot(time2,o*5.9,'k--')
plt.plot(time2,o*6.1,'k--')



