# -*- coding: utf-8 -*-

from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt

#%% NMPC model
m = GEKKO(remote=False)
m.time = np.linspace(0,5,51)

#Model Parameters
q = m.Param(value=100)
V = m.Param(value=100)
rho = m.Param(value=1000)
Cp = m.Param(value=0.239)
mdelH = m.Param(value=50000)
ER = m.Param(value=8750)
k0 = m.Param(value=7.2*10**10)
UA = m.Param(value=5*10**4)
Ca0 = m.Param(value=1)
T0 = m.Param(value=350)

#Variables
k = m.Var()
rate = m.Var()
T = m.Var(value=325,lb=250,ub=500)

#MV
Tc = m.MV(value=300,lb=250,ub=350)
#CV
Ca = m.CV(value=.7, ub=1, lb=0)

#Equations
m.Equation(k==k0*m.exp(-ER/T))
m.Equation(rate==k*Ca)
m.Equation(V* Ca.dt() == q*(Ca0-Ca)-V*rate)
m.Equation(rho*Cp*V* T.dt() == q*rho*Cp*(T0-T) + V*mdelH*rate + UA*(Tc-T))

#Global options
m.options.IMODE = 6 #MPC
m.options.CV_TYPE = 2

#MV tuning
Tc.STATUS = 1
Tc.DCOST = .01

#CV Tuning
Ca.STATUS = 1
if m.options.CV_TYPE == 1:
    Ca.SPHI = 0.51
    Ca.SPLO = 0.49
elif m.options.CV_TYPE == 2:
    Ca.SP = .5

m.solve()

## Plot
if m.options.IMODE > 3:
    plt.figure()
    plt.plot(m.time,Ca.value)
    if m.options.CV_TYPE == 1:
        plt.plot(m.time,np.ones(51)*0.51,'k--')
        plt.plot(m.time,np.ones(51)*0.49,'k--')
    else:
        plt.plot(m.time,np.ones(51)*0.5,'k--')
    plt.xlabel('Time')
    plt.ylabel('Ca')
    
    plt.figure()
    plt.plot(m.time,Tc.value)
    plt.xlabel('Time')
    plt.ylabel('Tc')