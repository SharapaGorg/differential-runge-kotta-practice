from scipy.integrate import solve_ivp
import numpy as np

def dydx(x, y):
    return x + np.cos(y)  # пример для уравнения 1(a)

sol = solve_ivp(dydx, [1, 2], [30], method='RK45', t_eval=np.arange(1, 2, 0.1))
print(sol.y)
