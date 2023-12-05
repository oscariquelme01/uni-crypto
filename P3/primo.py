import gmpy2 as gmp
import argparse
import sys
import time

def checkPositive(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % value)

    return int(value)


def millerrabin(p):

    #Primero comprobamos que sea impar.
    if p%2==0 or p ==0:
        return False
        #False = no primo
        #True = primo
 
    #Expresamos p-1 como 2^u*s, con s impar.
    s = p-1
    #Dividir s por 2 hasta que el resultado sea impar.
    u = 0
    while 1&s==0:
        u= u+1
        s = s >> 1
 
    print(p,"= 2^",u,"*",s)
 
    for _ in range(20):#Ejecuciones para reducir las probabiliades de fallo.
        #Elegimos a al azar tal que 2 <= a <= p-2
        a = randint(2, p - 2)
        a = powerModInt(a,s,p)
 
        if a == 1 or a == p-1:#p-1 = -1
            return True
        else:
            for i in [1,1,u-1]:
                a = powerModInt(a,2,p)
                if a == p-1:
                    return True
                elif a == 1:
                    return False
                i=i+1
            return False
        

def primo():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", required=True, type=checkPositive)
    parser.add_argument("-p", required=True, type=checkPositive)
    parser.add_argument("-o", required=False, type=str)
    args = parser.parse_args()

    bits = int(args.b)
    sec = args.p
    outputFile = open(args.o, 'w') if args.o else sys.stdout

    return 