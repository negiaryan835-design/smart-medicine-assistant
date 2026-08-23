from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import date, timedelta
from pathlib import Path

router = APIRouter()

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "regression"
    / "refill_prediction_model.pkl"
)

model = joblib.load(MODEL_PATH)


class RefillRequest(BaseModel):
    quantity_left: int
    daily_dose: int
    adherence_rate: float
    missed_doses: int


@router.post("/refill-prediction")
def predict_refill(data: RefillRequest):

    if data.quantity_left < 0:
        raise ValueError("quantity_left cannot be negative")

    if data.daily_dose <= 0:
        raise ValueError("daily_dose must be greater than 0")

    if not 0 <= data.adherence_rate <= 1:
        raise ValueError(
            "adherence_rate must be between 0 and 1"
        )

    if data.missed_doses < 0:
        raise ValueError("missed_doses cannot be negative")

    if data.quantity_left == 0:
        return {
            "predicted_days_until_refill": 0,
            "predicted_refill_date": date.today().isoformat()
        }

    input_data = pd.DataFrame([{
        "quantity_left": data.quantity_left,
        "daily_dose": data.daily_dose,
        "adherence_rate": data.adherence_rate,
        "missed_doses": data.missed_doses
    }])

    predicted_days = model.predict(input_data)[0]
    predicted_days = max(0, round(predicted_days))

    refill_date = date.today() + timedelta(
        days=predicted_days
    )

    return {
        "predicted_days_until_refill": predicted_days,
        "predicted_refill_date": refill_date.isoformat()
    }