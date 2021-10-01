# Source(s): 
# Adapted from Programming for Computations by S. Linge & H. Langtangen (2020)
# A Gentle Introduction to Numerical Simulations with Python 

from trapezoidal import trapezoidal

def test_trapezoidal_one_exact_result():
    """Compare one hand-computed result."""
    from math import exp
    v = lambda t: 3*(t**2)*exp(t**3)
    n = 2
    computed = trapezoidal(v, 0, 1, n)
    expected = 2.463642041244344
    error = abs(expected - computed)
    tol = 1E-14
    success = error < tol
    msg = 'error=%g > tol=%g' % (error, tol)
    assert success, msg

def test_trapezoidal_linear():
    """Check that linear functions are integrated exactly."""
    f = lambda x: 6*x - 4
    F = lambda x: 3*x**2 - 4*x # Anti-derivative
    a = 1.2; b = 4.4
    expected = F(b) - F(a)
    tol = 1E-14
    for n in 2, 20, 21:
        computed = trapezoidal(f, a, b, n)
        error = abs(expected - computed)
        success = error < tol # Should be the exact same but we need a tolerance because computers are not perfect
        msg = 'n=%d, err=%g' % (n, error)
        assert success, msg


test_trapezoidal_one_exact_result()
test_trapezoidal_linear()