import argparse
import os
import sys
import matrix
import numpy as np

from re import error


def generatePerm(n):
    perm = list(range(n))
    np.random.shuffle(perm)

    print(perm)
    return perm


def generatePermFromString(string):
    perm = []
    for num in string.split():
        perm.append(int(num))

    return perm

def writePermToFile(path, perm):
    with open(path, "w") as f:
        for i in range(len(perm)):
            f.write(str(perm[i]) + " ")


def readPermFromFile(path):
    with open(path, "r") as f:
        perm = []
        rawPerm = f.read()
        for i in rawPerm.split():
            perm.append(i)

        return perm


def readInput(args):
    if args.i is None:
        inputString = input("Input string: ")
        return inputString.strip("\n")
    else:
        if os.path.isfile(args.i):
            with open(args.i) as f:
                data = f.read(os.stat(args.i).st_size)
                return data.strip("\n")


def checkPositive(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % value)

    return int(value)


def mcd(a, b):
    while b > 0:
        a, b = b, a % b

    return a


def transposition():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true")
    parser.add_argument("-n", required=False, type=checkPositive)
    parser.add_argument("-p", required=False, type=str)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    outputFile = open(args.o, "w") if args.o else sys.stdout

    # Args validation
    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    if args.C and args.D:
        parser.error("You can't specify both -D and -C")

    if not args.p and not args.n:
        parser.error("eou must specify either -p or -n")

    if args.p and args.n:
        parser.error("You can't specify both -p and -n")

    # Generate perm for cyphering
    if args.n and args.C:
        n = int(args.n)
        perm = generatePerm(n)
        writePermToFile("perm.dat", perm)

    # Read perm for decyphering
    elif args.n and args.D:
        n = int(args.n)
        perm = readPermFromFile('perm.dat')

    # Generate perm from argument
    else:
        perm = generatePermFromString(args.p)
        n = len(perm)

    userInput = readInput(args)
    if args.C == True:
        print("Cifrando")
        encrypt(userInput, outputFile, perm)

    elif args.D == True:
        print("Descifrando")
        decrypt(userInput, outputFile, perm)


def encrypt(userInput, outputFile, perm):
    asciiPadding = ord("A")
    keysMatrix = matrix.fromPerm(perm)
    inputMatrix = matrix.fromString(userInput)
    n = keysMatrix.shape[0]

    # add padding so that the array is dividible in chunks of n size without leftovers
    while len(userInput) % n != 0:
        userInput += "@"

    # split the array into n chunks
    for i in range(0, len(inputMatrix), n):
        chunk = inputMatrix[i : i + n]

        cypheredChunk = keysMatrix.dot(chunk)
        for cypheredCharacter in cypheredChunk:
            outputFile.write(chr(cypheredCharacter + asciiPadding))


def decrypt(userInput, outputFile, perm):
    asciiPadding = ord("A")
    keysMatrix = matrix.fromPerm(perm)
    inputMatrix = matrix.fromString(userInput)
    n = keysMatrix.shape[0]

    # add padding so that the array is dividible in chunks of n size without leftovers
    while len(userInput) % n != 0:
        userInput += "@"

    inversedMatrix = matrix.inverse(keysMatrix)

    # split the array into n chunks
    for i in range(0, len(inputMatrix), n):
        chunk = inputMatrix[i : i + n]

        decryptedChunk = inversedMatrix.dot(chunk)
        for decryptedCharacter in decryptedChunk:
            outputFile.write(chr(round(decryptedCharacter) + asciiPadding))


if __name__ == "__main__":
    sys.exit(transposition())
