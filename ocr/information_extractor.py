import re


def extract_medicine_information(recognized_text):

    """
    Extract structured medicine information from OCR text.
    """

    medicine_name = None
    brand_name = None
    strength = None
    dosage = None
    manufacturer = None
    storage = None

    # --------------------------------
    # 1. Clean OCR text
    # --------------------------------

    cleaned_text = []

    for text in recognized_text:
        text = text.strip()

        if text:
            cleaned_text.append(text)

    # --------------------------------
    # 2. Strength
    # --------------------------------

    # Handles common OCR variations such as:
    # 500 mg
    # 500mg
    # 150 mg
    # 150mg
    # 5.5 mg

    strength_pattern = (
        r'\b\d+(?:\.\d+)?\s*(?:mg|g|mcg|ml|%|IU)\b'
    )

    for text in cleaned_text:

        match = re.search(
            strength_pattern,
            text,
            re.IGNORECASE
        )

        if match:
            strength = match.group()
            break

    # --------------------------------
    # 3. Medicine name
    # --------------------------------

    # Direct recognition of common medicine names

    for text in cleaned_text:

        lower_text = text.lower()

        if "paracetamol" in lower_text:

            medicine_name = "Paracetamol"
            break

    # If Paracetamol was not found,
    # use dosage-form based approach.

    if medicine_name is None:

        dosage_forms = [
            "capsules",
            "tablets",
            "syrup",
            "injection",
            "suspension",
            "cream",
            "ointment",
            "drops"
        ]

        for text in cleaned_text:

            lower_text = text.lower()

            if any(
                form in lower_text
                for form in dosage_forms
            ):

                possible_name = text

                # Remove dosage form
                for form in dosage_forms:

                    possible_name = re.sub(
                        rf'\b{form}\b',
                        '',
                        possible_name,
                        flags=re.IGNORECASE
                    )

                # Remove IP
                possible_name = re.sub(
                    r'\bIP\b',
                    '',
                    possible_name,
                    flags=re.IGNORECASE
                )

                # Remove strength
                possible_name = re.sub(
                    strength_pattern,
                    '',
                    possible_name,
                    flags=re.IGNORECASE
                )

                possible_name = possible_name.strip(
                    " -:,.;"
                )

                # Ignore obvious OCR noise
                if len(possible_name) >= 3:

                    if not re.fullmatch(
                        r'[\d\s\W]+',
                        possible_name
                    ):

                        medicine_name = possible_name
                        break

    # --------------------------------
    # 4. Brand name
    # --------------------------------

    for text in cleaned_text:

        lower_text = text.lower()

        # Dolo-650
        if re.search(
            r'\bdolo[-\s]?650\b',
            lower_text,
            re.IGNORECASE
        ):

            brand_name = "Dolo-650"
            break

        # Dabipla
        if "dabipla" in lower_text:

            brand_name = re.sub(
                r'\s+\d+(?:\.\d+)?$',
                '',
                text.strip()
            )

            brand_name = brand_name.strip(
                " -:,.;"
            )

            break

    # If no commercial brand was found,
    # use medicine + dosage-form pattern.

    if brand_name is None:

        for text in cleaned_text:

            match = re.search(
                r'^(paracetamol)\s+tablets?\s+IP$',
                text.strip(),
                re.IGNORECASE
            )

            if match:

                brand_name = "Paracetamol Tablets IP"
                break

    # --------------------------------
    # 5. Strength from brand pattern
    # --------------------------------

    # Some medicine brands include the strength
    # directly in the brand name, e.g. Dolo-650.

    if strength is None and brand_name:

        dolo_match = re.search(
            r'\bdolo[-\s]?(\d+)\b',
            brand_name,
            re.IGNORECASE
        )

        if dolo_match:
            strength = f"{dolo_match.group(1)} mg"

    # --------------------------------
    # 6. Dosage
    # --------------------------------

    for index, text in enumerate(cleaned_text):

        if "dosage" in text.lower():

            if index + 1 < len(cleaned_text):

                possible_dosage = cleaned_text[index + 1]

                if possible_dosage:
                    dosage = possible_dosage

            break

    # --------------------------------
    # 7. Manufacturer
    # --------------------------------

    for text in cleaned_text:

        lower_text = text.lower()

        # Example:
        # Marketed by CIPLA LTD.

        if "marketed by" in lower_text:

            manufacturer = re.sub(
                r'.*?marketed\s+by\s*',
                '',
                text,
                flags=re.IGNORECASE
            ).strip()

            if manufacturer:
                break

        # Example:
        # Mfg: Cipla

        if "mfg:" in lower_text:

            manufacturer = re.sub(
                r'.*?mfg:\s*',
                '',
                text,
                flags=re.IGNORECASE
            ).strip()

            if manufacturer:
                break

    # --------------------------------
    # 8. Storage information
    # --------------------------------

    storage_lines = []

    for text in cleaned_text:

        lower_text = text.lower()

        if (
            "protect from moisture" in lower_text
            or "store below" in lower_text
            or "store in" in lower_text
            or "keep in" in lower_text
            or "keep away" in lower_text
        ):

            storage_lines.append(text)

    if storage_lines:

        storage = " ".join(storage_lines)

    # --------------------------------
    # 9. Return structured information
    # --------------------------------

    return {
        "medicine_name": medicine_name,
        "brand_name": brand_name,
        "strength": strength,
        "dosage": dosage,
        "manufacturer": manufacturer,
        "storage": storage
    }