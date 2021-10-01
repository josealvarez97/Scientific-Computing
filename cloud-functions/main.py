from flask import jsonify
from math import exp
from trapezoidal import trapezoidal
from midpoint import midpoint

def midpoint_cloud_function(request):
    return cloud_function(request, midpoint)

def trapezoidal_cloud_function(request):
    return cloud_function(request, trapezoidal)

def cloud_function(request, numerical_method):
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

    f = None#lambda t: 3*(t**2)*exp(t**3)
    a = None
    b = None
    n = None

    if request.args and 'f' in request.args:
        exec("f=" + request.args.get('f'), globals())
        # f = locals()['f']
    elif request_json and 'f' in request_json:
        exec("f="+ request_json['f'], globals())
        # f = locals()['f']
    else:
        raise ValueError("Body is invalid, or missing 'f' property")
    f = globals()['f']


    if request.args and 'a' in request.args:
        a = request.args.get('a')
    elif request_json and 'a' in request_json:
        a = request_json['a']
    else:
        raise ValueError("Body is invalid, or missing 'a' property")

    if request.args and 'b' in request.args:
        b = request.args.get('b')
    elif request_json and 'b' in request_json:
        b = request_json['b']
    else:
        raise ValueError("Body is invalid, or missing 'b' property")

    if request.args and 'n' in request.args:
        n = request.args.get('n')
    elif request_json and 'n' in request_json:
        n = request_json['n']
    else:
        raise ValueError("Body is invalid, or missing 'n' property")

    # return str(globals()) + str(f) + str(globals()['f'])
    result = numerical_method(f, a, b, n)

    return jsonify(result=result, test="both")

