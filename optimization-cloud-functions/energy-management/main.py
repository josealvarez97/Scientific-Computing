from energy_management import optimize_static_network
from flask import jsonify


def static_energy_network(request):
    request_json = request.get_json()
    
    result = optimize_static_network(request_json)
    
    return jsonify(
        result=result)
    
    
    
    