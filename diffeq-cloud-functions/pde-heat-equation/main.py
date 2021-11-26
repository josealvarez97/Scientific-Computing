from flask import send_file
from heat_equation import HeatEquationSolver
from zipfile import ZipFile
import os
from os.path import basename
from io import BytesIO

from math import *

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

def parse_function_parameter(request, param):
    print("parse_function_parameter")
    request_json = request.get_json()
    if request.args and param in request.args:
        exec(param + "=" + request.args.get(param), globals())
        # f = locals()['f']
    elif request_json and param in request_json:
        exec(param + "="+ request_json[param], globals())
        # f = locals()['f']
    else:
        raise ValueError(f"Body is invalid, or missing '{param}' property")
    print("success with parse_function_parameter")
    return globals()[param]
    

def heat_equation(request):
    # Parse parameters
    request_json = request.get_json()
    
    heat_x_0 = parse_parameter(request, 'heat_x_0')
    heat_x_max = parse_parameter(request, 'heat_x_max')
    alpha = parse_parameter(request, 'alpha')
    Nx = parse_parameter(request, 'Nx')
    x_max = parse_parameter(request, 'x_max')
    Mt = parse_parameter(request, 'Mt')
    t_max = parse_parameter(request, 't_max')
    f_0 = parse_function_parameter(request, 'f_0')
    
    
    # L = 1
    # f_0 = lambda x: sin(pi*x/L)
    # phi_0 = phi_L = 0
    # alpha=0.1
    
    
    # Run simulation
    solver = HeatEquationSolver(f_0=f_0, 
                                heat_x_0=heat_x_0,
                                heat_x_max=heat_x_max,
                                alpha=alpha,
                                Nx=Nx, x_max=x_max, 
                                Mt=Mt, t_max=t_max,
                                save_plots=True)    
    u_solution = solver.get_solution()
    solver.plot_stacked(u_solution)
    
    # Create a ZipFile object
    memory_file = BytesIO()
    with ZipFile(memory_file, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk("/tmp/"):
            for filename in filenames:
                # Create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))
                
    print("Wrote zip file with results successfully.")
    memory_file.seek(0)
    print("about to send memory_file")
    return send_file(memory_file, attachment_filename='heat_equation_results.zip', as_attachment=True)
