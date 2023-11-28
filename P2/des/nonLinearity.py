from const import *
import matplotlib.pyplot as plt

MAX_48_BIT_INTEGER = 2**48 - 1

def generate48BitInputFromNumber(number):
    binaryRepresentation = bin(number)[2:]
    if len(binaryRepresentation) > 48:
        print('Numer is too big!')
        return ''

    while len(binaryRepresentation) < 48:
        binaryRepresentation = "0" + binaryRepresentation

    return binaryRepresentation

def intTo16BitBinary(number: int):
    if number >= 2**4 or number < 0:
        print('wrong number passed to intTo16BitBinary function')
        return ''

    binRepresentation = bin(number)[2:]
    while len(binRepresentation) < 4:
        binRepresentation = '0' + binRepresentation

    return binRepresentation

def sBoxOperation(sBox, binaryInput):
    if len(binaryInput) != 48:
        print("Wrong output length for sBoxOperation")
        return

    result = ""
    for i in range(0, len(binaryInput), 6):
        block = binaryInput[i : i + 6]
        row = int(block[0] + block[-1], 2)
        column = int(block[1:5], 2)

        output = str(sBox[row][column])
        result += intTo16BitBinary(sBox[row][column])

    return int(result, 2)


def main():
    data = []

    for i in range(1000):
        input = generate48BitInputFromNumber(i)
        output = sBoxOperation(S_BOXES[1], input)

        data.append(output)

    plt.plot(data)

    plt.xlabel('decimal input')
    plt.ylabel('decimal output')
    plt.title('Non-linearity of S-boxes in des')

    plt.show()

if __name__ == "__main__":
    main()
