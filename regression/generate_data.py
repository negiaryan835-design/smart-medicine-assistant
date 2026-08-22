import numpy as np
import pandas as pd

np.random.seed(42)

rows = []

for _ in range(1000):

    # Tablets currently remaining
    quantity_left = np.random.randint(5, 101)

    # Prescribed tablets per day
    daily_dose = np.random.choice([1, 2, 3])

    # Number of days over which we observe the user's behaviour
    observation_days = np.random.randint(7, 31)

    # Total doses the user was expected to take
    expected_doses = observation_days * daily_dose

    # User's natural adherence behaviour
    adherence_rate = np.random.uniform(0.60, 1.00)

    # Simulate the number of doses actually taken
    doses_taken = np.random.binomial(
        expected_doses,
        adherence_rate
    )

    # Calculate actual missed doses
    missed_doses = expected_doses - doses_taken

    # Actual adherence calculated from behaviour
    actual_adherence = doses_taken / expected_doses

    # Average number of tablets actually consumed per day
    avg_daily_usage = doses_taken / observation_days

    # Prevent zero usage
    avg_daily_usage = max(avg_daily_usage, 0.1)

    # Calculate days until the remaining supply runs out
    days_until_refill = quantity_left / avg_daily_usage

    # Small measurement/behaviour variation
    noise = np.random.normal(0, 0.5)

    days_until_refill = max(
        1,
        days_until_refill + noise
    )

    rows.append({
        "quantity_left": quantity_left,
        "daily_dose": daily_dose,
        "avg_daily_usage": round(avg_daily_usage, 2),
        "adherence_rate": round(actual_adherence, 2),
        "missed_doses": missed_doses,
        "days_until_refill": round(days_until_refill, 1)
    })


# Create DataFrame
data = pd.DataFrame(rows)

# Save training dataset
data.to_csv("medicine_training_data.csv", index=False)

print("Training dataset generated successfully!")
print(f"Number of records: {len(data)}")

print("\nFirst 10 records:")
print(data.head(10))

print("\nDataset statistics:")
print(data.describe())