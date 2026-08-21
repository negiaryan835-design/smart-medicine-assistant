from pathlib import Path

from ocr_pipeline import process_medicine_image


# Find the ocr folder
ocr_folder = Path(__file__).resolve().parent

# Find the sample image
image_path = ocr_folder / "images" / "sample1.jpg"


# Run OCR pipeline
result = process_medicine_image(image_path)


# Display result
print("\nMedicine Information")
print("--------------------")

for key, value in result.items():
    print(f"{key}: {value}")

print("\nPipeline test completed successfully.")