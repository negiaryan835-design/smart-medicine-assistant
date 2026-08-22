import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib


# 1. Load training dataset
data = pd.read_csv("medicine_training_data.csv")


# 2. Select input features
X = data[
    [
        "quantity_left",
        "daily_dose",
        "adherence_rate",
        "missed_doses"
    ]
]


# 3. Select target
y = data["days_until_refill"]


# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------------------------
# MODEL 1: LINEAR REGRESSION
# --------------------------------------------------

linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)

linear_r2 = r2_score(
    y_test,
    linear_predictions
)


# --------------------------------------------------
# MODEL 2: RANDOM FOREST REGRESSION
# --------------------------------------------------

forest_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

forest_model.fit(X_train, y_train)

forest_predictions = forest_model.predict(X_test)

forest_mae = mean_absolute_error(
    y_test,
    forest_predictions
)

forest_r2 = r2_score(
    y_test,
    forest_predictions
)


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\nMODEL COMPARISON")
print("------------------------------")

print("\nLinear Regression:")
print(f"MAE: {linear_mae:.2f} days")
print(f"R² : {linear_r2:.2f}")

print("\nRandom Forest Regression:")
print(f"MAE: {forest_mae:.2f} days")
print(f"R² : {forest_r2:.2f}")


# --------------------------------------------------
# SELECT BEST MODEL
# --------------------------------------------------

if forest_mae < linear_mae:
    best_model = forest_model
    best_model_name = "Random Forest Regression"
    best_mae = forest_mae
    best_r2 = forest_r2
else:
    best_model = linear_model
    best_model_name = "Linear Regression"
    best_mae = linear_mae
    best_r2 = linear_r2


print("\nBEST MODEL")
print("------------------------------")
print(f"Model: {best_model_name}")
print(f"MAE: {best_mae:.2f} days")
print(f"R² : {best_r2:.2f}")


# --------------------------------------------------
# SAVE BEST MODEL
# --------------------------------------------------

joblib.dump(
    best_model,
    "refill_prediction_model.pkl"
)

print("\nBest model saved as refill_prediction_model.pkl")