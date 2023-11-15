import argparse
import os
import sys
from random import randint

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
        ".", "").replace(",", "").replace(";", "").replace(":", ""))

    if not args.P and not args.I:
        parser.error("You must specify either -P or -I")

    if args.P and args.I:
        parser.error("You must put only one -P or -I")

    # Inicializar un diccionario para contar las frecuencias de cada letra
    frequenciestext = {}
    frequenciescyphered= {}

    for i in inputFile:
        if i in frequenciestext:
            frequenciestext[i] += 1
        else:
            frequenciestext[i] = 1   

    for key, value in frequenciestext.items():
        frequenciestext[key] = value / len(inputFile)

    print(frequenciestext) 

    for i in range(len(inputFile)):
        k = alphabet[randint(0,m-1)]
        if args.I:		
            if k==ord("O") or k==ord("C") or k==ord("B  "):
                k=ord("X")
			
		
        outputFile.write(chr((((ord(inputFile[i])-65)+(ord(k)-65))% m)+ 65))
    with open(args.i, encoding='UTF-8') as f:
        cyphertext = f.read(outputFile)

    for i in outputFile:
        if i in frequenciescyphered:
            frequenciescyphered[i] += 1
        else:
            frequenciescyphered[i] = 1   
    for key, value in frequenciescyphered.items():
        frequenciescyphered[key] = value / len(outputFile)


if __name__ == "__main__":
    sys.exit(segPerf())
