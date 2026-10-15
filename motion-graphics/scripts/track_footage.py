#!/usr/bin/env python3
"""Real tracking data for footage HUDs: MediaPipe hand landmarks and/or object boxes, sampled at 30 fps.

    python3 track_footage.py hands   out/sdr.mp4 assets/track.json
    python3 track_footage.py objects out/sdr.mp4 assets/obj.json [--allow "laptop,cell phone,cup,chair,dining table"]

hands.json   {"fps":30,"frames":[[{"lr":"Left","s":0.93,"p":[[x,y,z]×21]}…]…]}   x,y normalised 0..1
objects.json {"fps":30,"frames":[[[class,score,x,y,w,h]…]…]}                      pixels in 1920×1080 space

Setup (once):  pip install mediapipe   (if import fails with libEGL: apt-get install -y libegl1 libgles2)
Models download automatically to ~/.cache/motion-graphics/ on first use.
Use the SDR proxy (prep_footage.sh) as input. Detection on HDR frames is noticeably worse.
Privacy default: do not allow "person". Label hands and objects, not bystanders.
"""
import json, os, subprocess, sys, urllib.request
import numpy as np

MODELS = {"hands": "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task",
          "objects": "https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite2/float32/latest/efficientdet_lite2.tflite"}
mode, src, out = sys.argv[1], sys.argv[2], sys.argv[3]
allow = sys.argv[sys.argv.index("--allow") + 1].split(",") if "--allow" in sys.argv else ["laptop", "cell phone", "cup", "bottle", "chair", "dining table", "keyboard", "tv", "book", "backpack"]
cache = os.path.expanduser("~/.cache/motion-graphics"); os.makedirs(cache, exist_ok=True)
model = os.path.join(cache, os.path.basename(MODELS[mode]))
if not os.path.exists(model):
    print("downloading", MODELS[mode]); urllib.request.urlretrieve(MODELS[mode], model)

import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

W, H, FPS = 960, 540, 30
if mode == "hands":
    det = vision.HandLandmarker.create_from_options(vision.HandLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=model),
          running_mode=vision.RunningMode.VIDEO, num_hands=2, min_hand_detection_confidence=.35, min_hand_presence_confidence=.35, min_tracking_confidence=.35))
else:
    det = vision.ObjectDetector.create_from_options(vision.ObjectDetectorOptions(base_options=mpt.BaseOptions(model_asset_path=model),
          running_mode=vision.RunningMode.VIDEO, max_results=12, score_threshold=.25, category_allowlist=allow))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
frames, i = [], 0
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.frombuffer(buf, np.uint8).reshape(H, W, 3)); ts = int(i * 1000 / FPS)
    if mode == "hands":
        r = det.detect_for_video(img, ts)
        frames.append([{"lr": r.handedness[k][0].category_name, "s": round(r.handedness[k][0].score, 3), "p": [[round(q.x, 4), round(q.y, 4), round(q.z, 4)] for q in h]} for k, h in enumerate(r.hand_landmarks)])
    else:
        r = det.detect_for_video(img, ts)
        frames.append([[d.categories[0].category_name, round(d.categories[0].score, 3), d.bounding_box.origin_x * 2, d.bounding_box.origin_y * 2, d.bounding_box.width * 2, d.bounding_box.height * 2] for d in r.detections])
    i += 1
json.dump({"fps": FPS, "frames": frames}, open(out, "w"))
cov = "".join("#" if f else "." for f in frames)
print(f"{i} frames, {sum(1 for f in frames if f)} with detections → {out}")
print("coverage (1 char = 1/30 s, 60 per row):"); print("\n".join(cov[k:k + 60] for k in range(0, len(cov), 60)))
sys.stdout.flush(); os._exit(0)   # mediapipe can crash in its own shutdown handler; data is already written
