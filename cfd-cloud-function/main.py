from flask import send_file
from cavity_flow import CavityFlow, BoundaryType
from zipfile import ZipFile
import os
from os.path import basename
from io import BytesIO
from flow_visualizer import FlowVisualizer
import shutil

def parse_parameter(request, param):
    request_json = request.get_json()
    print("param", param)
    print("request json", request_json)
    if request.args and param in request.args:
        return request.arg.get(param)
    elif request_json and param in request_json:
        return request_json[param]
    else:
        raise ValueError(f"Body is invalid, or missing '{param}' property")
        

def cavity_flow(request):
    tmp = "/tmp/cavity_flow_temp"
    print("make temp directory")
      #If directory does not exist, make it
    if not os.path.isdir(tmp):
        print("make directory, none exists")
        os.makedirs(tmp,exist_ok=True)
    else:
        print("wipe everything in existing directory")
        #If wipe is True, remove files present in the directory
        # os.chdir(self.dir_path)
        filelist=os.listdir(tmp)
        print(filelist)
        for file in filelist:
            os.remove(os.path.join(tmp,file))
    print("successfully made temp directory")
    
    nt = parse_parameter(request, 'nt')
    viscosity = parse_parameter(request, 'viscosity')
    density = parse_parameter(request, 'density')
    u_top = parse_parameter(request, 'u_top')
    
    cfd_solver = CavityFlow(density=density,
                            viscosity=viscosity, tmpdir=tmp)

    cfd_solver.set_u_boundaries(top=(u_top,BoundaryType.DIRICHLET))
    cfd_solver.set_v_boundaries()
    cfd_solver.set_pressure_boundaries()

    cfd_solver.simulate_cavity_flow(nt=nt)
    
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
    
    plt.savefig(f'{tmp}/cavity_flow.png', bbox_inches='tight')
    print("Wrote cavity_flow.png successfullly.")
    
    flow_visualizer = FlowVisualizer(nx=cfd_solver.nx,
                                      ny=cfd_solver.ny,
                                      x_max=cfd_solver.x_max,
                                      y_max=cfd_solver.y_max,
                                      tmpdir=tmp)
    # flow_visualizer.make_plot(iteration=90)  
    
    flow_visualizer.save_animation()
    
    # Zip result folder
    shutil.make_archive(f"{tmp}/Result", 'zip', f"{tmp}/Result")
    shutil.rmtree(f"{tmp}/Result")# I should probably separate visualization results from results I plan to zip
    # Cleaning is not a bad idea, but I cloud probably do that after sending the zip file
    
    zipfile_path = shutil.make_archive("/tmp/resultzip", 'zip', tmp)
    print("Successfully wrote zip with shutil")
    
    # https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
    # create a ZipFile object
    # memory_file = BytesIO()
    # with ZipFile(memory_file, 'w') as zipObj:
    #   # Iterate over all the files in directory
    #   for folderName, subfolders, filenames in os.walk("/tmp/"):
    #       for filename in filenames:
    #           #create complete filepath of file in directory
    #           filePath = os.path.join(folderName, filename)
    #           # Add file to zip
    #           zipObj.write(filePath, basename(filePath))

    # print("Wrote zip file with results successfullly.")
    # memory_file.seek(0)
    # print("about to send memory_file")
    print("about to send zip_file")
    # https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework
    return send_file(zipfile_path, attachment_filename='cavity_flow_results.zip', as_attachment=True)