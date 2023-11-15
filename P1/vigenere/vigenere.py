import argparse
import os
from os.path import isfile
import sys


def readInput(args):
    if args.i is None:
        inputString = input("Input string: ")
        return inputString.strip('\n')
    else:
        if os.path.isfile(args.i):
            with open(args.i) as f:
                data = f.read(os.stat(args.i).st_size)
                return data.strip('\n')


def vigenere():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true")
    parser.add_argument("-k", required=True, type=str)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    outputFile = open(args.o, 'w') if args.o else sys.stdout

    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    k = str(args.k)
    m = 26

    userInput = readInput(args)
    if args.C == True:
        print("Cifrando")
        encrypt(userInput, k, m, outputFile)

    elif args.D == True:
        print("Descifrando")
        decrypt(userInput, k, m, outputFile)

    return 0


def encrypt(inputFile, k, m, outputFile):
    asciiPadding = ord("A")

    for i in range(len(inputFile)):
        symbolValue = ord(inputFile[i]) - asciiPadding
        keyValue = ord(k[i % len(k)]) - asciiPadding

        y = (symbolValue + keyValue) % m
        y += asciiPadding

        outputFile.write(chr(y))


def decrypt(inputFile, k, m, outputFile):
    asciiPadding = ord("A")

    for i in range(len(inputFile)):
        symbolValue = ord(inputFile[i]) - asciiPadding
        keyValue = ord(k[i % len(k)]) - asciiPadding

        y = (symbolValue - keyValue) % m
        y += asciiPadding

        outputFile.write(chr(y))


if __name__ == "__main__":
    sys.exit(vigenere())
