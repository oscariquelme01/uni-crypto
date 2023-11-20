import argparse
import os
import sys
from random import randint
import numpy
import string

alphabet = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


def readInput(args):
    if os.path.isfile(args.i):
        with open(args.i, encoding="UTF-8") as f:
            data = f.read(os.stat(args.i).st_size)
            return data.strip("\n")
    else:
        return ""


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n"),
        ("ü", "u"),
        ("Ï", "I"),
        ("À", "A"),
        ("Ù", "U"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


def segPerf():
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", required=False, action="store_true")
    parser.add_argument("-I", required=False, action="store_true")
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    inputFile = readInput(args)
    outputFile = open(args.o, "w") if args.o else sys.stdout

    m = 26

    characterExceptions = [
        " ",
        ".",
        ",",
        ";",
        ":",
        "\n",
        "-",
        "¿",
        "'",
        '"',
        "?",
        "!",
        "¡",
        "«",
        "»",
        "(",
        ")",
        "]",
        "~",
        ""
    ]
    for i in range(9):
        characterExceptions.append(str(i))

    inputFile = normalize(inputFile.upper())
    for characterException in characterExceptions:
        inputFile = inputFile.replace(characterException, "")

    if not args.P and not args.I:
        parser.error("You must specify either -P or -I")

    if args.P and args.I:
        parser.error("You must put only one -P or -I")

    # Inicializar un diccionario para contar las frecuencias de cada letra
    frequenciesText = {
        "A": 0.0,
        "B": 0.0,
        "C": 0.0,
        "D": 0.0,
        "E": 0.0,
        "F": 0.0,
        "G": 0.0,
        "H": 0.0,
        "I": 0.0,
        "J": 0.0,
        "K": 0.0,
        "L": 0.0,
        "M": 0.0,
        "N": 0.0,
        "O": 0.0,
        "P": 0.0,
        "Q": 0.0,
        "R": 0.0,
        "S": 0.0,
        "T": 0.0,
        "U": 0.0,
        "V": 0.0,
        "W": 0.0,
        "X": 0.0,
        "Y": 0.0,
        "Z": 0.0,
    }
    frequenciesCyphered = {
        "A": 0.0,
        "B": 0.0,
        "C": 0.0,
        "D": 0.0,
        "E": 0.0,
        "F": 0.0,
        "G": 0.0,
        "H": 0.0,
        "I": 0.0,
        "J": 0.0,
        "K": 0.0,
        "L": 0.0,
        "M": 0.0,
        "N": 0.0,
        "O": 0.0,
        "P": 0.0,
        "Q": 0.0,
        "R": 0.0,
        "S": 0.0,
        "T": 0.0,
        "U": 0.0,
        "V": 0.0,
        "W": 0.0,
        "X": 0.0,
        "Y": 0.0,
        "Z": 0.0,
    }
    cypheredOutput = ""

    # Inicializamos 3 matrices cuadradas de ceros con tamaño igual al tamaño del alfabeto
    p_yx = numpy.zeros(shape=(m, m))
    p_xy_frequencies = numpy.zeros(shape=(m, m))
    p_xy_final = numpy.zeros(shape=(m, m))

    for i in inputFile:
        if i not in string.ascii_uppercase:
            continue
        frequenciesText[i] += 1

    textLenght = len(inputFile)

    for key, value in frequenciesText.items():
        frequenciesText[key] = value / textLenght

    for i in range(textLenght):
        k = alphabet[randint(0, m - 1)]
        if args.I:
            if k == "O" or k == "C" or k == "B":
                k = "X"

        cypheredLetter = ((ord(inputFile[i]) - 65) + (ord(k) - 65)) % m
        cypheredOutput += chr(cypheredLetter + 65)

    outputFile.write(cypheredOutput)

    for i in cypheredOutput:
        frequenciesCyphered[i] += 1

    for key, value in frequenciesCyphered.items():
        frequenciesCyphered[key] = value / textLenght

    for i in range(textLenght):
        if inputFile[i] in alphabet:
            p_yx[(ord(cypheredOutput[i]) - 65)][(ord(inputFile[i]) - 65)] += 1

    ###############################
    ## HASTA AQUI ESTA BIEN 100% ##
    ###############################

    # p_yx = p_yx / textLenght
    for i in range(m):
        for j in range(m):
            p_xy_frequencies[i][j] = p_yx[i][j] / textLenght

    for i, char in enumerate(alphabet):
        for j, char2 in enumerate(alphabet):
            p_xy_final[i][j] = (
                p_xy_frequencies[j][i] * frequenciesText[char] / frequenciesCyphered[char2]
            )

    for i in range(m):
        aux = 0.0
        for j in range(m):
            aux += p_xy_final[i][j]
            print(
                "P(" + chr(i + 65) + "|" + chr(j + 65) + ") = " + str(p_xy_final[i][j])
            )
        media = aux / m
        print("\n")
        print("media = " + str(media))
        print("P(" + chr(i + 65) + ") = " + str(frequenciesText[chr(i + 65)]))
        print("-----------------------------------------------------")


if __name__ == "__main__":
    sys.exit(segPerf())
