import argparse
import os
from os.path import isfile
import sys


def readInput(args):
    if args.i is None:
        inputString = input("Input string: ")
        return inputString
    else:
        if os.path.isfile(args.i):
            with open(args.i) as f:
                data = f.read(os.stat(args.i).st_size)
                return data


def vigenere():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true")
    parser.add_argument("-k", required=True, type=str)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    k = str(args.k)
    fileo = args.o
    m = 26

    userInput = readInput(args)
    open(fileo, "w")
    if args.C == True:
        print("Cifrando")
        cifrar(userInput, k, m, fileo)

    elif args.D == True:
        print("Descifrando")
        descifrar(userInput, k, m, fileo)

    return 0


def cifrar(filei, k, m, fileo):
    for i in range(len(filei)):
        if filei[i] == " ":
            y = filei[i]
            with open(fileo, "a") as f:
                f.write(y)

        else:
            y = ((ord(filei[i]) - 65) + (ord(k[i % len(k)]) - 65)) % m
            y += 65
            with open(fileo, "a") as f:
                f.write(chr(y))

    return 0


def descifrar(filei, k, m, fileo):
    for i in range(len(filei)):
        if filei[i] == " ":
            y = filei[i]
            with open(fileo, "a") as f:
                f.write(y)

        else:
            y = ((ord(filei[i]) - 65) - (ord(k[i % len(k)]) - 65)) % m
            y += 65
            with open(fileo, "a") as f:
                f.write(chr(y))
    return 0


if __name__ == "__main__":
    sys.exit(vigenere())
