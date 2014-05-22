import random
import fractions
import gmpy
from mod_mult_inverse import modmulinv

def new_e(plist, tot_n):
    e = tot_n + 1
    while e > tot_n:
        i = random.randint(2, len(plist)-1)
        e = plist[i]
    return e

def genKeys(p, q):

    n = p*q

    tot_n = (p-1)*(q-1)

    plist = primes(tot_n)

    e = new_e(plist, tot_n)

    while fractions.gcd(e, tot_n) > 1:
        e = e + 1

    d = modmulinv(e, tot_n)

    public = (n, e)
    private = (n, d, p, q)

    return public, private

def primes(highest):

    prime_list = []

    for num in range(2,highest):
        if all(num%i != 0 for i in range(2,num)):
            prime_list.append(num)     

    return prime_list

plist = primes(2000)

ind1 = random.randint(1, len(plist)-1)
ind2 = random.randint(1, len(plist)-1)

p = plist[ind1]
q = plist[ind2]

pub, pri = genKeys(p, q)

prifi = open('pri.key', 'w')
pubfi = open('pub.key', 'w')

for v in pri:
    prifi.write(str(v) + ' ')
for v in pub:
    pubfi.write(str(v) + ' ')

prifi.close()
pubfi.close()

print pub, pri
