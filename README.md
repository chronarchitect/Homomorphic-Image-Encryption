# Secure Outsourcing of Image Editing Based on Homomorphic Encryption

### Problem Definition
Various cloud storage services now provide some basic image editing functionalities as well. Considering an image may disclose private information about the user and most coud based services provide free tier plans. The security threats faced by the user primarily from

1. malicious behaviour of the cloud where the cloud server may be interested to learn the private information contained in the images
2. an attacker gains access to the server and by extension all the images stored in it.

### Proposed Solution

We construct an image encryption and editing model based on homomorphic encryption. The idea of homomorphic computation is to perform operations on an encrypted ciphertext and the result would be the same as performing the operations on the plaintexts. <br/>
In our implementaion we extend Paillier's Homomorphic Encryption (PHE) scheme to operate over images. The Paillier cryptosystem is an additive homomorphic and probabilistic asymmetric encryption scheme. It is only partially homomorphic as it can only add encrypted ciphertexts or multiply an encrypted ciphertext by a plaintext. <br/>
The homomorphic properties of this cryptosystem is demonstrated by applying a brightness adjustment transform over the encrypted image.

#### Implementing PHE

We implement PHE and then extend it for images. To generate secure keys we require large primes. In our implementation we use the Rabin-Miller primality test to generate probabilistic primes of a given bit length. <br/>
All of the mathematics required for Paillier Cryptosystem and Rabin-Miller test are defined inside `ModularArithmetic.py` <br/>
`ModularArithmetic` and `RabinMiller` are prerequisites used by `Paillier.py`. <br/>
To use our implementation of PHE there are no dependecies as everything has been implemented from scratch. Simply import the file
```
import Paillier
```

#### Extending PHE for Image Cryptography

The `ImageCryptography` module depends on two other modules which can be installed through `pip` namely `Python Imaging Library (PIL)` and `numpy`. <br/>
To use this make sure the dependencies are met and <br/>
```
import Paillier
import ImageCryptography
```
 The Paillier module is used for generating keys here.
To extend Paillier for image encryption, we use the `Paillier.Encrypt` function to encrypt each pixel in our image, the image decryption function behaves similarly. <br/>
To show homomorphic image editing is possible, we have implemented a simple brightness function which makes use of Paillier's homomorphic constant addition to add a brightness factor to each pixel of the encrypted image. <br/>
In order to store encrypted image objects we use the built-in python module `pickle` which serialises the encrypted image object and stores it as a file.

#### Developers
* [Aniket Das](https://github.com/chronarchitect)
* [Akarsh Srivastava](https://github.com/heisenberg42) 
* Kanishka Gupta
* [Somdatta Mukherjee](https://github.com/SomdattaMukherjee/)
