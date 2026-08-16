from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image


# ============================================================
# CONFIGURATION
# ============================================================

CNN_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = CNN_DIR / "models" / "medicine_mobilenet_best.keras"
UNKNOWN_DIR = CNN_DIR / "dataset" / "unknown_test"

IMAGE_SIZE = (224, 224)

# Keep this at 0 while we analyze the model.
UNKNOWN_THRESHOLD = 0.0


# ============================================================
# CLASS NAMES
# ============================================================

# These MUST be in the same order used during training.
CLASS_NAMES = [
    "Acretin 30 g cream",
    "All-Vent 125 ml syrup",
    "Augmentin 14 tablets",
    "B.B.C. 25 ml spray solution",
    "Betaderm 30  gm cream",
    "Bronchopro 100 ml syrup",
    "Brufen 30 tablets",
    "Cataflam 20 tablets",
    "Comfort Massage Gel 50 gm gel",
    "Congestal 20 tablets",
    "Diclac 30  gm gel",
    "Flagyl 20 tablets",
    "Frost 100 ml spray",
    "Fucidin 20 g cream",
    "Glucophage 50 tablets",
    "Pandermal 15 g cream",
    "Paramol 20 tablets",
    "Reparil-Gel N 40 g gel",
    "Tentavair 160 mcg oral inhalation",
    "Visceralgine 120 ml syrup",
    "Zantac 20 tablets",
]


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 70)
print("MEDICINE CNN - UNKNOWN MEDICINE TEST")
print("=" * 70)

print("\nLoading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# FIND IMAGES
# ============================================================

extensions = {
    ".jpg",
    ".jpeg",
    ".png",
    ".JPG",
    ".JPEG",
    ".PNG"
}

image_paths = sorted(
    [
        p
        for p in UNKNOWN_DIR.iterdir()
        if p.suffix in extensions
    ]
)

print(f"\nUnknown images found: {len(image_paths)}")


# ============================================================
# PREDICT
# ============================================================

print("\n" + "=" * 70)
print("PREDICTIONS")
print("=" * 70)

results = []

for image_path in image_paths:

    # Load image
    img = image.load_img(
        image_path,
        target_size=IMAGE_SIZE
    )

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    # IMPORTANT:
    # Do NOT divide by 255.
    # MobileNetV2 preprocessing is already inside the model.

    predictions = model.predict(
        img_array,
        verbose=0
    )[0]

    # Get top 3 classes
    top_indices = np.argsort(predictions)[::-1][:3]

    top1_index = top_indices[0]
    top2_index = top_indices[1]

    top1_confidence = float(predictions[top1_index])
    top2_confidence = float(predictions[top2_index])

    margin = top1_confidence - top2_confidence

    top1_name = CLASS_NAMES[top1_index]

    # Current threshold is 0, so this will always show
    # the CNN prediction. We are analyzing first.
    if top1_confidence >= UNKNOWN_THRESHOLD:
        prediction = top1_name
    else:
        prediction = "UNKNOWN MEDICINE"

    print("\n" + "-" * 70)

    print(f"Image      : {image_path.name}")
    print(f"Prediction : {prediction}")
    print(f"Confidence : {top1_confidence * 100:.2f}%")
    print(f"Margin     : {margin * 100:.2f}%")

    print("\nTop 3 Predictions:")

    for rank, index in enumerate(top_indices, start=1):

        print(
            f"{rank}. "
            f"{CLASS_NAMES[index]:<40} "
            f"{predictions[index] * 100:.2f}%"
        )

    results.append({
        "image": image_path.name,
        "prediction": top1_name,
        "confidence": top1_confidence,
        "margin": margin
    })


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("UNKNOWN DATASET SUMMARY")
print("=" * 70)

confidences = np.array([
    r["confidence"]
    for r in results
])

margins = np.array([
    r["margin"]
    for r in results
])

print(f"\nImages tested       : {len(results)}")

if len(results) > 0:

    print(
        f"Average confidence : "
        f"{confidences.mean() * 100:.2f}%"
    )

    print(
        f"Minimum confidence : "
        f"{confidences.min() * 100:.2f}%"
    )

    print(
        f"Maximum confidence : "
        f"{confidences.max() * 100:.2f}%"
    )

    print(
        f"Average top-1/top-2 margin : "
        f"{margins.mean() * 100:.2f}%"
    )

    print(
        f"Minimum margin             : "
        f"{margins.min() * 100:.2f}%"
    )

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)