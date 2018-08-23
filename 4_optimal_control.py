from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt

# create GEKKO model
m = GEKKO()

m.time = np.linspace(0,10,501)

# constants
E = 1
c = 17.5
r = 0.71
k = 80.5
U_max = 20

# fishing rate
u = m.MV(value=1,lb=0,ub=1)
u.STATUS = 1
u.DCOST = 0

# fish population
x = m.Var(value=70)

# fish population balance
m.Equation(x.dt() == r*x*(1-x/k)-u*U_max)

# objective (profit)
J = m.Var(value=0)
m.Equation(J.dt() == (E-c/x)*u*U_max)
# final objective
Jf = m.FV()
Jf.STATUS = 1
m.Connection(Jf,J,pos2='end')
# maximize profit
m.Obj(-Jf)

# options
m.options.IMODE = 6  # optimal control
m.options.NODES = 3  # collocation nodes

m.solve()

# print profit
print('Optimal Profit: ' + str(Jf.value[0]))

# plot results
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(m.time,J.value,'r--',label='profit')
plt.plot(m.time[-1],Jf.value[0],'ro',markersize=10)
plt.plot(m.time,x.value,'b-',label='fish population')
plt.ylabel('Value')
plt.legend()
plt.subplot(2,1,2)
plt.plot(m.time,u.value,'k.-',label='fishing rate')
plt.ylabel('Rate')
plt.xlabel('Time (yr)')
plt.legend()
plt.show()