from fastapi import APIRouter
from pydantic import BaseModel
from db import cursor, connection

router = APIRouter()


class MedicineLogRequest(BaseModel):
    MedicineID: int
    TakenDate: str
    TakenTime: str


@router.get("/history")
def history():

    cursor.execute("""
        SELECT
            medicinelog.LogID,
            medicinelog.MedicineID,
            medicines.MedicineName,
            medicinelog.TakenDate,
            medicinelog.TakenTime
        FROM medicinelog
        JOIN medicines
        ON medicinelog.MedicineID = medicines.MedicineID
        ORDER BY medicinelog.TakenDate DESC,
                 medicinelog.TakenTime DESC
    """)

    return cursor.fetchall()


@router.post("/medicinelog")
def log_medicine(data: MedicineLogRequest):

    cursor.execute("""
        INSERT INTO medicinelog
        (MedicineID, TakenDate, TakenTime)
        VALUES (%s, %s, %s)
    """, (
        data.MedicineID,
        data.TakenDate,
        data.TakenTime
    ))

    connection.commit()

    return {
        "message": "Medicine dose recorded successfully"
    }