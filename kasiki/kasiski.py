import argparse
import os
import gmpy2 as gmp
from os.path import isfile
import sys

from re import error

def readInput(args):
    if args.i is None:
        inputString = input('Input string: ')
        return inputString
    else:
        if os.path.isfile(args.i):
            with open(args.i) as f:
                data = f.read(os.stat(args.i).st_size)
                return data

def checkPositive(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError('%s is not a positive integer' % value)

    return int(value)

def mcd(a,b):
    while(b > 0):
        a, b = b, a % b

    return a

def search(aux, filei,ng,pos,dic: dict):
    for i in range(len(filei)):
        if aux == filei[i:i+ng]:
            if i != pos:
                if aux not in dic.keys():
                    dic[aux] = list()
                    dic[aux].append(pos)
                else:
                    if pos not in dic[aux]:
                        dic[aux].append(pos)

    return 0

def kasiski():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=False, type=checkPositive)
    parser.add_argument('-i', required=False, type=str)
    parser.add_argument('-o', required=False, type=str)

    args = parser.parse_args()

    dic = {}

    ng = int(args.l)
    filei = readInput(args)
    fileo = args.o

    open(fileo,'w')

    for i in range(len(filei)):
        if i+ng <= len(filei):
            aux = filei[i:i+ng]
            search(aux,filei,ng,i,dic)
    print(dic)        

    return 0

if __name__  == "__main__":
    sys.exit(kasiski())