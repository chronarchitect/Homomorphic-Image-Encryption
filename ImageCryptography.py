from PIL import Image
import numpy as np
import pickle

import Paillier

def ImgEncrypt(public_key, plainimg):
    """
    args:
        public_key: Paillier PublicKey object
        plainimg: PIL Image object
        
    returns:
        cipherimg: Encryption of plainimg
    Encrypts an image
    """
    
    cipherimg = np.asarray(plainimg)
    shape = cipherimg.shape
    cipherimg = cipherimg.flatten().tolist()
    cipherimg = [Paillier.Encrypt(public_key, pix) for pix in cipherimg]
    
    return np.asarray(cipherimg).reshape(shape)


def ImgDecrypt(public_key, private_key, cipherimg):
    """
    args:
        public_key: Paillier PublicKey object
        private_key: Paillier PrivateKey object
        cipherimg: encryption of Image
        
    returns:
        Image object which is the decryption of cipherimage
    Decrypts ecnrypted image
    """
    shape = cipherimg.shape
    plainimg = cipherimg.flatten().tolist()
    plainimg = [Paillier.Decrypt(public_key, private_key, pix) for pix in plainimg]
    plainimg = [pix if pix < 255 else 255 for pix in plainimg]
    plainimg = [pix if pix > 0 else 0 for pix in plainimg]
    
    return Image.fromarray(np.asarray(plainimg).reshape(shape).astype(np.uint8))


def homomorphicBrightness(public_key, cipherimg, factor):
    """
    args:
        public_key: Paillier PublicKey object
        cipherimg: n dimensional array containing encryption of image pixels
        factor: Amount of brightness to be added (-ve for decreasing brightness)
    
    returns:
        n dimensional array containing encryption of image pixels with brightness adjusted
    
    Function to demonstrate homomorphism
    Performs brightness adjust operation on the encrypted image
    """
    shape = cipherimg.shape
    brightimg = cipherimg.flatten().tolist()
    brightimg = [Paillier.homomorphic_add_constant(public_key, pix, factor) for pix in brightimg]
    
    return np.asarray(brightimg).reshape(shape)


def saveEncryptedImg(cipherimg, filename):
    """
    args:
        cipherimg: Encryption of an image
        filename: filename to save encryption (saved under encrypted-images directory)
        
    saves Encryption of image int a file
    """
    filename = "encrypted-images/" + filename
    fstream = open(filename, "wb")
    pickle.dump(cipherimg, fstream)
    fstream.close()


def loadEncryptedImg(filename):
    """
    args:
        filename: filename of the Encrypted object under encrypted-images directory
        
    returns:
        n-dimensional array containing ecryption of image
    loads Encrypted image object from file
    """
    filename = "encrypted-images/" + filename    
    fstream = open(filename, "rb")
    cipherimg = pickle.load(fstream)
    fstream.close()
    return cipherimg
