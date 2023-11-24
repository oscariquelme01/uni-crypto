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


def paddingTo64(result):
    if len(result.replace(" ", "")) % BLOCK_SIZE != 0:
        result += "0"
        return paddingTo64(result)

    return result


def stringToBinary(string: str):
    ret = ""
    for c in string:
        # si queremos meter -65 pra trabajar con A=0
<<<<<<< HEAD
        bits = bin(ord(c)).replace("0b", "")
        for i in range(8 - len(bits)):  # 8 is the desired length for out bits so we add padding
=======
        bits = bin(ord(c)).replace("0b", "")
        for i in range(
            8 - len(bits)
        ):  # 8 is the desired length for out bits so we add padding
>>>>>>> af4c848 (Miprimerachamba)
            bits = "0" + bits

        ret += bits

    return ret


def text_in_blocks(string: str):
    blocks_input = []
    for i in range(0, len(string), 64):
        blocks_input.append(string[i : i + 64])
    return blocks_input


def doPermutation(permutation, source):
    ret = ""
    for i in range(len(permutation)):
        ret += source[permutation[i] - 1]

    return ret


def des(ctr, key):
    # Reduce key into 56 bits and split it into left and right
    binaryKey = key
    reducedKey = doPermutation(PC_1, binaryKey)

    halvedLength = int(len(reducedKey) / 2)

    leftReducedKey = reducedKey[:halvedLength]
    rightReducedKey = reducedKey[halvedLength:]

    leftReducedKeylist = []
    rightReducedKeylist = []

    leftReducedKey_aux = leftReducedKey
    rightReducedKey_aux = rightReducedKey

    leftReducedKeylist.append(leftReducedKey_aux)
    rightReducedKeylist.append(rightReducedKey_aux)

    for i in range(16):
        shifts = ROUND_SHIFTS[i]
        for x in range(shifts):
            aux_left = leftReducedKey_aux[0]
            aux_right = rightReducedKey_aux[0]
            leftReducedKey_aux = leftReducedKey_aux[1:] + aux_left
            rightReducedKey_aux = rightReducedKey_aux[1:] + aux_right
        leftReducedKeylist.append(leftReducedKey_aux)
        rightReducedKeylist.append(rightReducedKey_aux)

    key_list = []
    for i in range(16):
        aux_key = leftReducedKeylist[i] + rightReducedKeylist[i]
        reducedKey_aux = doPermutation(PC_2, aux_key)
        key_list.append(reducedKey_aux)

    # Step 2
    block = paddingTo64(stringToBinary(ctr))
    result = ""
  
    ip = doPermutation(IP, block)
    leftIp = ip[:32]
    rightIp = ip[32:]
    leftIp_list = []
    rightIp_list = []
    rightIp_aux = rightIp
    leftIp_aux = leftIp
    for i in range(16):
        leftIp_list.append(rightIp_aux)
        rightIp_aux = xor(leftIp_aux, function(rightIp_aux,key_list[i]))
        rightIp_list.append(rightIp_aux)
        leftIp_aux = rightIp_aux

    result = doPermutation(IP_INV,rightIp_list[15] + leftIp_list[15])
    return result    

def random_key():
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

    blocks_xor = []
    for i in range(0, len(xorKeyRightIp), 6):
        blocks_xor.append(xorKeyRightIp[i : i + 6])

    result = s_function(blocks_xor)

    return result

def s_function(blocks):
    solution = ""
    for i in range(len(S_BOXES)):
        box = S_BOXES[i]
        block = blocks[i]

        # grab first and last element to index row
        row = int(block[0] + block[-1], 2)
        column = int(block[1:5], 2)

        solution += decimalToBinary(box[row][column])

    solution = doPermutation(P,solution)
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
    parser.add_argument("-ctr", required=True, type=str)
    parser.add_argument("-i", required=False, type=str)
    parser.add_argument("-o", required=False, type=str)

    args = parser.parse_args()

    if not args.C and not args.D:
        parser.error("You must specify either -D or -C")

    inputFile = readInput(args).upper()
    outputFile = open(args.o, "w") if args.o else sys.stdout
    ctr = args.ctr
    if args.k:
        key = args.k
    else:
        key = random_key()

    print("Key: " + key)
    if len(key) != BLOCK_SIZE:
        print(f"Invalid key: must be {BLOCK_SIZE} bits")
        return


    if args.C:
        outputFile.write(cifrar(ctr,key,inputFile))
    elif args.D :
        descifrar(ctr,key,inputFile)

    
    
  
   

def cifrar(ctr,key,inputFile):
    cypheredCounter = des(ctr, key)

    inputText = paddingTo64(stringToBinary(inputFile))
    solution =""
    inputBlocks = text_in_blocks(inputText)
    for block in inputBlocks:
        solution += xor(cypheredCounter,block)
    
    print(solution)
    outputText = ""
    for i in range(0, len(solution), 8):    
        outputText += chr(int(solution[i:i+8],2))

    return outputText


def descifrar(ctr,key,inputFile):
    return 0

if __name__ == "__main__":
    sys.exit(desCTR())
