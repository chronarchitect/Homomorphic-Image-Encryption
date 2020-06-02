import math

def multiplicative_order (n, modulus) :
    """
    multiplicative_order( n, modulus)
    
    returns multiplicative order k
    k is the smallest positive integer
    such that n ^ k = 1 (mod modulus)
    
    """
    if modulus == 1:
        raise ArithmeticError("modulus of 1 specified")
    if math.gcd (n , modulus) > 1 :
        raise ArithmeticError("non-coprime n and modulus specified")
    else:
        order = 1
        mod_exp = n % modulus
        while mod_exp != 1 :
            order += 1
            mod_exp = (mod_exp * n) % modulus
        return order


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
