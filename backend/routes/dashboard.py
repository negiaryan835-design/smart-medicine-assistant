from fastapi import APIRouter
from db import cursor

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    cursor.execute("SELECT COUNT(*) AS totalMedicines FROM medicines")
    total = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS activeReminders FROM medicines")
    reminders = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS medicinesScanned FROM medicinelog")
    scanned = cursor.fetchone()

    return {
        "totalMedicines": total["totalMedicines"],
        "activeReminders": reminders["activeReminders"],
        "medicinesScanned": scanned["medicinesScanned"]
    }