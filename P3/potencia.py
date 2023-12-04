import gmpy2 as gmp
import argparse
import sys
import time

def checkPositive(value):
    if int(value) <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % value)

    return int(value)

def exp_normal(base, exponente, modulo):
    resultado = gmp.mpz(1)

    while(exponente > 0):
        resultado *= gmp.mpz(base) 
        exponente -= gmp.mpz(1)
        resultado = gmp.mpz(resultado % modulo)
    
    return resultado

def exp_gmp(base , exponente, modulo):
    resultado = gmp.mpz(1)
    resultado = gmp.mpz(pow(base,exponente,modulo))
    return resultado


def tiempo_gmp(base,exponente,modulo):
    inicio = time.time()
    solucion = exp_gmp(base,exponente,modulo)
    print(time.time() - inicio)
    return solucion
    
def tiempo_normal(base,exponente,modulo):
    inicio = time.time()
    solucion = exp_normal(base,exponente,modulo)
    print(time.time() - inicio)
    return solucion

def potencia():

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", required=True, type=checkPositive)
    parser.add_argument("-exp", required=True, type=checkPositive)
    parser.add_argument("-m", required=True, type=checkPositive)
    args = parser.parse_args()

    base = gmp.mpz(int(args.b))
    exponente = gmp.mpz(int(args.exp))
    modulo = gmp.mpz(int(args.m))

    solucion1 = gmp.mpz(tiempo_gmp(base,exponente,modulo))
    solucion2 = gmp.mpz(tiempo_normal(base,exponente,modulo))

    print("Solucion 1: "+str(solucion1))
    print("Solucion 2: "+str(solucion2))

if __name__ == "__main__":
    sys.exit(potencia())