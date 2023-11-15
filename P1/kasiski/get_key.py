import argparse
import os
import gmpy2 as gmp
from os.path import isfile
import sys
import math

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

PJ = {'A': 0.0804, 'B': 0.0154, 'C': 0.0306, 'D': 0.0399, 'E': 0.1251, 'F': 0.0230, 'G': 0.0196, 'H': 0.0549, 
      'I': 0.0726, 'J': 0.0016, 'K': 0.0067, 'L': 0.0414, 'M': 0.0253,  'N': 0.0709, 'O': 0.0760, 'P': 0.0200, 
      'Q': 0.0011, 'R': 0.0612, 'S': 0.0654, 'T': 0.0925, 'U': 0.0271,  'V': 0.0099, 'W': 0.0192, 'X': 0.0019, 
      'Y': 0.0173, 'Z': 0.0019}

def function(segmento,m):
    a = 0
    aux = 0
    f = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
         'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    
    for i in segmento:
        f[i] += 1

    for j in range(m):
        for k in range(m):
            a += PJ[chr(k+65)] * (f[chr(((k+j)% m)+65)]/(len(segmento)))

        if a > aux:
            aux = a
            p = j
        a = 0
    return p


def get_key():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=False, type=checkPositive)
    parser.add_argument('-i', required=False, type=str)
    parser.add_argument('-o', required=False, type=str)

    args = parser.parse_args()

    ng = int(args.l)
    filei = readInput(args)
    fileo = args.o

    m = 26
    l = ""
    lista = []
    open(fileo,'w')
    
    for i in range(ng):
        lista.append("") 
   
   
    for i,value in enumerate(filei):
        lista[i%ng]+=value

    for i in lista:
        p = function(i,m)
        l += chr(p+65) 

    with open(fileo, 'a') as f:
        f.write(l)

    return l

if __name__  == "__main__":
    sys.exit(get_key())