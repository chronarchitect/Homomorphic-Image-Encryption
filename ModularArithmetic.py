def lcm(a, b):
    """
    lcm(a, b)

    returns Lowest Common Multiple of a and b
    """
    return a * b // xgcd(a,b)[0]

def xgcd(a, b):
    """
    xgcd (a, b)

    returns (g, x, y) according to the Extended Euclidean Algorithm
    such that, ax + by = g
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = xgcd(b % a, a)
        return (g, x - (b // a) * y, y)

def multiplicative_inverse(a, modulus):
    """
    multiplicative_inverse(a, modulus)

    returns x: multiplicative inverse of a
    such that, a * x = 1 (mod modulus)
    """
    g, x, y = xgcd(a, modulus)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % modulus


def binary_exponent(base, exponent, modulus):
    """
    modular_binary_exponent( base, exponent, modulus)
    
    args:
        base
        exponent
        modulus
    
    generates:
        base ^ exponent (mod modulus)
    
        along with intermediate results from binary exponentiation
        required for Rabin-Miller primality test
    """
    if modulus == 1:
        yield 0
        return
    bitmask = 1 << exponent.bit_length() - 1
    res = 1
    while bitmask:
        res = (res * res) % modulus
        if bitmask & exponent:
            res = (res * base) % modulus
        yield res
        bitmask >>= 1
