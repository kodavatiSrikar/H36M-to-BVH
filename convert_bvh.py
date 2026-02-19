# import cdflib
# import os
# import shutil
# from pathlib import Path

# # ============================================================
# # CONFIG
# # ============================================================
# PROJECT_ROOT = "/Users/srikarkodavati/Desktop/H36M-to-BVH"
# BASE_BVH = os.path.join(PROJECT_ROOT, "base_H36M_hierarchy.bvh")
# OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "output_bvh")

# SUBJECTS = [f"S{i}" for i in range(1, 12)]  # S1–S11
# POSE_SUBDIR = os.path.join("MyPoseFeatures", "D3_Angles")

# FRAME_TIME = 0.02
# SKEL_SCALE = 100.0

# ROT_ORDER = [
#     [5,6,4], [32,33,31], [35,36,34], [38,39,37], [41,42,40],
#     [44,45,43], [47,48,46], [50,51,49], [53,54,52], [56,57,55],
#     [59,60,58], [62,63,61], [65,66,64], [68,69,67], [71,72,70],
#     [74,75,73], [77,78,76],
#     [20,21,19], [23,24,22], [26,27,25], [29,30,28],
#     [8,9,7], [11,12,10], [14,15,13], [17,18,16]
# ]

# # ============================================================
# # CONVERT ONE SUBJECT (LOGIC UNCHANGED)
# # ============================================================
# def convert_subject(subject):
#     pose_dir = os.path.join(PROJECT_ROOT, subject, POSE_SUBDIR)
#     if not os.path.isdir(pose_dir):
#         print(f"[SKIP] {subject}: no D3_Angles")
#         return

#     out_dir = os.path.join(OUTPUT_ROOT, subject)
#     os.makedirs(out_dir, exist_ok=True)

#     for pose in sorted(Path(pose_dir).glob("*.cdf")):
#         cdf_angles = cdflib.CDF(pose)
#         angles = cdf_angles.varget("Pose")[0]   # 🔑 SAME AS WORKING SCRIPT

#         frames = len(angles)
#         action = pose.stem.replace(" ", "_")

#         out_bvh = os.path.join(out_dir, f"{action}.bvh")

#         shutil.copy(BASE_BVH, out_bvh)

#         with open(out_bvh, "a") as file:
#             file.write("\nMOTION \n")
#             file.write("Frames:\t" + str(frames) + " \n")
#             file.write("Frame Time: " + str(FRAME_TIME) + " \n")

#             for frame in angles:
#                 xp = frame[0] / SKEL_SCALE
#                 yp = frame[1] / SKEL_SCALE
#                 zp = frame[2] / SKEL_SCALE
#                 file.write(f"{xp} {yp} {zp} ")

#                 for r in ROT_ORDER:
#                     zr = frame[r[2] - 1]
#                     xr = frame[r[0] - 1]
#                     yr = frame[r[1] - 1]
#                     file.write(f"{zr} {xr} {yr} ")

#                 file.write("\n")

#         print(f"[OK] {subject} → {action}.bvh")

# # ============================================================
# # MAIN
# # ============================================================
# def main():
#     if not os.path.isfile(BASE_BVH):
#         raise FileNotFoundError("base_H36M_hierarchy.bvh not found")

#     os.makedirs(OUTPUT_ROOT, exist_ok=True)

#     for subject in SUBJECTS:
#         convert_subject(subject)

#     print("✔ Done converting S1–S11")

# if __name__ == "__main__":
#     main()



import cdflib
import os
import shutil
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================
PROJECT_ROOT = "/Users/srikarkodavati/Desktop/H36M-to-BVH"
BASE_BVH = os.path.join(PROJECT_ROOT, "base_H36M_hierarchy.bvh")
OUTPUT_ROOT = os.path.join(PROJECT_ROOT, "output_bvh")

SUBJECTS = [f"S{i}" for i in range(1, 12)]  # S1–S11
POSE_SUBDIR = os.path.join("MyPoseFeatures", "D3_Angles")

FRAME_TIME = 0.02
SKEL_SCALE = 100.0

# BVH joint rotation order (UNCHANGED)
ROT_ORDER = [
    [5,6,4], [32,33,31], [35,36,34], [38,39,37], [41,42,40],
    [44,45,43], [47,48,46], [50,51,49], [53,54,52], [56,57,55],
    [59,60,58], [62,63,61], [65,66,64], [68,69,67], [71,72,70],
    [74,75,73], [77,78,76],
    [20,21,19], [23,24,22], [26,27,25], [29,30,28],
    [8,9,7], [11,12,10], [14,15,13], [17,18,16]
]

# ============================================================
# CONVERT ONE SUBJECT (LOGIC PRESERVED)
# ============================================================
def convert_subject(subject):
    pose_dir = os.path.join(PROJECT_ROOT, subject, POSE_SUBDIR)
    if not os.path.isdir(pose_dir):
        print(f"[SKIP] {subject}: no D3_Angles")
        return

    out_dir = os.path.join(OUTPUT_ROOT, subject)
    os.makedirs(out_dir, exist_ok=True)

    for pose in sorted(Path(pose_dir).glob("*.cdf")):
        cdf_angles = cdflib.CDF(pose)
        angles = cdf_angles.varget("Pose")[0]

        frames = len(angles)
        action = pose.stem.replace(" ", "_")
        out_bvh = os.path.join(out_dir, f"{action}.bvh")

        shutil.copy(BASE_BVH, out_bvh)

        with open(out_bvh, "a") as file:
            file.write("\nMOTION\n")
            file.write(f"Frames:\t{frames}\n")
            file.write(f"Frame Time: {FRAME_TIME}\n")

            for frame in angles:
                # Root translation
                xp = frame[0] / SKEL_SCALE
                yp = frame[1] / SKEL_SCALE
                zp = frame[2] / SKEL_SCALE

                # Root rotation (FIX: rotate -90° around X)
                root_x = frame[3] - 90.0
                root_y = frame[4]
                root_z = frame[5]

                file.write(f"{xp} {yp} {zp} ")
                file.write(f"{root_x} {root_y} {root_z} ")

                # Joint rotations (UNCHANGED)
                for r in ROT_ORDER[1:]:
                    zr = frame[r[2] - 1]
                    xr = frame[r[0] - 1]
                    yr = frame[r[1] - 1]
                    file.write(f"{zr} {xr} {yr} ")

                file.write("\n")

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

    print("✔ Done converting S1–S11")

if __name__ == "__main__":
    main()
