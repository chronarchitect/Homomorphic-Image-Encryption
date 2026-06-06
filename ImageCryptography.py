from PIL import Image
import numpy as np
import pickle
import concurrent.futures
import multiprocessing
import os

import Paillier

def _encrypt_pixel(args):
    public_key, pix = args
    return Paillier.Encrypt(public_key, pix)

def _decrypt_pixel(args):
    public_key, private_key, pix = args
    return Paillier.Decrypt(public_key, private_key, pix)

def _brightness_pixel(args):
    public_key, pix, factor = args
    return Paillier.homomorphic_add_constant(public_key, pix, factor)

def ImgEncrypt(public_key, plainimg, parallel=True):
    """
    args:
        public_key: Paillier PublicKey object
        plainimg: PIL Image object
        parallel: Whether to use multiprocessing (default: True)
        
    returns:
        cipherimg: Encryption of plainimg
    Encrypts an image
    """
    
    cipherimg_arr = np.asarray(plainimg)
    shape = cipherimg_arr.shape
    pixels = cipherimg_arr.flatten().tolist()
    
    if parallel:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            args = [(public_key, pix) for pix in pixels]
            cipherimg = list(executor.map(_encrypt_pixel, args))
    else:
        cipherimg = [Paillier.Encrypt(public_key, pix) for pix in pixels]
    
    return np.asarray(cipherimg).reshape(shape)


def ImgDecrypt(public_key, private_key, cipherimg, parallel=True):
    """
    args:
        public_key: Paillier PublicKey object
        private_key: Paillier PrivateKey object
        cipherimg: encryption of Image
        parallel: Whether to use multiprocessing (default: True)
        
    returns:
        Image object which is the decryption of cipherimage
    Decrypts ecnrypted image
    """
    shape = cipherimg.shape
    cipher_pixels = cipherimg.flatten().tolist()
    
    if parallel:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            args = [(public_key, private_key, pix) for pix in cipher_pixels]
            plainimg = list(executor.map(_decrypt_pixel, args))
    else:
        plainimg = [Paillier.Decrypt(public_key, private_key, pix) for pix in cipher_pixels]
        
    plainimg = [pix if pix < 255 else 255 for pix in plainimg]
    plainimg = [pix if pix > 0 else 0 for pix in plainimg]
    
    return Image.fromarray(np.asarray(plainimg).reshape(shape).astype(np.uint8))


def homomorphicBrightness(public_key, cipherimg, factor, parallel=True):
    """
    args:
        public_key: Paillier PublicKey object
        cipherimg: n dimensional array containing encryption of image pixels
        factor: Amount of brightness to be added (-ve for decreasing brightness)
        parallel: Whether to use multiprocessing (default: True)
    
    returns:
        n dimensional array containing encryption of image pixels with brightness adjusted
    
    Function to demonstrate homomorphism
    Performs brightness adjust operation on the encrypted image
    """
    shape = cipherimg.shape
    bright_pixels = cipherimg.flatten().tolist()
    
    if parallel:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            args = [(public_key, pix, factor) for pix in bright_pixels]
            brightimg = list(executor.map(_brightness_pixel, args))
    else:
        brightimg = [Paillier.homomorphic_add_constant(public_key, pix, factor) for pix in bright_pixels]
    
    return np.asarray(brightimg).reshape(shape)


def saveEncryptedImg(cipherimg, filename):
    """
    args:
        cipherimg: Encryption of an image
        filename: filename to save encryption (saved under encrypted-images directory)
        
    saves Encryption of image int a file
    """
    if not os.path.exists("encrypted-images"):
        os.makedirs("encrypted-images")
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
