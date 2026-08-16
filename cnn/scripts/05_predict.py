from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image


# ============================================================
# CONFIGURATION
# ============================================================
# cnn/ directory
CNN_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = CNN_DIR / "models" / "medicine_mobilenet_best.keras"
CLASS_NAMES_PATH = CNN_DIR / "models" / "class_names.txt"

IMAGE_SIZE = (224, 224)

# Temporary threshold.
# We will tune this properly after testing.
UNKNOWN_THRESHOLD = 0.00


# ============================================================
# LOAD CLASS NAMES
# ============================================================

print("=" * 60)
print("MEDICINE CNN - IMAGE PREDICTION")
print("=" * 60)

print("\nLoading class names...")

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    CLASS_NAMES = [line.strip() for line in f if line.strip()]

print(f"Loaded {len(CLASS_NAMES)} classes.")


# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# GET IMAGE
# ============================================================

image_path = input("\nEnter path to medicine image: ").strip()
image_path = Path(image_path)

if not image_path.exists():
    print("\nERROR: Image file not found.")
    print(f"Path checked: {image_path}")
    exit()


# ============================================================
# PREPROCESS IMAGE
# ============================================================

print("\nProcessing image...")

img = image.load_img(
    image_path,
    target_size=IMAGE_SIZE
)

img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)



# ============================================================
# PREDICTION
# ============================================================

print("Running prediction...")

predictions = model.predict(img_array, verbose=0)[0]

top_indices = np.argsort(predictions)[::-1][:3]

best_index = top_indices[0]
best_confidence = float(predictions[best_index])


# ============================================================
# UNKNOWN DETECTION
# ============================================================

if best_confidence < UNKNOWN_THRESHOLD:
    predicted_medicine = "UNKNOWN MEDICINE"
else:
    predicted_medicine = CLASS_NAMES[best_index]


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)
print("PREDICTION RESULT")
print("=" * 60)

print(f"\nPrediction  : {predicted_medicine}")
print(f"Confidence  : {best_confidence * 100:.2f}%")

print("\nTop 3 CNN Predictions:")
print("-" * 60)

for rank, index in enumerate(top_indices, start=1):
    print(
        f"{rank}. {CLASS_NAMES[index]:40s}"
        f"{predictions[index] * 100:.2f}%"
    )

print("=" * 60)