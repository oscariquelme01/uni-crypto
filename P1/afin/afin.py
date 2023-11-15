import argparse
import os
import gmpy2 as gmp
import sys

from re import error


def readInput(args):
    if args.i is None:
        inputString = input("Input string: ")
        return inputString.strip('\n')
    else:
        if os.path.isfile(args.i):
            with open(args.i) as f:
                data = f.read(os.stat(args.i).st_size)
                return data.strip('\n')


def checkPositive(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % value)

    return int(value)


def mcd(a, b):
    while b > 0:
        a, b = b, a % b

    return a


def extendedEuclides(a, m):
    if m == 0:
        return (1, 0, a)

    x1, y1, gcd = extendedEuclides(m, a % m)
    x = y1
    y = x1 - (a // m) * y1

    return x, y, gcd

def getInverse(a, m):
    x, _, gcd = extendedEuclides(a, m)

    return None if gcd != 1 else x % m


def afin():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true") 
    parser.add_argument("-m", required=True, type=checkPositive)
    parser.add_argument("-a", required=True, type=int)
    parser.add_argument("-b", required=True, type=checkPositive)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    a = gmp.mpz(int(args.a))
    b = gmp.mpz(int(args.b))
    m = gmp.mpz(int(args.m))
    outputFile = open(args.o, 'w') if args.o else sys.stdout

    if mcd(a, m) != 1:
        raise error(f"y = ({a}x + {b}) % {m} does not define an inyective function")

    userInput = readInput(args)
    if args.C == True:
        print("Cifrando")
        encrypt(userInput, a, b, m, outputFile)

    elif args.D == True:
        print("Descifrando")
        decrypt(userInput, a, b, m, outputFile)


# a es la constante multiplicativa
# b es la constante a sumar
# m es el tamaño del alfabeto
def encrypt(inputFile, a, b, m, outputFile):
    asciiPadding = ord('A')

    for i in range(len(inputFile)):
        alphabetPostion = ord(inputFile[i]) - asciiPadding

        y = (a * (alphabetPostion) + b) % m
        y += asciiPadding

        outputFile.write(chr(gmp.mpz(y)))

    return 0


# a es la constante multiplicativa
# b es la constante a sumar
# m es el tamaño del alfabeto
def decrypt(inputFile, a, b, m, outputFile):
    asciiPadding = ord('A')

    inversedA = getInverse(a, m)
    for i in range(len(inputFile)):
        alphabetPostion = ord(inputFile[i]) - asciiPadding

        y = ((alphabetPostion - b) * inversedA) % m
        y += asciiPadding

        outputFile.write(chr(gmp.mpz(y)))

    return 0


if __name__ == "__main__":
    sys.exit(afin())
