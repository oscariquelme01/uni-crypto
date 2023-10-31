import numpy as np
""" 
Simple wrapper for working with matrix for our use case. 
"""

def fromFile(path):
    try:
        matrix = np.loadtxt(path, dtype=int)
        return matrix

    except IOError:
        print(f"Error: Could not read the file at {path}")
        return None

def determinant(matrix):
    try:
        det = np.linalg.det(matrix)
        return round(det)

    except Exception as e:
        print(f"Error: {e}")
        return None

def inverse(matrix):
    try:
        inverse = np.linalg.inv(matrix)
        return inverse

    except Exception as e:
        print(f"Error: {e}")
        return None
