import os
import json
import shutil
import numpy as np
from pathlib import Path
import pycolmap

IMG_DIR = Path("scene/images")     # your images path 
COLMAP_DIR = Path("scene/colmap_output")
DB_PATH = COLMAP_DIR / "database.db"
SPARSE_DIR = COLMAP_DIR / "sparse"





def qvec2rotmat(qvec):
    w, x, y, z = qvec
    return np.array([
        [1 - 2*y*y - 2*z*z, 2*x*y - 2*z*w,     2*x*z + 2*y*w],
        [2*x*y + 2*z*w,     1 - 2*x*x - 2*z*z, 2*y*z - 2*x*w],
        [2*x*z - 2*y*w,     2*y*z + 2*x*w,     1 - 2*x*x - 2*y*y]
    ])


if COLMAP_DIR.exists():
    shutil.rmtree(COLMAP_DIR)
COLMAP_DIR.mkdir(parents=True)

print("Extracting features...")
pycolmap.extract_features(
    database_path=DB_PATH,
    image_path=IMG_DIR,
    camera_model="SIMPLE_RADIAL"
)

print("Matching features (exhaustive)...")
pycolmap.match_exhaustive(
    database_path=DB_PATH
)

print("Running incremental SfM...")
reconstructions = pycolmap.incremental_mapping(
    database_path=DB_PATH,
    image_path=IMG_DIR,
    output_path=SPARSE_DIR
)

recon = max(reconstructions.values(), key=lambda r: len(r.images))
print(f"Registered images: {len(recon.images)}")
print(f"sparse points: {len(recon.points3D)}")

ply_path = SPARSE_DIR / "points.ply"
recon.export_PLY(str(ply_path))
print(f"Sparse point cloud saved: {ply_path}")


