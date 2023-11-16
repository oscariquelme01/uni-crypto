import argparse
import os
import sys
from random import randint
import numpy
import string

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def readInput(args):
    if args.i is None:
        inputString = input("Input string: ")
        return inputString.strip('\n')
    else:
        if os.path.isfile(args.i):
            with open(args.i, encoding='UTF-8') as f:
                data = f.read(os.stat(args.i).st_size)
                return data.strip('\n')


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n"),
        ("ü", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def segPerf():
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", required=False, action="store_true")
    parser.add_argument("-I", required=False, action="store_true")
    parser.add_argument('-i', required=False, type=str)
    parser.add_argument('-o', required=False, type=str)

    args = parser.parse_args()

    inputFile = readInput(args)
    outputFile = open(args.o, 'w') if args.o else sys.stdout
    m = 26

    inputFile = normalize(inputFile.upper().replace(" ", "").replace(
        ".", "").replace(",", "").replace(";", "").replace(":", "").replace("\n","").replace("-","").replace("¿","")
        .replace("'","").replace("?","").replace("¡","").replace("!","").replace("«","").replace("»","").replace("(",""))

    if not args.P and not args.I:
        parser.error("You must specify either -P or -I")

    if args.P and args.I:
        parser.error("You must put only one -P or -I")

    # Inicializar un diccionario para contar las frecuencias de cada letra
    frequenciestext = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
         'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    frequenciescyphered= {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0,
         'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    cypheredtxt = ""
    p_xy = numpy.zeros(shape=(m,m))
    p_xy_frequencies = numpy.zeros(shape=(m,m))
    p_xy_final = numpy.zeros(shape=(m,m))
    counter = 0

    for i in inputFile:
        if i not in string.ascii_uppercase:
            continue
        frequenciestext[i] += 1
        counter += 1
    
    textlenght = counter
 
    for key, value in frequenciestext.items():
        frequenciestext[key] = value / textlenght

    for i in range(textlenght):
        k = alphabet[randint(0,m-1)]
        if args.I:		
            if k==ord("O") or k==ord("C") or k==ord("B"):
                k=ord("X")
		
        cypheredtxt += chr((((ord(inputFile[i])-65)+(ord(k)-65))% m)+ 65)

    outputFile.write(cypheredtxt)

    for i in cypheredtxt:
        frequenciescyphered[i] += 1
  
    for key, value in frequenciescyphered.items():
        frequenciescyphered[key] = value / textlenght

    for i in range(textlenght):
        p_xy[(ord(inputFile[i])-65)% m][(ord(cypheredtxt[i])-65)% m]+=1

    for i in range(m):
        for j in range(m):
            p_xy_frequencies[i][j] = p_xy[i][j] / textlenght   

    for i,char in enumerate(string.ascii_uppercase):
       for j,char2 in enumerate(string.ascii_uppercase): 
            p_xy_final[i][j] = p_xy_frequencies[i][j] * frequenciestext[char] / frequenciescyphered[char2] 

    print(p_xy_final)
    print(len(inputFile))

if __name__ == "__main__":
    sys.exit(segPerf())
