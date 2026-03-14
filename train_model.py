import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Load dataset

df = pd.read_csv("synthetic_mandi_10000.csv")

# Select numeric features

features = df[[
"modal_price",
"price_prev_day",
"avg_price_7d",
"avg_price_30d",
"quantity_arrived_kg"
]]

# Train model

model = IsolationForest(
n_estimators=200,
contamination=0.05,
random_state=42
)

model.fit(features)

# Save model

joblib.dump(model, "agrisentinel_model.pkl")

print("✅ Model trained and saved!")
