import json
from pathlib import Path

from ocr_pipeline import process_medicine_image


# --------------------------------
# Folder paths
# --------------------------------

OCR_FOLDER = Path(__file__).resolve().parent

IMAGE_FOLDER = OCR_FOLDER / "images"
OUTPUT_FOLDER = OCR_FOLDER / "output"
RESULTS_FOLDER = OUTPUT_FOLDER / "results"


# Create output folder if it doesn't exist

RESULTS_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------
# Supported image formats
# --------------------------------

SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


# --------------------------------
# Process all images
# --------------------------------

def main():

    image_files = [
        file
        for file in IMAGE_FOLDER.iterdir()
        if file.suffix.lower() in SUPPORTED_FORMATS
    ]

    if not image_files:

        print("\nNo medicine images found.")

        print(
            f"Please add images to: {IMAGE_FOLDER}"
        )

        return

    print(
        f"\nFound {len(image_files)} image(s)."
    )

    all_results = {}

    for image_path in sorted(image_files):

        print("\n" + "=" * 50)
        print(f"Processing: {image_path.name}")
        print("=" * 50)

        try:

            information = process_medicine_image(
                image_path
            )

            all_results[image_path.name] = information

            # --------------------------------
            # Save individual JSON result
            # --------------------------------

            result_file = (
                RESULTS_FOLDER /
                f"{image_path.stem}.json"
            )

            with open(
                result_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    information,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("\nExtracted Information:")
            print("---------------------")

            for key, value in information.items():

                print(f"{key}: {value}")

            print(
                f"\nSaved result to: {result_file}"
            )

        except Exception as error:

            print(
                f"\nError processing "
                f"{image_path.name}: {error}"
            )

    # --------------------------------
    # Save combined results
    # --------------------------------

    combined_file = (
        OUTPUT_FOLDER /
        "all_results.json"
    )

    with open(
        combined_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 50)
    print("ALL IMAGES PROCESSED")
    print("=" * 50)

    print(
        f"Combined results saved to: {combined_file}"
    )


# --------------------------------
# Run program
# --------------------------------

if __name__ == "__main__":
    main()