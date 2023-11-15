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
    det = np.linalg.det(matrix)
    return int(det)


def extendedEuclides(a, m):
    if m == 0:
        return (1, 0, a)

    x1, y1, gcd = extendedEuclides(m, a % m)
    x = y1
    y = x1 - (a // m) * y1

    return x, y, gcd


def cofactor(matrix):
    """
    Calculate cofactor matrix of A
    """
    sel_rows = np.ones(matrix.shape[0], dtype=bool)
    sel_columns = np.ones(matrix.shape[1], dtype=bool)
    cofactor = np.zeros_like(matrix)
    sgn_row = 1
    for row in range(matrix.shape[0]):
        # Unselect current row
        sel_rows[row] = False
        sgn_col = 1
        for col in range(matrix.shape[1]):
            # Unselect current column
            sel_columns[col] = False

            subMatrix = matrix[sel_rows][:, sel_columns]
            cofactor[row, col] = sgn_row * sgn_col * (round(np.linalg.det(subMatrix)))

            # Reselect current column
            sel_columns[col] = True
            sgn_col = -sgn_col

        sel_rows[row] = True
        # Reselect current row
        sgn_row = -sgn_row

    return cofactor


def adjugate(matrix):
    return cofactor(matrix).T


def inverse(matrix, m):
    # Find x in module m so that it satisfies that x * det(k) == 1 mod(m).
    # X will be equal to 1/det(k) in mod(m)
    matrixDeterminant = determinant(matrix) % m

    inversedDeterminant = -1
    for i in range(m):
        x = i * matrixDeterminant
        if x % m == 1:
            inversedDeterminant = i
            break

    adjugateMatrix = adjugate(matrix)
    return (inversedDeterminant * adjugateMatrix) % m


def fromString(inputString):
    asciiPadding = ord("A")
    asciiList = [ord(char) - asciiPadding for char in inputString.upper()]

    return np.array(asciiList, dtype=int)
