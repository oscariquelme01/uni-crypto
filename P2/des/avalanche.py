from desCTR import des, randomKey


def xor(a, b):
    solution = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            solution += "0"
        else:
            solution += "1"

    return solution


# xor entre los dos numeros, luego hacemos un recuento de los bits que han cambiado y dividimos esto por la longitud de los numeros, teniendo asi una representacion de lo 'distintos' que son los numeros
# Un buen resultado para un algoritmo debe estar cerca del 0.5 al cambiar un solo bit porque indica que cerca de la mitad de bits han cambiado.
def differenceIndex(n1, n2):
    xorResults = xor(n1, n2)
    equalBits = xorResults.count("0")

    return equalBits / len(xorResults)


def main():
    block = input("Input block (less than 8 characters): ").upper()
    key = randomKey()

    print('\nChanging the first bit of the key:')
    print("key:          ", key)
    firstResult = des(block, key)
    firstBitModified = '1' if key[0] == '0' else '0'
    key = firstBitModified + key[1:]
    print("modified key: ", key)
    secondResult = des(block, key)
    print('Index is ', differenceIndex(firstResult, secondResult))

    print('\nChanging the last character of the block')
    print('First block:  ', block)
    lastBlockChar = ord(block[-1]) - ord('A')
    nextChar = chr((lastBlockChar + 1) % 26 + ord('A'))
    block = block[:-1] + nextChar
    print('Second block: ', block)
    thirdResult = des(block, key)
    print('Index is ', differenceIndex(secondResult, thirdResult))

if __name__ == "__main__":
    main()
