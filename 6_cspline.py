# -*- coding: utf-8 -*-

from gekko import GEKKO 
import numpy as np
import matplotlib.pyplot as plt

def f(x): # function to generate data for cspline
    return 3*np.sin(x) - (x-3) 

x_data = np.random.rand(50)*10+10
y_data = f(x_data)

c = GEKKO()
x = c.Var(value=np.random.rand(1)*10+10) #initialize at random point
y = c.Var()
c.cspline(x,y,x_data,y_data,True)
c.Obj(y)
c.solve(disp=False)

plt.figure()
plt.scatter(x_data,y_data,5,'b')
plt.scatter(x.value,y.value,200,'r','x')