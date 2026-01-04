import os
import shutil

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
SOURCE_FOLDER = "scene/images_raw"   # Where your raw photos are
TARGET_FOLDER = "images"       # Where the renamed photos will go
PREFIX = "img_"                # Output format: img_001.jpg

# -----------------------------------------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------------------------------------
def rename_dataset():
    if not os.path.exists(SOURCE_FOLDER):
        print(f"Error: Create a folder named '{SOURCE_FOLDER}' and put your photos there.")
        return

    # Create target folder
    if os.path.exists(TARGET_FOLDER):
        user_input = input(f"⚠️ Folder '{TARGET_FOLDER}' exists. Delete it? (y/n): ")
        if user_input.lower() == 'y':
            shutil.rmtree(TARGET_FOLDER)
        else:
            print("Aborting.")
            return
    os.makedirs(TARGET_FOLDER)

    # Get files
    valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(SOURCE_FOLDER) if f.lower().endswith(valid_exts)]
    
    # Sort by creation time so the sequence makes sense (walking around the object)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(SOURCE_FOLDER, x)))

    print(f"found {len(files)} images. Renaming...")

    for i, filename in enumerate(files):
        # Normalize extension
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.jpeg': ext = '.jpg'
        
        new_name = f"{PREFIX}{i+1:03d}{ext}"
        
        src_path = os.path.join(SOURCE_FOLDER, filename)
        dst_path = os.path.join(TARGET_FOLDER, new_name)
        
        shutil.copy2(src_path, dst_path)
        print(f"   {filename} -> {new_name}")

    print(f"Done! Use the '{TARGET_FOLDER}' folder for COLMAP.")

if __name__ == "__main__":
    rename_dataset()