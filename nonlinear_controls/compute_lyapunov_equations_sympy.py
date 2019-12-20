import sympy as S
import numpy as np

x = S.Symbol('x')
xdot = S.Symbol('xdot')
theta = S.Symbol('theta')
thetadot = S.Symbol('thetadot')
thetaddot = S.Symbol('thetaddot')
xddot = S.Symbol('xddot')
g = S.Symbol('g')
l = S.Symbol('l')
F = S.Symbol('F')
m = S.Symbol('m')
M = S.Symbol('M')
gamma = S.Symbol('gamma')

###Equation for xddot
#xddot = (F + m*l*thetaddot*S.cos(theta) - m*l*(thetadot**2)*S.sin(theta))/(M+m)
thetaddot = (xddot*S.cos(theta)+g*S.sin(theta))/l
##Substitude xddot into thetaddot
#eqn = (xddot*S.cos(theta) + g*S.sin(theta))/l - thetaddot
eqn = (F + m*l*thetaddot*S.cos(theta) - m*l*(thetadot**2)*S.sin(theta))/(M+m) - xddot

print('eqn = ',eqn)
#print('xddot = ',xddot)

##Solve for thetaddot
#sol = S.solvers.solve(eqn,'thetaddot')
##Solve for xddot
sol = S.solvers.solve(eqn,'xddot')

#print('thetaddot = ',sol)
print('xddot = ',sol)

##Create Lyapunov Function
#V = 0.5*M*x**2 + 0.5*M*xdot**2
#V = 0.5*m*(l**2)*thetadot**2/2. + m*g*(1-S.cos(theta))
V = 0.5*M*x**2 + 0.5*M*xdot**2 + 0.5*m*(l**2)*thetadot**2 + m*g*(1-S.cos(theta))

print('V = ',V)

##Now take Derivatives
###This is the equation for thetaddot but I'm going to use sol since I solved for it above
#Vdot = m*l**2*thetadot*thetaddot + m*g*S.sin(theta)*thetadot
#Vdot = m*l**2*thetadot*sol[0] + m*g*S.sin(theta)*thetadot
#Vdot = M*x*xdot + M*xdot*xddot + m*l**2*thetadot*thetaddot + m*g*S.sin(theta)*thetadot
#thetaddot = (xddot*S.cos(theta)+g*S.sin(theta))/l
thetaddot = (sol[0]*S.cos(theta)+g*S.sin(theta))/l
Vdot = M*x*xdot + M*xdot*sol[0] + m*l**2*thetadot*thetaddot + m*g*S.sin(theta)*thetadot
#Vdot = M*x*xdot + M*xdot*xddot
#Vdot = M*x*xdot + M*xdot*sol[0]

print('Vdot = ',Vdot)

###Make Vdot 0
#F = (1./S.cos(theta))*(-M*g*S.sin(theta) - g*m*S.sin(theta) + l*m*thetadot**2*S.sin(2*theta)/2. - S.sin(theta)*g*(M + m*S.sin(theta)**2)/l)
#F = -g*m*S.sin(2*theta)/2.+l*m*thetadot**2*S.sin(theta)-x*(M+m*S.sin(theta)**2)
F  = -g*m*S.sin(2*theta)/2. + l*m*thetadot**2*S.sin(theta)

##Copied from Terminal
#Vdot = g*m*thetadot*S.sin(theta) + l*m*thetadot*(F*S.cos(theta) + M*g*S.sin(theta) + g*m*S.sin(theta) - l*m*thetadot**2*S.sin(2*theta)/2)/(M + m*S.sin(theta)**2)
#Vdot = M*x*xdot + M*xdot*(F + g*m*S.sin(2*theta)/2 - l*m*thetadot**2*S.sin(theta))/(M + m*S.sin(theta)**2)
Vdot = M*x*xdot + M*xdot*(F + g*m*S.sin(2*theta)/2 - l*m*thetadot**2*S.sin(theta))/(M + m*S.sin(theta)**2) + g*m*thetadot*S.sin(theta) + l*m*thetadot*(g*S.sin(theta) + (F + g*m*S.sin(2*theta)/2 - l*m*thetadot**2*S.sin(theta))*S.cos(theta)/(M + m*S.sin(theta)**2))

print('Vdot with control = ',Vdot)
