import math
import argparse

the_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']

def readGodel(filename):

    fi = open(filename, 'r')

    int_list = []

    for line in fi:
        line = line[:-1]
        int_list.append(int(line))

    return int_list

def decode(integer, primelist):

    power_list = []

    for prime in primelist:
        power = 0
        while integer%prime == 0:
            integer = integer / prime
            power = power + 1
        power_list.append(power)

    return power_list

def primes(highest):

    prime_list = []

    for num in range(2,highest):
        if all(num%i != 0 for i in range(2,num)):
            prime_list.append(num)     

    return prime_list

def ints2str(int_list):

    string = ''

    for i in int_list:
        if (i != 0): string = string + the_alphabet[i-1]

    return string

def decodeFile(filename, highest, debug=False):

    plist = primes(1000)

    ilist = readGodel(filename)

    if debug: print ilist

    words = ''

    for integer in ilist:

        if debug: print integer

        pow_list = decode(integer, plist)
        
        if debug: print pow_list

        word = ints2str(pow_list)

        if debug: print word

        words = words + word + ' '

    return words

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', 
                        help="Run with Debug Output", default=0, type=int)
    parser.add_argument('-f', '--filename', 
                        help="Filename to write wav file", 
                        default='test.txt', type=str)
    parser.add_argument('-p', '--max_prime',
                        help="Maximum prime to use for factorization",
                        default=1000, type=int)
    args = parser.parse_args()

    print 'Reading file', args.filename, '...'

    outstr = decodeFile(args.filename, args.max_prime, debug=args.debug)

    print 'Contents of', args.filename, '...'
    print outstr

if __name__ == "__main__":
    main()
