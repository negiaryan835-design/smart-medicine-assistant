from pathlib import Path
from PIL import Image

# =========================
# CONFIGURATION
# =========================

CNN_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = CNN_DIR / "dataset"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# =========================
# STORAGE
# =========================

total_images = 0
corrupt_images = []
image_modes = {}
image_sizes = {}
class_counts = {}

# =========================
# ANALYZE DATASET
# =========================

print("=" * 70)
print("MEDICINE IMAGE DATASET ANALYSIS")
print("=" * 70)

classes = sorted([
    folder for folder in DATASET_DIR.iterdir()
    if folder.is_dir()
])

for class_dir in classes:

    class_images = 0

    for image_path in class_dir.iterdir():

        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        total_images += 1
        class_images += 1

        try:
            with Image.open(image_path) as img:

                # Check that image can actually be loaded
                img.verify()

            # Open again because verify() closes the image
            with Image.open(image_path) as img:

                width, height = img.size
                mode = img.mode

                image_sizes[(width, height)] = (
                    image_sizes.get((width, height), 0) + 1
                )

                image_modes[mode] = image_modes.get(mode, 0) + 1

        except Exception as e:

            corrupt_images.append(
                (str(image_path), str(e))
            )

    class_counts[class_dir.name] = class_images

# =========================
# RESULTS
# =========================

print("\nCLASS DISTRIBUTION")
print("-" * 70)

for class_name, count in class_counts.items():
    print(f"{class_name:<40} {count:>3}")

print("\n" + "=" * 70)

print(f"Total classes : {len(classes)}")
print(f"Total images  : {total_images}")

print("\nIMAGE MODES")
print("-" * 70)

for mode, count in sorted(image_modes.items()):
    print(f"{mode:<10} {count}")

print("\nIMAGE SIZES")
print("-" * 70)

# Show most common image sizes
sorted_sizes = sorted(
    image_sizes.items(),
    key=lambda x: x[1],
    reverse=True
)

for (width, height), count in sorted_sizes[:15]:
    print(f"{width} x {height:<6} → {count} images")

if len(sorted_sizes) > 15:
    print(f"... and {len(sorted_sizes) - 15} other sizes")

# =========================
# CORRUPTED IMAGES
# =========================

print("\nCORRUPTED IMAGES")
print("-" * 70)

if not corrupt_images:

    print("None found.")

else:

    print(f"Found {len(corrupt_images)} corrupted images:")

    for path, error in corrupt_images:
        print(f"\n{path}")
        print(f"Error: {error}")

# =========================
# FINAL STATUS
# =========================

print("\n" + "=" * 70)

if not corrupt_images:
    print("DATASET STATUS: HEALTHY")
else:
    print("DATASET STATUS: NEEDS CLEANING")

print("=" * 70)