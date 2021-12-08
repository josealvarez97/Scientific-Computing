'''
References:
Deshmukh, G. (2021). Computational Fluid Dynamics using Python: Modeling Laminar Flow. 
Towards Data Science. 
Retrieved from https://towardsdatascience.com/computational-fluid-dynamics-using-python-modeling-laminar-flow-272dad1ebec
'''
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class FlowVisualizer():
    def __init__(self, nx, ny, x_max, y_max, tmpdir=None):
        #### Simulation inputs
        self.nx=nx
        self.ny=ny
        self.x_max=x_max
        self.y_max=y_max
        
        #Go to the Result directory
        cwdir=os.getcwd()
        self.dir_path= (os.path.join(cwdir,"Result") if tmpdir==None
                          else os.path.join(tmpdir,"Result"))
        # os.chdir(self.dir_path)
        
        
        #Go through files in the directory and store filenames
        filenames=[]
        iterations=[]
        for root,dirs,files in os.walk(self.dir_path):
            for datafile in files:
                if "p-u-v" in datafile:
                    filenames.append(datafile)
                    no_ext_file=datafile.replace(".txt","").strip()
                    iter_no=int(no_ext_file.split("iteration")[-1])
                    iterations.append(iter_no)
        #Discern the final iteration and interval
        initial_iter=np.amin(iterations)            
        final_iter=np.amax(iterations)
        inter=(final_iter - initial_iter)/(len(iterations)-1)
        self.number_of_frames=len(iterations)
        self.sorted_iterations=np.sort(iterations)
        
        #Create blank figure
        self.fig=plt.figure(figsize=(16,8))
        self.ax=plt.axes(xlim=(0,self.x_max),ylim=(0,self.y_max))

        
    def read_datafile(self, iteration):
        #Set filename and path according to given iteration
        filename=f"p-u-v-iteration{iteration}.txt"
        filepath=os.path.join(self.dir_path,filename)
        #Load text file as numpy array
        arr=np.loadtxt(filepath,delimiter=",") # prefer csv.
        rows,cols=arr.shape
        #Define empty arrays for pressure and velocities
        p_p=np.zeros((self.ny,self.nx))
        u_p=np.zeros((self.ny,self.nx))
        v_p=np.zeros((self.ny,self.nx))
        #Organize imported array into variables
        p_arr=arr[:,0]
        u_arr=arr[:,1]
        v_arr=arr[:,2]
        
        #Reshape 1D data into 2D
        p_p=p_arr.reshape((self.ny,self.nx))
        u_p=u_arr.reshape((self.ny,self.nx))
        v_p=v_arr.reshape((self.ny,self.nx))
        
        return p_p,u_p,v_p
        
        
    def make_plot(self,iteration=0):
        
        #Create mesh for X and Y inputs to the figure
        x=np.linspace(0,self.x_max,self.nx)
        y=np.linspace(0,self.y_max,self.ny)
        [X,Y]=np.meshgrid(x,y)
        #Determine indexing for stream plot (10 points only)
        index_cut_x=int(self.nx/10)
        index_cut_y=int(self.ny/10)
        #Create blank figure
        fig=plt.figure(figsize=(16,8))
        ax=plt.axes(xlim=(0,self.x_max),ylim=(0,self.y_max))
        #Create initial contour and stream plot as well as color bar
        p_p,u_p,v_p=self.read_datafile(iteration)
        ax.set_xlim([0,self.x_max])
        ax.set_ylim([0,self.y_max])
        ax.set_xlabel("$x$",fontsize=12)
        ax.set_ylabel("$y$",fontsize=12)
        ax.set_title("Frame No: 0")
        cont=ax.contourf(X,Y,p_p)
        stream=ax.streamplot(X[::index_cut_y,::index_cut_x],Y[::index_cut_y,::index_cut_x],u_p[::index_cut_y,::index_cut_x],v_p[::index_cut_y,::index_cut_x],color="k")
        fig.colorbar(cont)
        fig.tight_layout()
        
        fig.savefig('../from_plot_fisualizer.png', bbox_inches='tight')
        print("Saved from_plot_fisualizer.png")

    def animate(self, i):
        #Print frames left to be added to the animation
        sys.stdout.write("\rFrames remaining: {0:03d}".format(len(self.sorted_iterations)-i))
        sys.stdout.flush()
        #Get iterations in a sequential manner through sorted_iterations
        iteration=self.sorted_iterations[i]
        #Use the read_datafile function to get pressure and velocities
        p_p,u_p,v_p=self.read_datafile(iteration)
        #Clear previous plot and make contour and stream plots for current iteration
        
        # print("iteration i", i)
        # print(type(self.fig))
        
        self.ax.clear()
        self.ax.set_xlim([0,self.x_max])
        self.ax.set_ylim([0,self.y_max])
        self.ax.set_xlabel("$x$",fontsize=12)
        self.ax.set_ylabel("$y$",fontsize=12)
        self.ax.set_title("Frame No: {0}".format(i))
        
        #Create mesh for X and Y inputs to the figure
        x=np.linspace(0,self.x_max,self.nx)
        y=np.linspace(0,self.y_max,self.ny)
        [X,Y]=np.meshgrid(x,y)
        #Determine indexing for stream plot (10 points only)
        index_cut_x=int(self.nx/10)
        index_cut_y=int(self.ny/10)



        cont=self.ax.contourf(X,Y,p_p)
        stream=self.ax.streamplot(X[::index_cut_y,::index_cut_x],\
                             Y[::index_cut_y,::index_cut_x],\
                             u_p[::index_cut_y,::index_cut_x],\
                             v_p[::index_cut_y,::index_cut_x],\
                             color="k")
        return cont,stream
        
        
    def save_animation(self):
        print("######## Making FlowPy Animation ########")
        print("#########################################")
        anim=animation.FuncAnimation(self.fig,self.animate,frames=self.number_of_frames,
                                        interval=50,blit=False)
        movie_path=os.path.join(self.dir_path,"../FluidFlowAnimation.mp4")
        anim.save(r"{0}".format(movie_path))
        print("\nAnimation saved as FluidFlowAnimation.mp4 in Result")