import pandas as pd
import joblib

# Load trained model

model = joblib.load("agrisentinel_model.pkl")

# Example new market data (simulate farmer input)

new_data = pd.DataFrame([{
"modal_price": 12,
"price_prev_day": 28,
"avg_price_7d": 30,
"avg_price_30d": 31,
"quantity_arrived_kg": 8000
}])

prediction = model.predict(new_data)[0]

if prediction == -1:
    print("⚠️ ALERT: Suspicious price detected!")
else:
    print("✅ Price appears normal.")
