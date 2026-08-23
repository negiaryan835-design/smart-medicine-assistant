from fastapi import APIRouter, UploadFile, File
from tensorflow.keras.models import load_model
from PIL import Image
from pathlib import Path
import numpy as np
import sys
import tempfile
import os

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "cnn" / "models" / "medicine_mobilenet_best.keras"
CLASS_PATH = BASE_DIR / "cnn" / "models" / "class_names.txt"

OCR_PATH = BASE_DIR / "ocr"
sys.path.insert(0, str(OCR_PATH))

from ocr_pipeline import process_medicine_image

model = load_model(MODEL_PATH)

with open(CLASS_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f if line.strip()]


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_data = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp_file:
        temp_file.write(image_data)
        temp_path = temp_file.name

    try:
        image = Image.open(temp_path).convert("RGB")
        image = image.resize((224, 224))

        image = np.array(image, dtype=np.float32)
        image = np.expand_dims(image, axis=0)

        prediction = model.predict(image, verbose=0)[0]

        index = int(np.argmax(prediction))
        confidence = float(prediction[index])

        medicine_name = class_names[index]

        try:
            ocr_result = process_medicine_image(temp_path)
        except Exception as e:
            ocr_result = {
                "error": str(e)
            }

        return {
            "medicine": medicine_name,
            "confidence": round(confidence, 4),
            "ocr": ocr_result
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)