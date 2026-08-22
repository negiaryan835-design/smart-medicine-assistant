import joblib
import pandas as pd
from datetime import date, timedelta

# Load the trained model
model = joblib.load("refill_prediction_model.pkl")


def predict_refill(tablets_left, tablets_per_day, days_since_start):
    input_data = pd.DataFrame([{
        "tablets_left": tablets_left,
        "tablets_per_day": tablets_per_day,
        "days_since_start": days_since_start
    }])

    # Make prediction
    predicted_days = model.predict(input_data)[0]

    # Don't allow negative days
    predicted_days = max(0, round(predicted_days))

    # Calculate predicted refill date
    refill_date = date.today() + timedelta(days=predicted_days)

    return {
        "predicted_days_remaining": predicted_days,
        "predicted_refill_date": refill_date.isoformat()
    }


# Test prediction
result = predict_refill(
    tablets_left=20,
    tablets_per_day=2,
    days_since_start=5
)

print("Prediction:")
print(result)
