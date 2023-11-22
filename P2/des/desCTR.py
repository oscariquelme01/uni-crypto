import argparse
import os
import sys
from re import error
from const import *
from random import randint

def readInput(args):
    if os.path.isfile(args.i):
        with open(args.i) as f:
            data = f.read(os.stat(args.i).st_size)
            return data.strip('\n')
    else:
        return ''

def padding(result):
    if len(result.replace(" ","")) % 64 != 0:
        result += "0"
        return padding(result)
    return result

def stringToBinary(string: str):
    ret = ''
    for c in string:
        #si queremos meter -65 pra trabajar con A=0
        bits = bin(ord(c)).replace('0b', '')
        for i in range(8 - len(bits)): # 8 is the desired length for out bits so we add padding
            bits = '0' + bits
        
        ret += bits

    return ret

def doPermutation(permutation, source):
    ret = ''
    for i in range(len(permutation)):
        ret += source[permutation[i]]

    return ret

def desCTR():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true") 
    parser.add_argument("-k", required=True, type=str)
    parser.add_argument("-ctr", required=True, type=int)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()
    
    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    inputFile = readInput(args).upper()
    outputFile = open(args.o, 'w') if args.o else sys.stdout
    m = 26
    key = args.k.upper()
    if len(key) * 8 != 64:
        print('Invalid key: must be 64 bits')
        return

    text = padding(stringToBinary(inputFile))

    binaryKey = stringToBinary(key)
    reducedKey = doPermutation(PC_1, binaryKey)
    print(reducedKey)

def cifrar():

    return 0

def descifrar():

    return 0

if __name__ == "__main__":
    sys.exit(desCTR())
