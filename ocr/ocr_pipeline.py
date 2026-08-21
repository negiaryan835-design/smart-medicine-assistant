import easyocr
from pathlib import Path

from image_preprocessor import preprocess_image
from information_extractor import extract_medicine_information


# --------------------------------
# OCR reader
# --------------------------------

reader = easyocr.Reader(["en"])


# --------------------------------
# Process one medicine image
# --------------------------------

def process_medicine_image(image_path):
    """
    Complete OCR pipeline for one medicine image.

    Steps:
    1. Preprocess image
    2. Perform OCR
    3. Filter low-confidence text
    4. Extract medicine information
    5. Return structured data
    """

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # --------------------------------
    # Step 1: Preprocess image
    # --------------------------------

    output_folder = (
        Path(__file__).resolve().parent
        / "output"
        / "preprocessed"
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    preprocessed_path = (
        output_folder
        / f"{image_path.stem}_preprocessed.jpg"
    )

    preprocess_image(
        image_path,
        preprocessed_path
    )

    # --------------------------------
    # Step 2: Perform OCR
    # --------------------------------

    results = reader.readtext(
        str(preprocessed_path)
    )

    # --------------------------------
    # Step 3: Filter OCR results
    # --------------------------------

    recognized_text = []
    confidence_scores = []

    for item in results:

        text = item[1]
        confidence = item[2]

        # Keep all detected text for information extraction
        recognized_text.append(text)

        # Use reasonably confident detections
        # for the overall OCR confidence score
        if confidence >= 0.5:
            confidence_scores.append(confidence)

    # --------------------------------
    # Calculate OCR confidence
    # --------------------------------

    if confidence_scores:
        average_confidence = (
            sum(confidence_scores)
            / len(confidence_scores)
        )
    else:
        average_confidence = 0.0

    # --------------------------------
    # Step 4: Extract medicine details
    # --------------------------------

    medicine_information = (
        extract_medicine_information(
            recognized_text
        )
    )

    # --------------------------------
    # Step 5: Return result
    # --------------------------------

    medicine_information["ocr_confidence"] = round(
        average_confidence,
        2
    )

    return medicine_information