import joblib
import pandas as pd
from datetime import date, timedelta


# Load the trained model
model = joblib.load("refill_prediction_model.pkl")


def predict_refill(
    quantity_left,
    daily_dose,
    adherence_rate,
    missed_doses
):

    # -----------------------------
    # INPUT VALIDATION
    # -----------------------------

    if quantity_left < 0:
        raise ValueError("quantity_left cannot be negative")

    if daily_dose <= 0:
        raise ValueError("daily_dose must be greater than 0")

    if not 0 <= adherence_rate <= 1:
        raise ValueError(
            "adherence_rate must be between 0 and 1"
        )

    if missed_doses < 0:
        raise ValueError("missed_doses cannot be negative")

    if not isinstance(missed_doses, int):
        raise ValueError("missed_doses must be an integer")

    # If no tablets are left, refill is needed immediately
    if quantity_left == 0:
        return {
            "predicted_days_until_refill": 0,
            "predicted_refill_date": date.today().isoformat()
        }

    # -----------------------------
    # PREPARE INPUT
    # -----------------------------

    input_data = pd.DataFrame([{
        "quantity_left": quantity_left,
        "daily_dose": daily_dose,
        "adherence_rate": adherence_rate,
        "missed_doses": missed_doses
    }])

    # -----------------------------
    # MAKE PREDICTION
    # -----------------------------

    predicted_days = model.predict(input_data)[0]

    # Don't allow negative predictions
    predicted_days = max(0, round(predicted_days))

    # Calculate predicted refill date
    refill_date = date.today() + timedelta(
        days=predicted_days
    )

    return {
        "predicted_days_until_refill": predicted_days,
        "predicted_refill_date": refill_date.isoformat()
    }


# -----------------------------
# TEST PREDICTION
# -----------------------------

result = predict_refill(
    quantity_left=20,
    daily_dose=2,
    adherence_rate=0.80,
    missed_doses=4
)

print("Prediction:")
print(result)