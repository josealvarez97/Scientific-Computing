'''
Reference sources:
Recktenwald, G. W. (2004). Finite-difference approximations to the heat equation. 
Mechanical Engineering, 10(01).
'''
from math import *
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('dark_background')
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

class HeatEquationSolver:

  def __init__(self, Nx=60, x_max=50, Mt=100, t_max=10, 
               f_0=lambda x: sin(x) + x**(1/2),
               alpha=1, heat_x_0=None, heat_x_max=None,
               save_plots=False):
    self.N = Nx
    self.x_max = x_max
    self.dx = self.x_max/(self.N-1)
    self.x_i = lambda i: self.dx*i 

    self.M = Mt
    self.t_max = t_max
    self.dt = self.t_max/(self.M-1)
    self.t_m = lambda m: self.dt*m

    # Initial condition (t=0)
    self.f_0 = f_0

    self.alpha = alpha

    self.heat_x_0 = heat_x_0
    self.heat_x_max = heat_x_max
    if self.heat_x_0 == None: self.heat_x_0 = self.f_0(0)
    if self.heat_x_max == None: self.heat_x_max = self.f_0(self.x_max)

    self.save_plots = save_plots

  def condition(self, x_i, t_m):
    # "Constant" boundary conditions
    if x_i == 0:
      return self.heat_x_0 
    
    if x_i == self.x_max:
      return self.heat_x_max
    
    # Enforce condition (t=0)
    if t_m == 0:
      return self.f_0(x_i)

    return 0

  def get_solution(self):
    u = [[self.condition(self.x_i(i), self.t_m(m)) for i in range(self.N)] 
         for m in range(self.M)]

    # Computational improvement, equation 17 in Recktenwald (2004)
    r = (self.alpha*self.dt)/(self.dx**2)
    r2 = 1 - 2*r

    # Forward Time, Centered Space (FTCS) Solution 
    for m in range(1,self.M): # Exclude initial condition
      for i in range(1, self.N-1): # Exclude boundaries
        u[m][i] = r*u[m-1][i-1] + r2*u[m-1][i] + r*u[m-1][i+1]

    return u

  def plot(self, heat_equation_solution, time_m, show=True):
    x_values = [self.x_i(i) for i in range(self.N)]
    u_values = heat_equation_solution[time_m]
    plt.plot(x_values, u_values,
             label=f"$t$ = {round(self.t_m(time_m),2)}")
    plt.legend(fontsize='large')
    plt.xlabel("$x$", fontsize=20)
    plt.ylabel("Heat", fontsize=20)
    if show: self.show()

  def show(self):
    if self.save_plots:
      print("Save fig")
      plt.savefig('/tmp/heat_equation.png', bbox_inches='tight',
                  dpi=300)
      print("Fig saved successfully.")
    else:
      plt.show()

  def plot_stacked(self, u_solution):
    plt.figure(figsize=(8,4))
    m_times = np.linspace(0,self.M-1,5).astype(int)
    # print(m_times)
    for m in np.linspace(0,self.M-1,5).astype(int):
      is_last = m == self.M-1
      self.plot(u_solution, time_m=m, show=is_last)
      
      
def test_1():
    solver = HeatEquationSolver(save_plots=True)
    
    u_solution = solver.get_solution()
    
    # solver.plot(u_solution, time_m=10)
    solver.plot_stacked(u_solution)
    
def test_2():
    L = 1
    f_0 = lambda x: sin(pi*x/L)
    phi_0 = phi_L = 0
    alpha=0.1
    solver = HeatEquationSolver(f_0=f_0, 
                                Nx=20, x_max=1, 
                                heat_x_0=phi_0,
                                heat_x_max=phi_L,
                                Mt=20, t_max=1,
                                alpha=0.1,
                                save_plots=True)
    
    u_solution = solver.get_solution()
    
    solver.plot_stacked(u_solution)

    
if __name__ == '__main__':
    test_2()