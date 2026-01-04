import json
import numpy as np
import pycolmap

SPARSE_DIR = "scene/colmap_output/sparse/0"
IMAGE_DIR = "scene/images"

recon = pycolmap.Reconstruction(SPARSE_DIR)

camera = next(iter(recon.cameras.values()))
w, h = camera.width, camera.height
fx, fy, cx, cy = camera.params[:4]
camera_angle_x = 2 * np.arctan(w / (2 * fx))

frames = []

for image in recon.images.values():
    pose = image.cam_from_world()   # Rigid3d object

    R = pose.rotation.matrix()    # (3, 3)
    t = pose.translation.reshape(3, 1)

    cam_from_world = np.eye(4)
    cam_from_world[:3, :3] = R
    cam_from_world[:3, 3:] = t

    c2w = np.linalg.inv(cam_from_world)

    frames.append({
        "file_path": f"{IMAGE_DIR}/{image.name}",
        "transform_matrix": c2w.tolist()
    })

out = {
    "camera_angle_x": float(camera_angle_x),
    "fl_x": float(fx),
    "fl_y": float(fy),
    "cx": float(cx),
    "cy": float(cy),
    "w": int(w),
    "h": int(h),
    "frames": frames
}

with open("transforms.json", "w") as f:
    json.dump(out, f, indent=2)

print(f"transforms.json written with {len(frames)} frames")
