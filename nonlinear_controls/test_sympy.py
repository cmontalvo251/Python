


import sympy as S


g = S.Symbol('g')
theta = S.Symbol('theta')
x = S.Symbol('x')
l = S.Symbol('l')

eqn1 = g*theta + x*l/theta

sol = S.solve(eqn1,'theta')

print(sol)