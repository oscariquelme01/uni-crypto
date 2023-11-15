import numpy as np

""" 
Simple wrapper for working with matrix for our use case. 
"""

def fromPerm(perm):
    matrix = np.zeros((len(perm), len(perm)), dtype=int)

    for i in range(len(perm)):
        matrix[i, int(perm[i])] = 1

    return matrix


def fromFile(path):
    try:
        matrix = np.loadtxt(path, dtype=int)
        return matrix

    except IOError:
        print(f"Error: Could not read the file at {path}")
        return None


def determinant(matrix):
    det = np.linalg.det(matrix)
    return int(det)


def inverse(matrix):
    return np.linalg.inv(matrix)


def fromString(inputString):
    asciiPadding = ord("A")
    asciiList = [ord(char) - asciiPadding for char in inputString.upper()]

    return np.array(asciiList, dtype=int)
