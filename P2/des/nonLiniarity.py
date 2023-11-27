from const import *


def generate48BitInputFromNumber(number):
    binaryRepresentation = bin(number)[2:]
    if len(binaryRepresentation) > 48:
        print('Numer is too big!')
        return ''

    while len(binaryRepresentation) < 48:
        binaryRepresentation = "0" + binaryRepresentation

    return binaryRepresentation


def sBoxOperation(sBox, binaryInput):
    if len(binaryInput) != 48:
        print("Wrong output length for sBoxOperation")
        return

    print(binaryInput)
    output = ""
    for i in range(0, len(binaryInput), 6):
        block = binaryInput[i : i + 6]
        row = int(block[0] + block[-1], 2)
        column = int(block[1:5], 2)

        output += str(sBox[row][column])

    return output


def main():
    output = sBoxOperation(S_BOXES[1], generate48BitInputFromNumber(211812313212631))
    print(output)


if __name__ == "__main__":
    main()
