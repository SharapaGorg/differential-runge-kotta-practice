from rich.console import Console
from rich.table import Table
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

console = Console()

def runge_kutta(f, y0, x0, x_end, h, order):
    n = int((x_end - x0) / h) + 1
    x = np.linspace(x0, x_end, n)
    y = np.zeros(n)
    y[0] = y0

    if order == 2:
        for i in range(1, n):
            k1 = f(x[i-1], y[i-1])
            k2 = f(x[i-1] + h, y[i-1] + h * k1)
            y[i] = y[i-1] + h * (k1 + k2) / 2
    elif order == 4:
        for i in range(1, n):
            k1 = f(x[i-1], y[i-1])
            k2 = f(x[i-1] + h / 2, y[i-1] + h * k1 / 2)
            k3 = f(x[i-1] + h / 2, y[i-1] + h * k2 / 2)
            k4 = f(x[i-1] + h, y[i-1] + h * k3)
            y[i] = y[i-1] + h * (k1 + 2*k2 + 2*k3 + k4) / 6

    return x, y

def solve_and_display(f, y0, x0, x_end, steps, order, task_label):
    results = []

    for h in steps:
        x, y = runge_kutta(f, y0, x0, x_end, h, order)
        results.append((x, y))

    rel_errors = []
    for i in range(len(steps) - 1):
        x1, y1 = results[i]
        x2, y2 = results[i+1]

        # Interpolating to compare on the same x grid
        interp_func = interp1d(x2, y2, kind='cubic')
        y1_interp = interp_func(x1[:len(x2)])
        error = np.abs(y1[:len(x2)] - y1_interp)
        rel_errors.append(error)

    table = Table(title=f"Task {task_label}, Order {order}")

    # Add column headers
    table.add_column("N", justify="center")
    table.add_column("Relative Errors", justify="center")

    n_values = [20, 100, 200, 1000][:len(rel_errors)]
    for i, N in enumerate(n_values):
        errors_str = " ".join(f"{e:.5f}" for e in rel_errors[i])
        table.add_row(f"N_{N}", errors_str)

    console.print(table)

    abs_errors = [np.max(e) for e in rel_errors]

    return abs_errors

steps = [0.1, 0.05, 0.01, 0.005, 0.001]
orders = [2, 4]

# Example function a: y' = x + cos(y), y(1) = 30
f_a = lambda x, y: x + np.cos(y)
abs_errors_a = []
for order in orders:
    abs_err = solve_and_display(f_a, 30, 1, 2, steps, order, "A")
    abs_errors_a.append(abs_err)

# Example function b: y' = x^2 + y^2, y(2) = 1
f_b = lambda x, y: x**2 + y**2
abs_errors_b = []
for order in orders:
    abs_err = solve_and_display(f_b, 1, 1, 2, steps, order, "B")
    abs_errors_b.append(abs_err)

# Plot the Log2 of absolute errors
x_labels = ['N_20', 'N_100', 'N_200', 'N_1000']
for i, abs_errors in enumerate(abs_errors_a):
    plt.plot(x_labels[:len(abs_errors)], np.log2(abs_errors), label=f'Function A, Order {orders[i]}')
for i, abs_errors in enumerate(abs_errors_b):
    plt.plot(x_labels[:len(abs_errors)], np.log2(abs_errors), label=f'Function B, Order {orders[i]}')

plt.xlabel('N')
plt.ylabel('Log2 of Absolute Error')
plt.title('Log2 of Absolute Errors for Both Methods')
plt.legend()
plt.show()