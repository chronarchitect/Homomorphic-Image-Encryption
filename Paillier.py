import random

import ModularArithmetic
import RabinMiller

class PrivateKey:
    """
    PrivateKey object contains λ and μ
    in accordance to the Paillier Cryptosystem
    
    args:
        p: a prime number
        q: another prime number
        (p and q are of equal length)
        n: product of p and q
        
    attributes:
        λ: lowest common multiple of p-1 and q-1
        ∵ p and q are of equal length we can use the simplification,
        μ: modular multiplicative inverse of λ and n
    """
    
    def __init__(self, p, q, n):

        self.λ = ModularArithmetic.lcm( p-1, q-1)
        self.μ = ModularArithmetic.multiplicative_inverse( self.λ, n)
        
    def __repr__(self):
        return ("---\nPrivate Key :\nλ:\t"+str(self.λ) +"\nμ:\t"+str(self.μ) +"\n---")


class PublicKey:
    """
    Public Key object contains n and g
    in accordance to the Paillier Cryptosystem
    
    args:
        n: product of two equal lenght prime numbers
    
    attributes:
        n: product of two primes
        g: a random number such that,
        multiplicative order of g in n^2 is a multiple of n
        
        ∵ p and q are of equal length we can use a simplification of g = n+1
    """
    def __init__(self, n):
        self.n = n
        self.nsq = n * n
        self.g = n+1
    
    def __repr__(self):
        return ("---\nPublic Key :\nn:\t"+ str(self.n) +"\n---")


def generate_keys(bitlen=128):
    """
    generate_keys( bitlen)
    
    args:
        bitlen: length of primes to be generated (default: 128)
    
    returns Public Private key pair as a tuple
    (PublicKey, PrivateKey)
    """
    
    p = RabinMiller.generate_prime(bitlen)
    q = RabinMiller.generate_prime(bitlen)
    n = p * q
    return (PublicKey(n), PrivateKey(p, q, n))


def Encrypt(public_key, plaintext, rn=None):
    """
    Encrypt( public_key, plaintext, rn=None)
    
    args:
        public_key: Paillier Publickey object
        plaintext: number to be encrypted
        rn: optional pre-computed r^n % n^2
        
    returns:
        ciphertext: encryption of plaintext
        such that ciphertext = (g ^ plaintext) * (r ^ n) (mod n ^ 2)
        where, r is a random number in n such that r and n are coprime
    """
    
    if rn is None:
        r = random.randint( 1, public_key.n-1)
        while not ModularArithmetic.xgcd( r, public_key.n)[0] == 1:
            r = random.randint( 1, public_key.n)
        rn = pow(r, public_key.n, public_key.nsq)
        
    # Optimization: Since g = n + 1, (n+1)^m mod n^2 = (1 + m*n) mod n^2
    a = (1 + (plaintext * public_key.n)) % public_key.nsq
    
    ciphertext = (a * rn) % public_key.nsq
    return ciphertext

def get_random_rn(public_key):
    """
    Generates a random r^n % n^2 for pre-computation.
    """
    r = random.randint( 1, public_key.n-1)
    while not ModularArithmetic.xgcd( r, public_key.n)[0] == 1:
        r = random.randint( 1, public_key.n)
    return pow(r, public_key.n, public_key.nsq)


def Decrypt(public_key, private_key, ciphertext):
    """
    Decrypt( publick_key, private_key, ciphertext)
    
    args:
        public_key: Paillier PublicKey object
        private_key: Paillier PrivateKey object
        ciphertext: Encrypted Integer which was ecnrypted using the public_key
        
    returns:
        plaintext: decryption of ciphertext
        such that plaintext = L(ciphertext ^ λ) * μ (mod n ^ 2)
        where, L(x) = (x - 1) / n
    """
    
    x = pow(ciphertext, private_key.λ, public_key.nsq)
    L = lambda x: (x - 1) // public_key.n
    
    plaintext = (L(x) * private_key.μ) % public_key.n 
    return plaintext


def homomorphic_add(public_key, a, b):
    """
    adds encrypted integer a to encrypted integer b 
    
    args:
        public_key
        encryption of integer a
        encryption of integer b
    returns:
        encryption of sum of a and b
    """
    return (a * b) % public_key.nsq


def homomorphic_add_constant(public_key, a, k):
    """
    adds a plaintext k to encrypted integer a
    
    args:
        public_key
        encryption of integer a
        plaintext k
    returns:
        encryption of sum of a and k
    """
    # Optimization: g^k mod n^2 = (1 + kn) mod n^2
    gk = (1 + (k * public_key.n)) % public_key.nsq
    return a * gk % public_key.nsq


def homomorphic_mult_constant(public_key, a, k):
    """
    multiplies a plaintext k to encrypted integer a
    
    args:
        public_key
        encryption of integer a
        plaintext k
    returns:
        encryption of product of a and k
    """
    return pow(a, k, public_key.nsq)
