import os
from PIL import Image
import Paillier
import ImageCryptography
import numpy as np

def demo():
    # 1. Generate keys
    print("Generating keys...")
    public_key, private_key = Paillier.generate_keys(bitlen=128)
    print("Keys generated.")

    # 2. Load a test image
    img_path = "test-images/lena512gray.bmp"
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found.")
        return
    
    print(f"Loading image {img_path}...")
    img = Image.open(img_path).convert('L') # Ensure it's grayscale for simplicity
    img = img.resize((64, 64)) # Resize to speed up encryption for demo
    print(f"Image loaded and resized to 64x64.")

    # 3. Encrypt the image
    print("Encrypting image (this might take a while)...")
    cipherimg = ImageCryptography.ImgEncrypt(public_key, img)
    print("Image encrypted.")

    # 4. Perform homomorphic brightness adjustment
    brightness_factor = 50
    print(f"Adjusting brightness homomorphically by {brightness_factor}...")
    bright_cipherimg = ImageCryptography.homomorphicBrightness(public_key, cipherimg, brightness_factor)
    print("Brightness adjusted.")

    # 5. Decrypt the images
    print("Decrypting original encrypted image...")
    decrypted_img = ImageCryptography.ImgDecrypt(public_key, private_key, cipherimg)
    
    print("Decrypting brightness-adjusted image...")
    decrypted_bright_img = ImageCryptography.ImgDecrypt(public_key, private_key, bright_cipherimg)

    # 6. Save results
    if not os.path.exists("demo-results"):
        os.makedirs("demo-results")
    
    decrypted_img.save("demo-results/decrypted_original.png")
    decrypted_bright_img.save("demo-results/decrypted_bright.png")
    print("Results saved in demo-results/ folder.")

    # 7. Verify some pixel values
    orig_pixels = np.asarray(img)
    dec_pixels = np.asarray(decrypted_img)
    dec_bright_pixels = np.asarray(decrypted_bright_img)

    print("\nVerification:")
    print(f"Original pixel [0,0]: {orig_pixels[0,0]}")
    print(f"Decrypted pixel [0,0]: {dec_pixels[0,0]}")
    print(f"Decrypted bright pixel [0,0]: {dec_bright_pixels[0,0]} (Expected around {orig_pixels[0,0] + brightness_factor})")

if __name__ == "__main__":
    demo()
