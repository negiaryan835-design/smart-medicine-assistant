from pathlib import Path

CNN_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = CNN_DIR / "dataset" / "raw"

print("=" * 50)
print("MEDICINE DATASET INVENTORY")
print("=" * 50)

total_images = 0

for class_dir in sorted(DATASET_DIR.iterdir()):
    if class_dir.is_dir():
        images = [
            image for image in class_dir.iterdir()
            if image.is_file()
            and image.suffix.lower() in {".jpg", ".jpeg", ".png"}
        ]

        count = len(images)
        total_images += count

        print(f"{class_dir.name:<35} {count:>3} images")

print("-" * 50)
print(f"Total classes : {len([d for d in DATASET_DIR.iterdir() if d.is_dir()])}")
print(f"Total images  : {total_images}")