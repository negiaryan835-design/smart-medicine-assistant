from pydantic import BaseModel

class Medicine(BaseModel):
    UserID: int
    MedicineName: str
    ExpiryDate: str
    Quantity: int
    DailyDose: int
    ReminderTime: str
    StartDate: str