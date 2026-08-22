import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# 1. Load dataset
data = pd.read_csv("medicine_data.csv")

# 2. Select input features
X = data[["tablets_left", "tablets_per_day", "days_since_start"]]

# 3. Select target
y = data["days_remaining"]

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Create regression model
model = LinearRegression()

# 6. Train the model
model.fit(X_train, y_train)

# 7. Make predictions
predictions = model.predict(X_test)

# 8. Evaluate the model
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model trained successfully!")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R² Score: {r2:.2f}")

# 9. Save trained model
joblib.dump(model, "refill_prediction_model.pkl")

print("Model saved as refill_prediction_model.pkl")
