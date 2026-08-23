from fastapi import APIRouter
from db import cursor
from datetime import date

router = APIRouter()

@router.get("/medicines/{medicine_id}/adherence")
def get_adherence(medicine_id: int):

    cursor.execute("""
        SELECT
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

    start_date = start_date

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

    missed_doses = max(0, expected_doses - actual_doses)

    if expected_doses == 0:
        adherence_rate = 1.0
    else:
        adherence_rate = actual_doses / expected_doses
        adherence_rate = min(1.0, max(0.0, adherence_rate))

    doses_used = actual_doses
    quantity_left = max(0, quantity - doses_used)

    return {
        "medicine_id": medicine_id,
        "days_since_start": days_since_start,
        "expected_doses": expected_doses,
        "actual_doses": actual_doses,
        "missed_doses": missed_doses,
        "adherence_rate": round(adherence_rate, 2),
        "quantity_left": quantity_left
    }