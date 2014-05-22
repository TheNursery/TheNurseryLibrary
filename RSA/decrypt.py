from encrypt import readKey
import argparse

def decrypt(c, n, d):
    m = pow(c, d, n)
    return m

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', 
                        help="Run with Debug Output", default=0, type=int)
    parser.add_argument('-k', '--keyfile', 
                        help="Source of public encryption key", 
                        default='pri.key', type=str)
    args = parser.parse_args()

    nstr, dstr, pstr, qstr = readKey(args.keyfile)
    n = int(nstr)
    d = int(dstr)

    if args.debug: print n, d

    c = input('Enter Encrypted Message Number: ')

    m = decrypt(c, n, d)

    print 'Decrypted value:', m

if __name__ == "__main__":
    main()
