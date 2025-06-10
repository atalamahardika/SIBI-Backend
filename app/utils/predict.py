import tensorflow as tf
import numpy as np
from PIL import Image
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import datetime

# === Load Model ===
model_path = os.path.join(os.path.dirname(__file__), '../model/resnet.keras')
model = tf.keras.models.load_model(model_path)

# === Label klasifikasi ===
labels = [chr(i) for i in range(97, 123)]  # a-z

# === Setup MediaPipe ===
base_options = python.BaseOptions(model_asset_path=os.path.join(os.path.dirname(__file__), 'hand_landmarker.task'))
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    running_mode=vision.RunningMode.IMAGE
)
detector = vision.HandLandmarker.create_from_options(options)

# === Lokasi penyimpanan gambar ===
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMAGES_DIR = os.path.join(ROOT_DIR, 'images')
RAW_DIR = os.path.join(IMAGES_DIR, 'raw')
PREPROCESS_DIR = os.path.join(IMAGES_DIR, 'preprocess')

# Buat semua folder jika belum ada
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PREPROCESS_DIR, exist_ok=True)

def preprocess_image(image: Image.Image):
    # Simpan gambar asli
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    original_path = os.path.join(RAW_DIR, f"original_{timestamp}.jpg")
    image.save(original_path)

    # Konversi ke np.array
    image_np = np.array(image)
    h, w = image_np.shape[:2]

    # Konversi ke MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_np)

    # Deteksi tangan
    detection_result = detector.detect(mp_image)
    if not detection_result.hand_landmarks:
        raise ValueError("Tangan tidak terdeteksi.")

    # ROI dari landmark
    landmarks = detection_result.hand_landmarks[0]
    x_list = [lm.x * w for lm in landmarks]
    y_list = [lm.y * h for lm in landmarks]
    xmin, xmax = int(min(x_list)), int(max(x_list))
    ymin, ymax = int(min(y_list)), int(max(y_list))

    # Tambahkan margin
    margin = 20
    xmin = max(0, xmin - margin)
    ymin = max(0, ymin - margin)
    xmax = min(w, xmax + margin)
    ymax = min(h, ymax + margin)

    # Crop ROI dan resize
    hand_roi = image_np[ymin:ymax, xmin:xmax]
    hand_pil = Image.fromarray(hand_roi)
    resized = hand_pil.resize((224, 224))

    # Simpan gambar hasil preprocessing
    processed_path = os.path.join(PREPROCESS_DIR, f"processed_{timestamp}.jpg")
    resized.save(processed_path)

    # Preprocessing untuk model
    image_array = tf.keras.preprocessing.image.img_to_array(resized)
    image_array = tf.expand_dims(image_array, 0)  # (1, 224, 224, 3)
    image_array = tf.keras.applications.resnet50.preprocess_input(image_array)
    # image_array = image_array / 255.0 # Manual
    return image_array

def predict_image(image: Image.Image):
    processed = preprocess_image(image)
    prediction = model.predict(processed)
    predicted_class = np.argmax(prediction, axis=1)[0]
    return labels[predicted_class]
