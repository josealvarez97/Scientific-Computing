# Source(s): 
# Adapted from Programming for Computations by S. Linge & H. Langtangen (2020)
# A Gentle Introduction to Numerical Simulations with Python 

def midpoint(f, a, b, n):
    h = float(b-a)/n
    result = 0
    for i in range(n):
        result += f((a + h/2.0) + i*h)
    result *= h
    return result