from pathlib import Path

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ============================================================
# CONFIGURATION
# ============================================================
CNN_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = CNN_DIR / "models" / "medicine_mobilenet_best.keras"
TEST_DIR = CNN_DIR / "dataset" / "test"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16


# ============================================================
# LOAD MODEL
# ============================================================

print("=" * 60)
print("MEDICINE CNN - MODEL EVALUATION")
print("=" * 60)

print("\nLoading model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully.")


# ============================================================
# LOAD TEST DATASET
# ============================================================

print("\nLoading test dataset...")

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
    shuffle=False
)

class_names = test_ds.class_names
num_classes = len(class_names)

print(f"\nNumber of classes: {num_classes}")

for i, name in enumerate(class_names):
    print(f"{i:2d}: {name}")


# ============================================================
# MODEL EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("TEST SET EVALUATION")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(
    test_ds,
    verbose=1
)

print(f"\nTest Loss     : {test_loss:.4f}")
print(f"Test Accuracy : {test_accuracy:.4f}")
print(f"Test Accuracy : {test_accuracy * 100:.2f}%")


# ============================================================
# GET TRUE LABELS AND PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

y_true = []
y_pred = []

for images, labels in test_ds:

    predictions = model.predict(
        images,
        verbose=0
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1
    )

    y_true.extend(np.argmax(labels.numpy(), axis=1))
    y_pred.extend(predicted_classes)


y_true = np.array(y_true)
y_pred = np.array(y_pred)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

report = classification_report(
    y_true,
    y_pred,
    target_names=class_names,
    digits=4,
    zero_division=0
)

print(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

print("Generating confusion matrix...")

cm = confusion_matrix(
    y_true,
    y_pred
)

fig, ax = plt.subplots(
    figsize=(16, 14)
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=class_names
)

disp.plot(
    ax=ax,
    xticks_rotation=90,
    cmap="Blues",
    colorbar=False
)

plt.title("Medicine Classification - Confusion Matrix")
plt.tight_layout()

output_path = Path("models/confusion_matrix.png")

plt.savefig(
    output_path,
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print(f"\nConfusion matrix saved to:")
print(output_path)


# ============================================================
# WRONG PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("MISCLASSIFICATION SUMMARY")
print("=" * 60)

wrong = np.where(y_true != y_pred)[0]

print(f"\nIncorrect predictions: {len(wrong)}")
print(f"Correct predictions:   {len(y_true) - len(wrong)}")

if len(wrong) > 0:

    print("\nSome incorrect predictions:")

    for index in wrong[:20]:

        actual = class_names[y_true[index]]
        predicted = class_names[y_pred[index]]

        print(
            f"Actual: {actual:<40} "
            f"Predicted: {predicted}"
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)

print(f"Classes evaluated : {num_classes}")
print(f"Test images       : {len(y_true)}")
print(f"Correct           : {len(y_true) - len(wrong)}")
print(f"Incorrect         : {len(wrong)}")
print(f"Accuracy          : {test_accuracy * 100:.2f}%")

print("=" * 60)