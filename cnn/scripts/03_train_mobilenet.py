from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# ============================================================
# CONFIGURATION
# ============================================================
CNN_DIR = Path(__file__).resolve().parent.parent

TRAIN_DIR = CNN_DIR / "dataset" / "train"
VAL_DIR = CNN_DIR / "dataset" / "val"
MODEL_DIR = CNN_DIR / "models"

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

INITIAL_EPOCHS = 15
FINE_TUNE_EPOCHS = 15

SEED = 42


# ============================================================
# GPU CHECK
# ============================================================

print("=" * 60)
print("MEDICINE CNN TRAINING")
print("=" * 60)

gpus = tf.config.list_physical_devices("GPU")

if gpus:
    print(f"GPU detected: {gpus}")
else:
    print("No GPU detected. Training will use CPU.")

print(f"TensorFlow version: {tf.__version__}")


# ============================================================
# LOAD DATASETS
# ============================================================

print("\nLoading training dataset...")

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
    shuffle=True,
    seed=SEED
)

print("Loading validation dataset...")

val_ds = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical",
    shuffle=False
)


class_names = train_ds.class_names
NUM_CLASSES = len(class_names)

print("\nClasses:")
for i, name in enumerate(class_names):
    print(f"{i:2d}: {name}")

print(f"\nNumber of classes: {NUM_CLASSES}")


# ============================================================
# PERFORMANCE OPTIMIZATION
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)


# ============================================================
# DATA AUGMENTATION
# ============================================================

data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.10),
        layers.RandomTranslation(0.10, 0.10),
        layers.RandomContrast(0.10),
    ],
    name="data_augmentation"
)


# ============================================================
# LOAD PRETRAINED MOBILENETV2
# ============================================================

print("\nLoading MobileNetV2 pretrained on ImageNet...")

base_model = MobileNetV2(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers initially
base_model.trainable = False


# ============================================================
# BUILD MODEL
# ============================================================

inputs = keras.Input(shape=IMG_SIZE + (3,))

x = data_augmentation(inputs)

x = preprocess_input(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.4)(x)

outputs = layers.Dense(
    NUM_CLASSES,
    activation="softmax"
)(x)

model = keras.Model(inputs, outputs)


# ============================================================
# COMPILE MODEL
# ============================================================

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


print("\nModel summary:")
model.summary()


# ============================================================
# CALLBACKS
# ============================================================

checkpoint_path = MODEL_DIR / "medicine_mobilenet_best.keras"

callbacks = [

    keras.callbacks.ModelCheckpoint(
        checkpoint_path,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    ),

    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),

    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.3,
        patience=2,
        min_lr=1e-7,
        verbose=1
    )
]


# ============================================================
# PHASE 1 — TRAIN CLASSIFICATION HEAD
# ============================================================

print("\n" + "=" * 60)
print("PHASE 1: TRAINING CLASSIFICATION HEAD")
print("=" * 60)

history_initial = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=INITIAL_EPOCHS,
    callbacks=callbacks
)


# ============================================================
# PHASE 2 — FINE-TUNING
# ============================================================

print("\n" + "=" * 60)
print("PHASE 2: FINE-TUNING MOBILENETV2")
print("=" * 60)

base_model.trainable = True

# Freeze the earlier layers.
# Only the last ~30 layers will be fine-tuned.

for layer in base_model.layers[:-30]:
    layer.trainable = False


model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=1e-5
    ),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


history_fine = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=callbacks
)


# ============================================================
# SAVE FINAL MODEL
# ============================================================

final_model_path = MODEL_DIR / "medicine_mobilenet_final.keras"

model.save(final_model_path)


# ============================================================
# SAVE CLASS NAMES
# ============================================================

classes_path = MODEL_DIR / "class_names.txt"

with open(classes_path, "w", encoding="utf-8") as f:
    for class_name in class_names:
        f.write(class_name + "\n")


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(f"Final model: {final_model_path}")
print(f"Best model:  {checkpoint_path}")
print(f"Classes:     {classes_path}")

print("\nClasses:")
for name in class_names:
    print(f"  - {name}")

print("=" * 60)