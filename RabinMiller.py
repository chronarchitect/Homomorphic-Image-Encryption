import random
import ModularArithmetic as mod

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
        return 1 in mod.binary_exponent(rand, n-1, n)

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
