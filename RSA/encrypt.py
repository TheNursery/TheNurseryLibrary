import argparse
import fractions
from mod_mult_inverse import my_pow

def readKey(filename):
    
    pubfi = open(filename, 'r')
    vals = pubfi.readline().split(' ')

    return vals[:-1]

def encrypt(m, n, e):
    c = my_pow(m, e, n)
    return c

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', 
                        help="Run with Debug Output", default=0, type=int)
    parser.add_argument('-k', '--keyfile', 
                        help="Source of public encryption key", 
                        default='pub.key', type=str)
    args = parser.parse_args()

    nstr, estr = readKey(args.keyfile)
    n = int(nstr)
    e = int(estr)

    if args.debug: print n, e

    if args.debug: print 'GCD:', fractions.gcd(n, e)

    m = input('Enter Message Number: ')

    c = encrypt(m, n, e)

    print 'Encrypted value:', c

if __name__ == "__main__":
    main()
