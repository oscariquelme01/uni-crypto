import argparse
import os
import sys

from re import error


def readInput(args):
    if args.i is None:
        inputString = input("Input string: ")
        return inputString.strip("\n")
    else:
        if os.path.isfile(args.i):
            with open(args.i) as f:
                data = f.read(os.stat(args.i).st_size)
                return data.strip("\n")


def checkPermutation(value):
    length = len(value)
    for i in range(length):
        permItem = int(i)
        if permItem >= length:
            raise argparse.ArgumentTypeError(
                f"{permItem} is an index and it can't be greater than the length of the permutation"
            )

    return value



def permutations():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true")
    parser.add_argument("-k1", required=True, type=checkPermutation)
    parser.add_argument("-k2", required=True, type=checkPermutation)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    outputFile = open(args.o, "w") if args.o else sys.stdout

    # Args validation
    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    if args.C and args.D:
        parser.error("You can't specify both -D and -C")

    k1 = args.k1
    k2 = args.k2

    userInput = readInput(args)
    if args.C == True:
        print("Cifrando")
        encrypt(userInput, outputFile, k1, k2)

    elif args.D == True:
        print("Descifrando")
        decrypt(userInput, outputFile, k1, k2)


def encrypt(userInput, outputFile, k1, k2):
    # split the array into n chunks
    m = len(k1)
    n = len(k2)
    matrixDimensions = m * n

    # Add padding
    while len(userInput) % matrixDimensions:
        userInput += '@'

    for i in range(0, len(userInput), matrixDimensions):
        matrix = []
        chunk = userInput[i : i + matrixDimensions]

        # fill matrix
        for j in range(n):
            matrix.append([])
            for k in range(m):
                matrix[j].append(chunk[m * j + k])

        # cypher the chunk and write it to outputFile
        cypheredChunk = ''
        for j in range(n):
            colIndex = int(k2[j]) - 1
            for k in range(m):
                rowIndex = int(k1[k]) - 1
                cypheredChunk += matrix[colIndex][rowIndex]

        outputFile.write(cypheredChunk.strip('@'))

def decrypt(userInput, outputFile, k1, k2):
    # split the array into n chunks
    m = len(k1)
    n = len(k2)
    matrixDimensions = m * n

    while len(userInput) % matrixDimensions:
        userInput += '@'

    for i in range(0, len(userInput), matrixDimensions):
        matrix = [[0 for x in range(m)] for y in range(n)] 
        chunk = userInput[i : i + matrixDimensions]

        # fill matrix
        for j in range(n):
            colIndex = int(k2[j]) - 1
            for k in range(m):
                rowIndex = int(k1[k]) - 1
                matrix[colIndex][rowIndex] = chunk[m * j + k]

        # write decrypted message to output file
        for j in range(n):
            for k in range(m):
                if (matrix[j][k] != '@'):
                    outputFile.write(matrix[j][k])


if __name__ == "__main__":
    sys.exit(permutations())
