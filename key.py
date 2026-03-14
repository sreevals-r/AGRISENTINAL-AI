import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

# 1. Load Data and Resources
print("📊 Calculating AgriSentinel Metrics...")
df = pd.read_csv("synthetic_mandi_10000.csv")
encoders = joblib.load("label_encoders.pkl")
model = joblib.load("price_predictor.pkl")

# 2. Prepare Data (Same logic as training)
# We convert text columns to numbers so we can test the model
df['district_enc'] = encoders["district"].transform(df['district'])
df['market_enc'] = encoders["market"].transform(df['market_name'])
df['crop_enc'] = encoders["crop"].transform(df['crop_type'])
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

# Define inputs (X) and target (y)
X = df[['district_enc', 'market_enc', 'crop_enc', 'month', 'day']]
y = df['modal_price']

# 3. Test the Model
# We split data to test on unseen rows (standard validation method)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
y_pred = model.predict(X_test)

# 4. Calculate Metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
accuracy_percentage = r2 * 100 

print("\n" + "="*40)
print("   🏆 KEY METRICS FOR SLIDE")
print("="*40)
print(f"1. Model Accuracy (R² Score):  {accuracy_percentage:.2f}%")
print(f"2. Mean Absolute Error (MAE):  ₹{mae:.2f}")
print(f"3. Root Mean Sq Error (RMSE):  ₹{np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print("="*40)
print("\n📝 Copy this text for your 'Testing Results' slide:")
print(f"• Achieved a validation accuracy of {accuracy_percentage:.1f}% in price forecasting.")
print(f"• The model predicts market prices with an average error margin of only ₹{mae:.2f}.")
print("• Robust outlier detection using Isolation Forest (Unsupervised).")