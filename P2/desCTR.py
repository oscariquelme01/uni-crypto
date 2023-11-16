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

def padding(result):
    if len(result.replace(" ","")) % 64 != 0:
        result += "0"
        return padding(result)
    return result

def fromStr_to_binary(string):
    result = ' '.join(format(ord(c), 'b') for c in string)
    result += " "
    result = padding(result)
    return result

def desCTR():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true") 
    parser.add_argument("-k", required=True, type=str)
    parser.add_argument("-ctr", required=True, type=str)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()
    
    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    inputFile = readInput(args).upper()
    outputFile = open(args.o, 'w') if args.o else sys.stdout
    m = 26
    key = args.k

    inputFileBinary = fromStr_to_binary(inputFile)

    print(inputFileBinary)

def cifrar():

    return 0

def descifrar():

    return 0

if __name__ == "__main__":
    sys.exit(desCTR())
