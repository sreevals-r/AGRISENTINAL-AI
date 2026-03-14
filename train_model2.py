import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 1. Load your data
print("Loading data...")
df = pd.read_csv("synthetic_mandi_10000.csv")

# 2. Prepare Features (Inputs) and Target (Output)
# We need to turn text (District, Market, Crop) into numbers for the AI
le_district = LabelEncoder()
le_market = LabelEncoder()
le_crop = LabelEncoder()

df['district_enc'] = le_district.fit_transform(df['district'])
df['market_enc'] = le_market.fit_transform(df['market_name'])
df['crop_enc'] = le_crop.fit_transform(df['crop_type'])

# Convert date to numbers (Month and Day are important for seasonality)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# Define features: [District, Market, Crop, Month, Day]
X = df[['district_enc', 'market_enc', 'crop_enc', 'month', 'day']]
y = df['modal_price']  # We want to predict the price

# 3. Train the Model (Random Forest)
print("Training AI Model (this may take a moment)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Save everything
print("Saving models...")
joblib.dump(model, "price_predictor.pkl")
joblib.dump({
    "district": le_district,
    "market": le_market,
    "crop": le_crop
}, "label_encoders.pkl")

print("✅ Done! You now have 'price_predictor.pkl' and 'label_encoders.pkl'.")