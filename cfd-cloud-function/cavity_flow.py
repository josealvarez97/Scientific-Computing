
'''
Sections of this code were written with the help of the following references:

Owkes, M. (2020). A guide to writing your first CFD solver. Retrieved from https://www.montana.edu/mowkes/research/source-codes/GuideToCFD_2020_02_28_v2.pdf

Barba, Lorena A., and Forsyth, Gilbert F. (2018). CFD Python: the 12 steps to Navier-Stokes equations. Journal of Open Source Education, 1(9), 21, https://doi.org/10.21105/jose.00021

Alvarez, J., and Nobe, M. (2021). The Ultimate Guide to Write Your First CFD Solver. Retrieved from https://colab.research.google.com/github/josealvarez97/The-Ultimate-Guide-to-Write-Your-First-CFD-Solver/blob/main/The_Ultimate_Guide_to_Write_Your_First_CFD_Solver.ipynb

Deshmukh, G. (2021). Computational Fluid Dynamics using Python: Modeling Laminar Flow. Towards Data Science. Retrieved from https://towardsdatascience.com/computational-fluid-dynamics-using-python-modeling-laminar-flow-272dad1ebec

'''

# Import your favorite libraries
import numpy as np
from enum import Enum
import os
from flow_visualizer import FlowVisualizer

class BoundaryPosition(Enum):
  TOP = 0
  BOTTOM = 1
  RIGHT = 2
  LEFT = 3

class BoundaryType(Enum):
  DIRICHLET = 0
  NEUMANN = 1

class CavityFlow():

  def __init__(self, 
               x_min = 0, x_max = 2, nx = 41, 
               y_min = 0, y_max = 2, ny = 41, 
               density = 1, viscosity = .1, dt=.001,
               tmpdir=None):
    # Continuous domain
    self.x_min = x_min
    self.x_max = x_max
    self.nx = nx
    self.dx = (x_max - x_min) / (nx-1)

    self.y_min = y_min
    self.y_max = y_max
    self.ny = ny
    self.dy = (y_max - y_min) / (ny-1)

    # Global variables
    self.rho = density # density
    self.nu = viscosity # viscosity
    self.dt = dt


    # Data structures
    # Velocities
    self.u = np.zeros((ny, nx))
    self.v = np.zeros((ny, nx))
    # Pressure
    self.p = np.zeros((ny,nx))

    self.tmpdir = tmpdir
    #Get path to the Result directory
    cwdir=os.getcwd()
    self.dir_path=(os.path.join(cwdir,"Result") 
                      if self.tmpdir==None
                      else 
                      os.path.join(self.tmpdir,"Result"))



  def dirichlet_boundary(self, f, function_value, position):
    if position == BoundaryPosition.TOP:
      f[-1,:] = function_value
    elif position == BoundaryPosition.BOTTOM:
      f[0,:] = function_value
    elif position == BoundaryPosition.RIGHT:
      f[:,-1] = function_value
    elif position == BoundaryPosition.LEFT:
      f[:,0] = function_value
    else:
      raise Exception("Sorry, boundary argument is not valid.")
    
    return f

  # def dirichlet_boundaries(f, top_value, bottom_value, 
  #                        right_value, left_value):
  #   f[-1,:] = top_value
  #   f[0,:] = bottom_value
  #   f[:,-1] = right_value
  #   f[:,0] = left_value
    
  #   return f

  def neumann_boundary(self, f, function_rate, position):
    if position == BoundaryPosition.TOP:
      f[-1,:] = function_rate*self.dy + f[-2,:]
    elif position == BoundaryPosition.BOTTOM:
      f[1,:] = function_rate*self.dy + f[0,:]
    elif position == BoundaryPosition.RIGHT:
      f[:,-1] = function_rate*self.dx + f[:,-2]
    elif position == BoundaryPosition.LEFT:
      f[:,1] = function_rate*self.dx + f[:,0]
    else:
      raise Exception("Sorry, position argument is not valid.")
    
    return f

  # def neumann_boundaries(f, top_rate, bottom_rate,
  #                      right_rate, left_rate):
    
  #   f[-1,:] = top_rate*self.dy + f[-2,:] 
  #   f[1,:] = bottom_rate*self.dy + f[0,:]
  #   f[:,-1] = right_rate*self.dx + f[:,-2]
  #   f[:,1] = left_rate*self.dx + f[:,0]

  #   return f


  def boundary(self, f, value, boundary_type, boundary_position):
    if boundary_type == BoundaryType.DIRICHLET:
      return self.dirichlet_boundary(f=f, function_value = value,
                                     position = boundary_position) 
    elif boundary_type == BoundaryType.NEUMANN:
      return self.neumann_boundary(f=f, function_rate = value,
                                   position = boundary_position)
    else:
      raise Exception("Sorry, boudnary_type argument is not valid.")

  def f_boundaries(self, f,
                      top=(0, BoundaryType.DIRICHLET), 
                      bottom=(0,BoundaryType.DIRICHLET), 
                      right=(0,BoundaryType.DIRICHLET),
                      left=(0,BoundaryType.DIRICHLET)):
    
    f = self.boundary(f=f, value=top[0], boundary_type=top[1], 
                      boundary_position=BoundaryPosition.TOP)
    f = self.boundary(f=f, value=bottom[0], boundary_type=bottom[1], 
                      boundary_position=BoundaryPosition.BOTTOM)
    f = self.boundary(f=f, value=right[0], boundary_type=right[1], 
                      boundary_position=BoundaryPosition.RIGHT)
    f = self.boundary(f=f, value=left[0], boundary_type=left[1], 
                      boundary_position=BoundaryPosition.LEFT)

    return f

  def set_u_boundaries(self, 
                      top=(1, BoundaryType.DIRICHLET), 
                      bottom=(0,BoundaryType.DIRICHLET), 
                      right=(0,BoundaryType.DIRICHLET),
                      left=(0,BoundaryType.DIRICHLET)):
    
    self.u = self.f_boundaries(self.u, top, bottom, right, left)

  def set_v_boundaries(self, 
                      top=(0, BoundaryType.DIRICHLET), 
                      bottom=(0,BoundaryType.DIRICHLET), 
                      right=(0,BoundaryType.DIRICHLET),
                      left=(0,BoundaryType.DIRICHLET)):
    
    self.v = self.f_boundaries(self.v, top, bottom, right, left)    

  def set_pressure_boundaries(self, 
                            top=(0, BoundaryType.DIRICHLET),
                            bottom=(0,BoundaryType.NEUMANN), 
                            right=(0,BoundaryType.NEUMANN), 
                            left=(0,BoundaryType.NEUMANN)):
      self.p = self.f_boundaries(self.p, top, bottom, right, left)  
      # Set pressure configuration, somehow

  def reset_pressure_boundaries(self):
    # Access pressure configuration and reset, somehow
    print("Warning: reset_pressure_boundaries not implemented.")

  def diff_1st_x(self, f):
    return (f[1:-1, 2:] - f[1:-1,0:-2])/(2*self.dx)

  def diff_1st_y(self, f):
    return (f[2:, 1:-1] - f[0:-2,1:-1])/(2*self.dy)

  # Discretization
  def forward_diff_x(self, f):
    return (f[1:-1,2:] - f[1:-1,1:-1])/self.dx

  def forward_diff_y(self, f):
    return (f[2:,1:-1] - f[1:-1,1:-1])/self.dy

  def backward_diff_x(self, f):
    return (f[1:-1,1:-1] - f[1:-1,0:-2])/self.dx

  def backward_diff_y(self, f):
    return (f[1:-1,1:-1] - f[0:-2,1:-1])/self.dy

  def diff_2nd_x(self, f):
    return (
        # f(i-1,j) + 2*f(i,j) + f(i+1,j) 
        (f[1:-1,0:-2] - 2*f[1:-1,1:-1] + f[1:-1,2:])
        /self.dx**2
        ) 
    
  def diff_2nd_y(self, f):
    return (
        # f(i,j-1) + 2*f(i,j) + f(i,j+1) 
        (f[0:-2,1:-1] - 2*f[1:-1,1:-1] + f[2:,1:-1])
        /self.dy**2
        )

  def laplacian(self, f):
    return self.diff_2nd_x(f) + self.diff_2nd_y(f)
    
  def vel_without_pressure(self, un, vn):
    u_without_pressure = un.copy()
    v_without_pressure = vn.copy()

    u_without_pressure[1:-1,1:-1] = ( -1*(un[1:-1,1:-1]*self.forward_diff_x(un) + 
                                       vn[1:-1,1:-1]*self.forward_diff_y(un)) 
                                      + self.nu*self.laplacian(un)
                                     ) * self.dt + un[1:-1,1:-1]

    v_without_pressure[1:-1,1:-1] = ( -1*(un[1:-1,1:-1]*self.forward_diff_x(vn) + 
                                          vn[1:-1,1:-1]*self.forward_diff_y(vn))
                                      + self.nu*self.laplacian(vn)
                                      ) * self.dt + vn[1:-1,1:-1]

    return u_without_pressure, v_without_pressure


  def get_R(self, u_without_pressure, v_without_pressure):
    R = np.zeros((self.ny,self.nx))
    
    divergence_vel_without_pressure = (
        self.forward_diff_x(u_without_pressure) + 
        self.forward_diff_y(v_without_pressure)
    )
    R[1:-1,1:-1] = (self.rho/self.dt) * divergence_vel_without_pressure

    return R


  def solve_pressure_poisson(self, R):
    # Δ𝑦2(𝑝𝑛+1(𝑖−1,𝑗)+𝑝𝑛+1(𝑖+1,𝑗))
    term1 = self.dy**2 * (self.p[1:-1,0:-2] + self.p[1:-1,2:])
    # Δ𝑥2(𝑝𝑛+1(𝑖−1,𝑗)+𝑝𝑛+1(𝑖+1,𝑗))
    term2 = self.dx**2 * (self.p[0:-2,1:-1] + self.p[2:,1:-1])
    # −R𝑛(𝑖,𝑗)Δ𝑥2Δ𝑦2
    term3 = -1 * R[1:-1,1:-1] * (self.dx**2 * self.dy**2)

    self.p[1:-1,1:-1] =  (term1 + term2 + term3) / (2*(self.dy**2 + self.dx**2))
    self.reset_pressure_boundaries()


  def update_velocity(self, u_without_pressure, v_without_pressure):
    self.u[1:-1,1:-1] = (-self.dt/self.rho) * self.diff_1st_x(self.p) + u_without_pressure[1:-1,1:-1]
    self.v[1:-1,1:-1] = (-self.dt/self.rho) * self.diff_1st_y(self.p) + v_without_pressure[1:-1,1:-1]

  def simulate_cavity_flow(self, nt):
    self.make_result_directory()
    for n in range(nt):
      u_without_pressure, v_without_pressure = self.vel_without_pressure(un=self.u,
                                                                         vn=self.v)
      R = self.get_R(u_without_pressure, v_without_pressure)
      self.solve_pressure_poisson(R)
      self.update_velocity(u_without_pressure, v_without_pressure)
      
      self.u[1:-1, 1:-1]
      self.v[1:-1, 1:-1]
      
      self.write_to_file(iteration=n)
      
      

    print("Simulation finished.")
    
    
  def make_result_directory(self, wipe=True):
      print("make result directory")
      #If directory does not exist, make it
      if not os.path.isdir(self.dir_path):
          print("make directory, none exists")
          os.makedirs(self.dir_path,exist_ok=True)
      else:
          print("wipe everything in existing directory")
          #If wipe is True, remove files present in the directory
          if wipe:
              # os.chdir(self.dir_path)
              filelist=os.listdir(self.dir_path)
              print(filelist)
              for file in filelist:
                  os.remove(os.path.join(self.dir_path,file))
      print("successfully made directory")
      
  def write_to_file(self, iteration,interval=5):
      if(iteration%interval==0):
          filename=f"p-u-v-iteration{iteration}.txt"
          path=os.path.join(self.dir_path,filename)
          with open(path,"w") as file:
              for i in range(self.nx): # I question doing it from 1,-1
                  for j in range(self.ny):
                      file.write(f"{self.p[i,j]},{self.u[i,j]},{self.v[i,j]}\n")
    
def application():
    cfd_solver = CavityFlow(tmpdir="./sample_data")
    cfd_solver.set_u_boundaries()
    cfd_solver.set_v_boundaries()
    cfd_solver.set_pressure_boundaries()

    cfd_solver.simulate_cavity_flow(nt=100)
    
    import numpy as np
    from matplotlib import pyplot as plt, cm

    
    x = np.linspace(cfd_solver.x_min, cfd_solver.x_max, cfd_solver.nx)
    y = np.linspace(cfd_solver.x_min, cfd_solver.x_max, cfd_solver.nx)
    
    X,Y = np.meshgrid(x,y)
    
    fig = plt.figure(figsize=(11,7), dpi=100)
    # plotting the pressure field as a contour
    plt.contourf(X, Y, cfd_solver.p, alpha=0.5, cmap=cm.viridis)
    plt.colorbar()
    # plotting the pressure field outlines
    plt.contour(X, Y, cfd_solver.p, cmap=cm.viridis)
    # plotting velocity field
    plt.quiver(X[::2, ::2], Y[::2, ::2], cfd_solver.u[::2, ::2], cfd_solver.v[::2, ::2])
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # /tmp/cavity_flow.png
    plt.savefig('cavity_flow_quiver_plot.png', bbox_inches='tight')
    print("Wrote cavity_flow_quiver_plot.png successfullly.")
    
    fig = plt.figure(figsize=(11, 7), dpi=100)
    plt.contourf(X, Y, cfd_solver.p, alpha=0.5, cmap=cm.viridis)
    plt.colorbar()
    plt.contour(X, Y, cfd_solver.p, cmap=cm.viridis)
    plt.streamplot(X, Y, cfd_solver.u, cfd_solver.v)
    plt.xlabel('X')
    plt.ylabel('Y');
    plt.savefig('cavity_flow_stream_plot.png', bbox_inches='tight')
    print("Wrote cavity_flow_stream_plot.png successfullly.")


    flow_visualizer = FlowVisualizer(nx=cfd_solver.nx,
                                      ny=cfd_solver.ny,
                                      x_max=cfd_solver.x_max,
                                      y_max=cfd_solver.y_max,
                                      tmpdir="./sample_data")
    # flow_visualizer.make_plot(iteration=90)  
    
    flow_visualizer.save_animation()
    
    

if __name__ == '__main__':
    application()