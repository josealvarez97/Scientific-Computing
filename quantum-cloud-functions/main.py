from flask import jsonify
import time
from number_partition import create_problem_for_number_partition, create_simplified_problem_for_number_partition, solve_number_partition
from karmarkar_karp import karmarkar_karp

def cloud_function(request):
    """ Responds to any HTTP request.
    Args: 
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a 
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
         https://cloud.google.com/functions/docs/quickstart-python
    """
    request_json = request.get_json()

    partition_weights = None
    method = None
    if not request_json:
        return jsonify(
            result="Bad request.")


    if 'partition_weights' in request_json:
        partition_weights = request_json['partition_weights']
    if 'method' in request_json:
        method = request_json['method']

    result = None
    formatted_result = None
    if method == 'qubo' or method == None:
        # problem = create_problem_for_number_partition(partition_weights)
        problem = create_simplified_problem_for_number_partition(partition_weights)
        result = solve_number_partition(problem)

    elif method == 'karmarkar_karp':
        result = karmarkar_karp(partition_weights)

    return jsonify(
    result=result)




