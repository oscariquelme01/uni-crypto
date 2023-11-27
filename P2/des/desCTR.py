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
            return data.strip("\n")
    else:
        return ""


def paddingTo64(string):
    if len(string.replace(" ", "")) % BLOCK_SIZE != 0:
        string += "0"
        return paddingTo64(string)

    return string


def stringToBinary(string: str):
    ret = ""
    for c in string:
        bits = bin(ord(c)).replace("0b", "")
        for i in range(
            8 - len(bits)
        ):  # 8 is the desired length for out bits so we add padding
            bits = "0" + bits

        ret += bits

    return ret


def hexToBinary(hexString: str):
    binaryRepresentation = bin(int(hexString, 16))[2:]
    while len(binaryRepresentation) % 4 != 0:
        binaryRepresentation = "0" + binaryRepresentation
    return binaryRepresentation


def textInBlocks(string: str):
    blocks_input = []
    for i in range(0, len(string), 64):
        blocks_input.append(string[i : i + 64])
    return blocks_input


def doPermutation(permutation, source):
    ret = ""
    for i in range(len(permutation)):
        ret += source[permutation[i] - 1]

    return ret


def generateKeys(initialKey):
    # Reduce key into 56 bits and split it into left and right
    initialBinaryKey = initialKey
    initialReducedKey = doPermutation(PC_1, initialBinaryKey)

    halvedLength = int(len(initialReducedKey) / 2)

    leftReducedKey = initialReducedKey[:halvedLength]
    rightReducedKey = initialReducedKey[halvedLength:]

    leftReducedKeylist = []
    rightReducedKeylist = []

    leftReducedKeylist.append(leftReducedKey)
    rightReducedKeylist.append(rightReducedKey)

    for i in range(len(ROUND_SHIFTS)):
        shifts = ROUND_SHIFTS[i]
        for _ in range(shifts):
            leftReducedKey = leftReducedKey[1:] + leftReducedKey[0]
            rightReducedKey = rightReducedKey[1:] + rightReducedKey[0]

        leftReducedKeylist.append(leftReducedKey)
        rightReducedKeylist.append(rightReducedKey)

    keysList = []
    for i in range(len(leftReducedKeylist)):
        reducedKey = leftReducedKeylist[i] + rightReducedKeylist[i]
        reducedKey = doPermutation(PC_2, reducedKey)
        keysList.append(reducedKey)

    return keysList


def des(ctr, initialKey):
    initialKey = "0001001100110100010101110111100110011011101111001101111111110001"
    # Step 1
    keys = generateKeys(initialKey)

    # Step 2
    block = paddingTo64(stringToBinary(str(ctr)))
    result = ""

    ip = doPermutation(IP, block)
    leftIp = ip[:32]
    rightIp = ip[32:]

    for i in range(NUM_SUBKEYS):
        aux = rightIp
        rightIp = xor(leftIp, function(rightIp, keys[i + 1]))
        leftIp = aux

    result = doPermutation(IP_INV, rightIp + leftIp)
    return result


def randomKey():
    key = ""
    for i in range(64):
        key += str(randint(0, 1))
    return key


def xor(a, b):
    solution = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            solution += "0"
        else:
            solution += "1"

    return solution


def function(rightIp, key):
    rightIp = doPermutation(E, rightIp)
    xorKeyRightIp = xor(key, rightIp)

    blocksXOR = []
    for i in range(0, len(xorKeyRightIp), 6):
        blocksXOR.append(xorKeyRightIp[i : i + 6])

    result = s_function(blocksXOR)

    return result


def s_function(blocks):
    solution = ""
    for i in range(len(S_BOXES)):
        box = S_BOXES[i]
        block = blocks[i]

        # grab first and last element to index row, then use the rest of the bites to index column
        row = int(block[0] + block[-1], 2)
        column = int(block[1:5], 2)

        solution += decimalToBinary(box[row][column])

    solution = doPermutation(P, solution)
    return solution


def decimalToBinary(decimal):
    binary = bin(decimal).replace("0b", "")
    while len(binary) < 4:
        binary = "0" + binary
    return binary


def binaryToDecimal(binary):
    decimal = i = 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def desCTR():
    parser = argparse.ArgumentParser()
    parser.add_argument("-C", required=False, action="store_true")
    parser.add_argument("-D", required=False, action="store_true")
    parser.add_argument("-k", required=False, type=str)
    parser.add_argument("-ctr", required=True, type=int)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    inputFile = readInput(args).upper()
    outputFile = open(args.o, "w") if args.o else sys.stdout
    ctr = int(args.ctr)
    if args.k:
        key = args.k
    else:
        key = randomKey()

    # print("Key: " + key)
    if len(key) != BLOCK_SIZE:
        print(f"Invalid key: must be {BLOCK_SIZE} bits")
        return

    if args.C:
        outputFile.write(encrypt(ctr, key, inputFile))
    elif args.D:
        outputFile.write(decrypt(ctr, key, inputFile))


def encrypt(counter, key, inputFile):
    solution = ""

    binaryInput = stringToBinary(inputFile)
    paddingLength = BLOCK_SIZE - (len(binaryInput) % BLOCK_SIZE)
    inputText = paddingTo64(binaryInput)
    inputBlocks = textInBlocks(inputText)
    for block in inputBlocks:
        cypheredCounter = des(counter, key)
        solution += xor(cypheredCounter, block)

        counter += 1

    outputText = ""
    for i in range(0, len(solution) - paddingLength, 8):
        chunk = solution[i : i + 8]
        character = hex(int(solution[i : i + 8], 2))[2:]
        if len(character) == 1:
            character = "0" + character

        outputText += character

    print("cyphered text: ", outputText)
    return outputText


def decrypt(counter, key, inputFile):
    solution = ""

    binaryInput = hexToBinary(inputFile)
    paddingLength = BLOCK_SIZE - (len(binaryInput) % BLOCK_SIZE)
    inputText = paddingTo64(binaryInput)
    inputBlocks = textInBlocks(inputText)
    for block in inputBlocks:
        decipheredCounter = des(counter, key)
        solution += xor(decipheredCounter, block)

        counter += 1

    outputText = ""
    for i in range(0, len(solution) - paddingLength, 8):
        outputText += chr(int(solution[i : i + 8], 2))

    print("deciphered text: ", outputText)

    return outputText


if __name__ == "__main__":
    sys.exit(desCTR())
