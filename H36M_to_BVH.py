import os
import shutil
from pathlib import Path
import cdflib

# ============================================================
# CONFIG (PATHS ONLY)
# ============================================================
PROJECT_ROOT = "/Users/srikarkodavati/Desktop/H36M-to-BVH"
BASE_BVH = os.path.join(PROJECT_ROOT, "base_H36M_hierarchy.bvh")
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "output_bvh")

SUBJECTS = [f"S{i}" for i in range(1, 12)]  # S1 ... S11
POSE_SUBDIR = os.path.join("MyPoseFeatures", "D3_Angles")

FRAME_TIME = 0.02
SKEL_SCALE = 100.0

# ============================================================
# FIXED ROTATION ORDER (UNCHANGED)
# ============================================================
ROT_ORDER = [
    [5,6,4], [32,33,31], [35,36,34], [38,39,37], [41,42,40],
    [44,45,43], [47,48,46], [50,51,49], [53,54,52], [56,57,55],
    [59,60,58], [62,63,61], [65,66,64], [68,69,67], [71,72,70],
    [74,75,73], [77,78,76],
    [20,21,19], [23,24,22], [26,27,25], [29,30,28],
    [8,9,7], [11,12,10], [14,15,13], [17,18,16]
]

# ============================================================
# CONVERT ONE SUBJECT
# ============================================================
def convert_subject(subject):
    pose_dir = os.path.join(PROJECT_ROOT, subject, POSE_SUBDIR)
    if not os.path.isdir(pose_dir):
        print(f"[SKIP] {subject}: missing D3_Angles")
        return

    out_dir = os.path.join(OUTPUT_ROOT, subject)
    os.makedirs(out_dir, exist_ok=True)

    for cdf_path in sorted(Path(pose_dir).glob("*.cdf")):
        cdf = cdflib.CDF(cdf_path)
        angles = cdf.varget("Pose")

        action = cdf_path.stem.replace(" ", "_")
        out_bvh = os.path.join(out_dir, f"{action}.bvh")

        shutil.copy(BASE_BVH, out_bvh)

        with open(out_bvh, "a") as f:
            f.write("\nMOTION\n")
            f.write(f"Frames: {len(angles)}\n")
            f.write(f"Frame Time: {FRAME_TIME}\n")

            for frame in angles:
                # ROOT TRANSLATION (Option B: index only)
                xp = frame[0][0] / SKEL_SCALE
                yp = frame[1][0] / SKEL_SCALE
                zp = frame[2][0] / SKEL_SCALE
                f.write(f"{xp} {yp} {zp} ")

                # ROTATIONS (Option B: index only)
                for r in ROT_ORDER:
                    zr = frame[r[2] - 1][0]
                    xr = frame[r[0] - 1][0]
                    yr = frame[r[1] - 1][0]
                    f.write(f"{zr} {xr} {yr} ")

                f.write("\n")

        print(f"[OK] {subject} → {action}.bvh")

# ============================================================
# MAIN
# ============================================================
def main():
    if not os.path.isfile(BASE_BVH):
        raise FileNotFoundError("base_H36M_hierarchy.bvh not found")

    os.makedirs(OUTPUT_ROOT, exist_ok=True)

    for subject in SUBJECTS:
        convert_subject(subject)

    print("✔ Finished converting S1–S11")

if __name__ == "__main__":
    main()
