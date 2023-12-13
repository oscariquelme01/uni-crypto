import gmpy2 as gmp
import argparse
import sys
import time
import random

def checkPositive(value):
    if int(value) <= 0: raise argparse.ArgumentTypeError("%s is not a positive integer" % value)

    return int(value)

def checkPositiveFloat(value):
    if float(value) <= 0: raise argparse.ArgumentTypeError("%s is not a positive float" % value)

    return float(value)

def randomInteger(significantBits):
    if significantBits <= 0:
        raise ValueError("Number of significant bits must be greater than zero")

    random_number = random.getrandbits(significantBits)

    return random_number

def millerRabin(candidate, iterations):
    # handle special cases
    if candidate <= 1:
            return False
    if candidate == 2 or candidate == 3:
        return True
    if candidate % 2 == 0:
        return False

    # Write candidate as 2^k * d where d and k are both integers and d is odd 
    exp, oddNumber = 0, candidate - 1
    while oddNumber % 2 == 0:
        exp += 1
        oddNumber //= 2

    # miller rabin iterations
    for i in range(iterations):
        rand = random.randint(2, candidate - 2)
        x = pow(rand, oddNumber, candidate)

        if x == 1 or x == candidate - 1:
            return True

        while oddNumber != candidate - 1:
            x = (x * x) % candidate
            oddNumber *= 2

            if x == 1:
                return False
            if x == candidate - 1:
                return True

        return False

def getIterations(minAccuracy):
    if minAccuracy >= 1:
        return 0

    iterations = 0
    while True:
        iterations += 1
        accuracy = 1 - 4 ** (-iterations)
        if accuracy > minAccuracy:
            return iterations

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", required=True, type=checkPositive)
    parser.add_argument("-p", required=True, type=checkPositiveFloat)
    parser.add_argument("-o", required=False, type=str)
    args = parser.parse_args()
    minimumAccuracy = args.p
    iterations = getIterations(minimumAccuracy)

    if not iterations:
        print('Wrong -p argument, must be a float number between 1 and 0')
        return

    # Generate random number with the specified significant bits
    significantBits = int(args.b)
    candidate = randomInteger(significantBits)
    print(f'Candidate number: {candidate}')

    isPrime = millerRabin(candidate, iterations)
    print(f'Number is {"prime" if isPrime else "composite"}')
    if isPrime:
        print(f'Prime accuracy: {1 - 4 ** (-iterations)} (Iterations: {iterations})')

    gmpIsPrime = gmp.mpz(candidate).is_prime()
    print(f'According to gmp, number is {"prime" if gmpIsPrime else "composite"}')

    outputFile = open(args.o, 'w') if args.o else sys.stdout

    return 

if __name__ == "__main__":
    main()
