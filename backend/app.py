from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Smart Medicine Assistant Backend Running"
    }
@app.get("/dashboard")
def get_dashboard():
    return {
        "totalMedicines": 2,
        "activeReminders": 3,
        "medicinesScanned": 5
    }