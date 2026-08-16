from pathlib import Path
import random
import shutil

# =========================
# CONFIGURATION
# =========================

CNN_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = CNN_DIR / "dataset" / "raw"
TRAIN_DIR = CNN_DIR / "dataset" / "train"
VAL_DIR = CNN_DIR / "dataset" / "val"
TEST_DIR = CNN_DIR / "dataset" / "test"

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}


# =========================
# SET RANDOM SEED
# =========================

random.seed(SEED)


# =========================
# CHECK RATIOS
# =========================

assert abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) < 1e-6


# =========================
# GET CLASSES
# =========================

classes = sorted([
    folder for folder in RAW_DIR.iterdir()
    if folder.is_dir()
])

if not classes:
    raise RuntimeError(f"No class folders found in {RAW_DIR}")


print("=" * 60)
print("MEDICINE DATASET SPLITTING")
print("=" * 60)

print(f"Classes found: {len(classes)}")
print(f"Train ratio:   {TRAIN_RATIO}")
print(f"Validation:    {VAL_RATIO}")
print(f"Test ratio:    {TEST_RATIO}")
print(f"Random seed:   {SEED}")
print("=" * 60)


# =========================
# CREATE DIRECTORIES
# =========================

for directory in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# =========================
# SPLIT EACH CLASS
# =========================

total_train = 0
total_val = 0
total_test = 0

for class_dir in classes:

    images = [
        image for image in class_dir.iterdir()
        if image.is_file()
        and image.suffix in IMAGE_EXTENSIONS
    ]

    # Shuffle images
    random.shuffle(images)

    total_images = len(images)

    if total_images == 0:
        print(f"WARNING: {class_dir.name} contains no images.")
        continue

    # Calculate split sizes
    train_count = int(total_images * TRAIN_RATIO)
    val_count = int(total_images * VAL_RATIO)

    # Remaining images go to test
    test_count = total_images - train_count - val_count

    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]

    # Create class directories
    train_class_dir = TRAIN_DIR / class_dir.name
    val_class_dir = VAL_DIR / class_dir.name
    test_class_dir = TEST_DIR / class_dir.name

    train_class_dir.mkdir(parents=True, exist_ok=True)
    val_class_dir.mkdir(parents=True, exist_ok=True)
    test_class_dir.mkdir(parents=True, exist_ok=True)

    # Copy files
    for image in train_images:
        shutil.copy2(image, train_class_dir / image.name)

    for image in val_images:
        shutil.copy2(image, val_class_dir / image.name)

    for image in test_images:
        shutil.copy2(image, test_class_dir / image.name)

    total_train += train_count
    total_val += val_count
    total_test += test_count

    print(
        f"{class_dir.name:<35} "
        f"Train: {train_count:2d} | "
        f"Val: {val_count:2d} | "
        f"Test: {test_count:2d}"
    )


# =========================
# SUMMARY
# =========================

print("=" * 60)
print("SPLIT COMPLETE")
print("=" * 60)

print(f"Total training images:   {total_train}")
print(f"Total validation images: {total_val}")
print(f"Total test images:       {total_test}")
print(f"Total images:            {total_train + total_val + total_test}")

print("\nDataset created at:")

print(f"  {TRAIN_DIR}")
print(f"  {VAL_DIR}")
print(f"  {TEST_DIR}")

print("=" * 60)