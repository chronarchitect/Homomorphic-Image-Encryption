import math
import random

def modular_binary_exponent(base, exponent, modulus):
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

def is_probably_prime(n):
    """
    is_probably_prime(n)

    args:
        n
    returns:
        Boolean

    returns True if n is a probable prime
    based on the Rabin-Miller primality test
    """
    tests = max(128, n.bit_length())
    for i in range(tests):
        rand = random.randint(1,n-1)
        return 1 in modular_binary_exponent(rand, n-1, n)

def generate_prime(bitlen=128):
    """
    generate_prime(bitlen)

    args:
        bitlen: length of number to be generated (default: 128)
    returns:
        a probable prime of bitlen bits
        based on the Rabin-Miller primality test
    """
    n = random.getrandbits(bitlen) | 1<<(bitlen-1) | 1
    while not is_probably_prime(n):
        n = random.getrandbits(bitlen) | 1<<(bitlen-1) | 1
    return n
