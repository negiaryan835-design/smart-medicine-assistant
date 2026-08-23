from fastapi import APIRouter
import joblib
import pandas as pd
from datetime import date, timedelta
from pathlib import Path
from db import cursor

router = APIRouter()

MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "regression"
    / "refill_prediction_model.pkl"
)

model = joblib.load(MODEL_PATH)


@router.get("/medicines/{medicine_id}/refill-prediction")
def refill_prediction(medicine_id: int):

    cursor.execute("""
        SELECT
            MedicineID,
            Quantity,
            DailyDose,
            StartDate
        FROM medicines
        WHERE MedicineID = %s
    """, (medicine_id,))

    medicine = cursor.fetchone()

    if not medicine:
        return {
            "error": "Medicine not found"
        }

    quantity = medicine["Quantity"]
    daily_dose = medicine["DailyDose"]
    start_date = medicine["StartDate"]

    if start_date is None:
        return {
            "error": "Start date not available"
        }

    days_since_start = (date.today() - start_date).days

    if days_since_start < 0:
        days_since_start = 0

    expected_doses = days_since_start * daily_dose

    cursor.execute("""
        SELECT COUNT(*) AS actual_doses
        FROM medicinelog
        WHERE MedicineID = %s
    """, (medicine_id,))

    result = cursor.fetchone()
    actual_doses = result["actual_doses"]

    missed_doses = max(
        0,
        expected_doses - actual_doses
    )

    if expected_doses == 0:
        adherence_rate = 1.0
    else:
        adherence_rate = actual_doses / expected_doses
        adherence_rate = min(
            1.0,
            max(0.0, adherence_rate)
        )

    quantity_left = max(
        0,
        quantity - actual_doses
    )

    if quantity_left == 0:
        return {
            "medicine_id": medicine_id,
            "quantity_left": 0,
            "adherence_rate": round(adherence_rate, 2),
            "missed_doses": missed_doses,
            "predicted_days_until_refill": 0,
            "predicted_refill_date": date.today().isoformat()
        }

    input_data = pd.DataFrame([{
        "quantity_left": quantity_left,
        "daily_dose": daily_dose,
        "adherence_rate": adherence_rate,
        "missed_doses": missed_doses
    }])

    predicted_days = model.predict(input_data)[0]
    predicted_days = max(
        0,
        round(predicted_days)
    )

    refill_date = date.today() + timedelta(
        days=predicted_days
    )

    return {
        "medicine_id": medicine_id,
        "quantity_left": quantity_left,
        "days_since_start": days_since_start,
        "expected_doses": expected_doses,
        "actual_doses": actual_doses,
        "missed_doses": missed_doses,
        "adherence_rate": round(adherence_rate, 2),
        "predicted_days_until_refill": predicted_days,
        "predicted_refill_date": refill_date.isoformat()
    }