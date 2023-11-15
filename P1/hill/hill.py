import argparse
import os
import sys
import matrix

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


def checkPositive(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % value)

    return int(value)


def mcd(a, b):
    while b > 0:
        a, b = b, a % b

    return a


def hill():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true")
    parser.add_argument("-m", required=True, type=checkPositive)
    parser.add_argument("-n", required=True, type=checkPositive)
    parser.add_argument("-k", required=True, type=str)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    outputFile = open(args.o, "w") if args.o else sys.stdout
    keys = matrix.fromFile(args.k)
    m = int(args.m)
    n = int(args.n)

    # Args validation
    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    if args.C and args.D:
        parser.error("You can't specify both -D and -C")

    if keys is None:
        raise error(
            f"Failed to read matrix from the path provided by -k argument {args.k}"
        )

    if len(keys[0]) != n:
        raise error(
            f"Length mismatch! Matrix defined in {args.k} should be of length {n}x{n}"
        )

    if mcd(matrix.determinant(keys), m) != 1:
        raise error(
            f"The matrix defined in {args.k} is not inyective and decrypting is not possible"
        )

    userInput = readInput(args)
    if args.C == True:
        print("Cifrando")
        encrypt(userInput, outputFile, keys, m, n)

    elif args.D == True:
        print("Descifrando")
        decrypt(userInput, outputFile, keys, m, n)


def encrypt(userInput, outputFile, keysMatrix, m, n):
    asciiPadding = ord("A")
    # add padding so that the array is dividible in chunks of n size without leftovers
    while len(userInput) % n != 0:
        userInput += "@"

    inputMatrix = matrix.fromString(userInput)
    # split the array into n chunks
    for i in range(0, len(inputMatrix), n):
        chunk = inputMatrix[i : i + n]

        cypheredChunk = keysMatrix.dot(chunk) % m
        for cypheredCharacter in cypheredChunk:
            outputFile.write(chr(cypheredCharacter + asciiPadding))


def decrypt(userInput, outputFile, keysMatrix, m, n):
    asciiPadding = ord("A")
    # add padding so that the array is dividible in chunks of n size without leftovers
    while len(userInput) % n != 0:
        userInput += "@"

    inputMatrix = matrix.fromString(userInput)
    inversedMatrix = matrix.inverse(keysMatrix, m)

    # split the array into n chunks
    for i in range(0, len(inputMatrix), n):
        chunk = inputMatrix[i : i + n]
        
        decryptedChunk = inversedMatrix.dot(chunk) % m
        for decryptedCharacter in decryptedChunk:
            outputFile.write(chr(round(decryptedCharacter) + asciiPadding))


if __name__ == "__main__":
    sys.exit(hill())
