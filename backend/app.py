from fastapi import FastAPI
from routes.dashboard import router as dashboard_router
from routes.medicines import router as medicine_router
from routes.reminders import router as reminder_router
from routes.history import router as history_router
from routes.predict import router as predict_router
from routes.refill import router as refill_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(medicine_router)
app.include_router(reminder_router)
app.include_router(history_router)
app.include_router(predict_router)
app.include_router(refill_router)

@app.get("/")
def home():
    return {
        "message": "Smart Medicine Assistant Backend Running"
    }