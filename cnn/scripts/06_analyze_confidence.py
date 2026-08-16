from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image


# ============================================================
# CONFIGURATION
# ============================================================

CNN_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = CNN_DIR / "models" / "medicine_mobilenet_best.keras"
CLASS_NAMES_PATH = CNN_DIR / "models" / "class_names.txt"
TEST_DIR = CNN_DIR / "dataset" / "test"

IMAGE_SIZE = (224, 224)


# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 65)
print("CONFIDENCE ANALYSIS")
print("=" * 65)

print("\nLoading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded.")


# ============================================================
# COLLECT TEST IMAGES
# ============================================================

image_extensions = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

test_images = []

for class_index, class_name in enumerate(class_names):

    class_dir = TEST_DIR / class_name

    if not class_dir.exists():
        print(f"WARNING: Missing folder: {class_dir}")
        continue

    for file in class_dir.iterdir():

        if file.suffix in image_extensions:
            test_images.append(
                (file, class_index)
            )


print(f"\nTest images found: {len(test_images)}")


# ============================================================
# RUN PREDICTIONS
# ============================================================

results = []

print("\nAnalyzing confidence...")

for i, (image_path, true_class) in enumerate(test_images):

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

    predicted_class = int(np.argmax(predictions))
    confidence = float(predictions[predicted_class])

    correct = predicted_class == true_class

    results.append({
        "image": image_path,
        "true_class": true_class,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "correct": correct
    })

    if (i + 1) % 20 == 0:
        print(f"Processed {i + 1}/{len(test_images)}")


# ============================================================
# SEPARATE CORRECT / INCORRECT
# ============================================================

correct_results = [
    r for r in results
    if r["correct"]
]

incorrect_results = [
    r for r in results
    if not r["correct"]
]


correct_confidences = np.array([
    r["confidence"]
    for r in correct_results
])

incorrect_confidences = np.array([
    r["confidence"]
    for r in incorrect_results
])


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 65)
print("CONFIDENCE ANALYSIS RESULTS")
print("=" * 65)

print(f"\nTotal images       : {len(results)}")
print(f"Correct            : {len(correct_results)}")
print(f"Incorrect          : {len(incorrect_results)}")


if len(correct_confidences) > 0:

    print("\nCORRECT PREDICTIONS")
    print("-" * 65)

    print(
        f"Minimum confidence : "
        f"{correct_confidences.min() * 100:.2f}%"
    )

    print(
        f"Average confidence : "
        f"{correct_confidences.mean() * 100:.2f}%"
    )

    print(
        f"Median confidence  : "
        f"{np.median(correct_confidences) * 100:.2f}%"
    )

    print(
        f"Maximum confidence : "
        f"{correct_confidences.max() * 100:.2f}%"
    )


if len(incorrect_confidences) > 0:

    print("\nINCORRECT PREDICTIONS")
    print("-" * 65)

    print(
        f"Minimum confidence : "
        f"{incorrect_confidences.min() * 100:.2f}%"
    )

    print(
        f"Average confidence : "
        f"{incorrect_confidences.mean() * 100:.2f}%"
    )

    print(
        f"Maximum confidence : "
        f"{incorrect_confidences.max() * 100:.2f}%"
    )


# ============================================================
# LOW-CONFIDENCE CORRECT PREDICTIONS
# ============================================================

print("\n" + "=" * 65)
print("LOW-CONFIDENCE CORRECT PREDICTIONS")
print("=" * 65)

low_conf_correct = sorted(
    correct_results,
    key=lambda x: x["confidence"]
)

for result in low_conf_correct[:10]:

    true_name = class_names[result["true_class"]]

    print(
        f"{result['confidence'] * 100:6.2f}%  "
        f"{true_name:<40}  "
        f"{result['image'].name}"
    )


# ============================================================
# INCORRECT PREDICTIONS
# ============================================================

print("\n" + "=" * 65)
print("INCORRECT PREDICTIONS")
print("=" * 65)

for result in incorrect_results:

    true_name = class_names[result["true_class"]]
    predicted_name = class_names[result["predicted_class"]]

    print(
        f"{result['confidence'] * 100:6.2f}%  "
        f"Actual: {true_name:<35} "
        f"Predicted: {predicted_name}"
    )


print("\n" + "=" * 65)
print("ANALYSIS COMPLETE")
print("=" * 65)