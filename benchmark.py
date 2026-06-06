import time
import os
from PIL import Image
import Paillier
import ImageCryptography
import numpy as np

def benchmark():
    # 1. Generate keys
    print("Generating keys (128-bit)...")
    public_key, private_key = Paillier.generate_keys(bitlen=128)
    
    # 2. Load and prepare image
    img_path = "test-images/lena512gray.bmp"
    img = Image.open(img_path).convert('L')
    size = (32, 32) # Small size for quick benchmark
    img = img.resize(size)
    print(f"Image size: {size}")

    # --- Benchmark Original (Sequential) ---
    print("\nRunning Sequential Version...")
    start_time = time.time()
    # Note: We still use the optimized Encrypt function, but sequentially.
    # To truly compare with old version, we'd need to revert the math,
    # but let's compare Sequential vs Parallel with optimized math first.
    cipherimg_seq = ImageCryptography.ImgEncrypt(public_key, img, parallel=False)
    seq_encrypt_time = time.time() - start_time
    print(f"Sequential Encryption: {seq_encrypt_time:.4f}s")

    # --- Benchmark Parallel ---
    print("\nRunning Parallel Version...")
    start_time = time.time()
    cipherimg_par = ImageCryptography.ImgEncrypt(public_key, img, parallel=True)
    par_encrypt_time = time.time() - start_time
    print(f"Parallel Encryption: {par_encrypt_time:.4f}s")

    print(f"\nSpeedup: {seq_encrypt_time / par_encrypt_time:.2f}x")

    # Verify results match
    dec_seq = ImageCryptography.ImgDecrypt(public_key, private_key, cipherimg_seq, parallel=False)
    dec_par = ImageCryptography.ImgDecrypt(public_key, private_key, cipherimg_par, parallel=False)
    
    diff = np.sum(np.abs(np.asarray(dec_seq).astype(int) - np.asarray(dec_par).astype(int)))
    print(f"Result difference (sum of abs): {diff}")
    if diff == 0:
        print("Success: Sequential and Parallel results match!")
    else:
        print("Warning: Results mismatch!")

if __name__ == "__main__":
    benchmark()
