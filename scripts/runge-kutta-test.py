import os
from math import cos
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def runge_kutta(f, y0, x0, x_end, h):
    steps = int((x_end - x0) / h)
    x = x0
    y = y0

    console = Console()

    table = Table(title="Runge-Kutta Method")

    table.add_column("Step", justify="right", style="cyan", no_wrap=True)
    table.add_column("x", justify="right", style="green")
    table.add_column("y", justify="right", style="magenta")

    with Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Proceeding Runge-Kutta algorithm...", total=steps)

        for i in range(steps):
            k1 = h * f(x, y)
            k2 = h * f(x + h / 2.0, y + k1 / 2.0)
            k3 = h * f(x + h / 2.0, y + k2 / 2.0)
            k4 = h * f(x + h, y + k3)

            y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
            x += h

            # Clear console
            clear_console()

            # Print the equation again
            console.print("Solving the differential equation: y' = x + cos(y)")

            # Add row to the table
            table.add_row(str(i+1), f"{x:.5f}", f"{y:.5f}")
            console.print(table)

            # Update progress bar
            progress.update(task, advance=1)

    return y

def func(x, y):
    return x + cos(y)

# Initial conditions
x0 = 1
y0 = 30
x_end = 2
h = 0.1

runge_kutta(func, y0, x0, x_end, h)
