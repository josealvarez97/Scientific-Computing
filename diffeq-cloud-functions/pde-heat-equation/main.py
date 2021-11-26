from flask import send_file
from heat_equation import HeatEquationSolver
from zipfile import ZipFile
import os
from os.path import basename
from io import BytesIO

def heat_equation(request):
    # Run simulation
    solver = HeatEquationSolver(save_plots=True)
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
