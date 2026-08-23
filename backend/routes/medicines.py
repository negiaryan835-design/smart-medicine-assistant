from fastapi import APIRouter
from models import Medicine
from db import cursor, connection

router = APIRouter()

@router.get("/medicines")
def get_medicines():
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    return medicines

@router.post("/medicines")
def add_medicine(medicine: Medicine):

    cursor.execute("""
        INSERT INTO medicines
        (UserID, MedicineName, ExpiryDate,
         Quantity, DailyDose, ReminderTime, StartDate)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        medicine.UserID,
        medicine.MedicineName,
        medicine.ExpiryDate,
        medicine.Quantity,
        medicine.DailyDose,
        medicine.ReminderTime,
        medicine.StartDate
    ))

    connection.commit()

    return {
        "message": "Medicine Added Successfully"
    }

@router.put("/medicines/{medicine_id}")
def update_medicine(medicine_id: int, medicine: Medicine):

    cursor.execute("""
        UPDATE medicines
        SET
            UserID=%s,
            MedicineName=%s,
            ExpiryDate=%s,
            Quantity=%s,
            DailyDose=%s,
            ReminderTime=%s,
            StartDate=%s
        WHERE MedicineID=%s
    """, (
        medicine.UserID,
        medicine.MedicineName,
        medicine.ExpiryDate,
        medicine.Quantity,
        medicine.DailyDose,
        medicine.ReminderTime,
        medicine.StartDate,
        medicine_id
    ))

    connection.commit()

    return {
        "message": "Medicine Updated Successfully"
    }

@router.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int):

    cursor.execute(
        "DELETE FROM medicines WHERE MedicineID=%s",
        (medicine_id,)
    )

    connection.commit()

    return {
        "message": "Medicine Deleted Successfully"
    }