from fastapi import APIRouter
from db import cursor

router = APIRouter()


@router.get("/reminders")
def reminders():

    cursor.execute("""
        SELECT
            MedicineName,
            DailyDose,
            ReminderTime
        FROM medicines
    """)

    reminders = cursor.fetchall()

    for reminder in reminders:
        total_seconds = int(reminder["ReminderTime"].total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        reminder["ReminderTime"] = f"{hours:02d}:{minutes:02d}"

    return reminders