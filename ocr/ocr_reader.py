import easyocr
import json
from pathlib import Path

from image_preprocessor import preprocess_image
from information_extractor import extract_medicine_information


# Get the folder where this Python file is located
OCR_FOLDER = Path(__file__).resolve().parent

# Define image and output folders
IMAGE_FOLDER = OCR_FOLDER / "images"
OUTPUT_FOLDER = OCR_FOLDER / "output"

# Create output folder if it doesn't already exist
OUTPUT_FOLDER.mkdir(exist_ok=True)


def run_ocr(image_path):
    """
    Preprocess the image and run EasyOCR.
    Returns the OCR results.
    """

    print("Preprocessing image...")

    processed_image_path = OUTPUT_FOLDER / "preprocessed_image.jpg"

    preprocess_image(
        image_path,
        processed_image_path
    )

    print("Loading EasyOCR...")

    reader = easyocr.Reader(['en'])

    print("Reading preprocessed image...")

    results = reader.readtext(str(processed_image_path))

    return results

def clean_text(text):
    """
    Clean basic OCR noise from recognized text.
    """

    text = text.strip()

    # Remove unnecessary spaces
    text = " ".join(text.split())

    return text

def save_extracted_text(results, min_confidence=0.5):
    """
    Save recognized text that meets the minimum confidence threshold.
    """

    output_file = OUTPUT_FOLDER / "extracted_text.txt"

    recognized_text = []

    with open(output_file, "w", encoding="utf-8") as file:

        file.write("Recognized Text:\n\n")

        for item in results:

            text = item[1]
            confidence = item[2]

            if confidence >= min_confidence:

                text = clean_text(text)

                if text:
                    print(text)

                    recognized_text.append(text)

                    file.write(text + "\n")

    return recognized_text

def save_extracted_data(medicine_information):
    """
    Save extracted medicine information as a JSON file.
    """

    output_file = OUTPUT_FOLDER / "extracted_data.json"

    with open(output_file, "w", encoding="utf-8") as file:

        json.dump(
            medicine_information,
            file,
            indent=4,
            ensure_ascii=False
        )

    return output_file

def main():

    # Image that we want to process
    image_path = IMAGE_FOLDER / "sample1.jpg"

    # Check whether image exists
    if not image_path.exists():
        print(f"Image not found: {image_path}")
        return

    # Run OCR
    results = run_ocr(image_path)

    # Save recognized text
    recognized_text = save_extracted_text(results)
    medicine_information = extract_medicine_information(
        recognized_text
    )

    print("\nMedicine Information:")
    print("--------------------")

    for key, value in medicine_information.items():
        print(f"{key}: {value}")

    json_file = save_extracted_data(
        medicine_information
    )

    print(f"\nStructured data saved to: {json_file}")

    print("\n--------------------")
    print("OCR completed successfully!")
    print("--------------------")

    print("\nRecognized Text List:")

    for index, text in enumerate(recognized_text, start=1):
        print(f"{index}. {text}")


if __name__ == "__main__":
    main()