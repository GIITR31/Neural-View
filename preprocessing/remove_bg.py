import os
from rembg import remove
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
INPUT_DIR = "scene/images"           # The folder created by the rename script
OUTPUT_DIR = "scene/images_clean"    # Where transparent PNGs go

# -----------------------------------------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------------------------------------
def process_file(filename):
    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".png")
    
    print(f"Processing: {filename}...")
    
    try:
        with open(input_path, 'rb') as i:
            input_data = i.read()
            subject = remove(input_data)
            
        with open(output_path, 'wb') as o:
            o.write(subject)
            
    except Exception as e:
        print(f"Failed on {filename}: {e}")

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Error: '{INPUT_DIR}' folder not found. Run the rename script first.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    print(f"Removing backgrounds from {len(files)} images...")
    
    # Process in parallel to be faster
    with ThreadPoolExecutor() as executor:
        executor.map(process_file, files)

    print(f"Clean images are in '{OUTPUT_DIR}'")

if __name__ == "__main__":
    main()