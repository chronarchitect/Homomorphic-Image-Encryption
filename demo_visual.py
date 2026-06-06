import os
import time
from PIL import Image
import Paillier
import ImageCryptography
import numpy as np

def demo_visual():
    print("1. Generating keys...")
    public_key, private_key = Paillier.generate_keys(bitlen=128)

    print("2. Loading test image...")
    img_path = "test-images/lena512gray.bmp"
    img = Image.open(img_path).convert('L').resize((64, 64))
    
    print("3. Encrypting image...")
    cipherimg = ImageCryptography.ImgEncrypt(public_key, img)

    # --- Save using Pickle ---
    print("\n4. Saving using Pickle...")
    pickle_filename = "test_pickle.pkl"
    ImageCryptography.saveEncryptedImg(cipherimg, pickle_filename)
    pickle_path = f"encrypted-images/{pickle_filename}"
    pickle_size = os.path.getsize(pickle_path)
    print(f"Pickle size: {pickle_size / 1024:.2f} KB")

    # --- Save using Visual PNG ---
    print("5. Saving using Visual PNG...")
    visual_filename = "test_visual"
    ImageCryptography.saveVisualEncryptedImg(cipherimg, visual_filename)
    png_path = f"encrypted-images/{visual_filename}.png"
    json_path = f"encrypted-images/{visual_filename}.json"
    visual_size = os.path.getsize(png_path) + os.path.getsize(json_path)
    print(f"Visual (PNG + JSON) size: {visual_size / 1024:.2f} KB")

    print(f"\nSpace Savings: {100 * (1 - visual_size / pickle_size):.2f}%")

    # --- Load and Verify ---
    print("\n6. Loading back and verifying...")
    loaded_cipher = ImageCryptography.loadVisualEncryptedImg(visual_filename)
    
    if np.array_equal(cipherimg, loaded_cipher):
        print("Success: Loaded cipher matches original!")
    else:
        print("Error: Loaded cipher mismatch!")
        return

    print("7. Decrypting loaded image...")
    decrypted_img = ImageCryptography.ImgDecrypt(public_key, private_key, loaded_cipher)
    decrypted_img.save("demo-results/decrypted_visual.png")
    print("Decrypted image saved to demo-results/decrypted_visual.png")

    orig_pixels = np.asarray(img)
    dec_pixels = np.asarray(decrypted_img)
    if np.array_equal(orig_pixels, dec_pixels):
        print("Final Verification: Decrypted image perfectly matches original!")
    else:
        # Note: sometimes rounding or clipping in ImgDecrypt might cause 1-bit diffs, but usually it should match for grayscale
        diff = np.sum(np.abs(orig_pixels.astype(int) - dec_pixels.astype(int)))
        print(f"Final Verification: Differences found (sum of abs: {diff})")

if __name__ == "__main__":
    demo_visual()
