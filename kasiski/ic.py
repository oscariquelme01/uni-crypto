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

def mcd(a):
    return math.gcd(*a)

    
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

def ic_seg(segmento,m):
    aux = 0
    f = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
         'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    
    for i in segmento:
        f[i] += 1
    
    for i in range(m):
        aux += ((f[chr(i+65)])*(f[chr(i+65)]-1))/(len(segmento)*(len(segmento)-1))
    
    return aux
 
def ic():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=False, type=checkPositive)
    parser.add_argument('-i', required=False, type=str)
    parser.add_argument('-o', required=False, type=str)

    args = parser.parse_args()
    
    filei = readInput(args)
    ng = int(args.l)
    lista=[]
    m = 26
    
    # Inicializar un diccionario para contar las frecuencias de cada letra
    f = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
         'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    
    # Calcular las frecuencias de las letras
    for i in filei:
        f[i] += 1
    
    for i in range(ng):
        lista.append("") 
        
    for i,value in enumerate(filei):
        lista[i%ng]+=value

    p = 0
    for seg in lista:
        p += ic_seg(seg,m)

    indice = p/ng

    return indice


if __name__  == "__main__":
    sys.exit(ic())