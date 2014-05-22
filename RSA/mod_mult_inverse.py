
def my_pow(a, b, m):

    c = 1
    p = 0

    while p < b:
        c = (a * c)%m
        p = p + 1

    return c

def my_gcd(a, b):
    r0 = max(a, b)
    r1 = min(a, b)

    s0 = 1
    s1 = 0

    t0 = 0
    t1 = 1

    while r0%r1 > 0:
        q2 = r0 / r1
        r2 = r0%r1
        r0 = r1
        r1 = r2

        s2 = s0 - q2*s1
        s0 = s1
        s1 = s2

        t2 = t0 - q2*t1
        t0 = t1
        t1 = t2

    gcd_val = r1
    c = s1
    d = t1

    return gcd_val, c, d

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modmulinv(a, m):
    g, x, q = egcd(a, m)
    if g != 1:
        print 'Modular Multiplicative Inverse does not exist: gcd is not 1'
        print 'gcd = ', g
    else:
        return x % m
