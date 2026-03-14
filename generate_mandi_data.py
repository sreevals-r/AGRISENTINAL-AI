import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

districts = {
"Thiruvananthapuram": ["Neyyattinkara"],
"Kollam": ["Kottarakkara"],
"Ernakulam": ["Perumbavoor"],
"Palakkad": ["Alathur"],
"Thrissur": ["Chalakudy"],
"Malappuram": ["Tirur"],
"Kozhikode": ["Vadakara"]
}

crops = {
"Tomato": 30,
"Onion": 40,
"Banana": 34,
"Paddy": 21
}

weather_options = ["None", "Rain", "Flood", "Drought"]

rows = []
start_date = datetime(2025, 1, 1)

for i in range(10000):


    district = random.choice(list(districts.keys()))
    market = random.choice(districts[district])
    crop = random.choice(list(crops.keys()))

    base_price = crops[crop]

    date = start_date + timedelta(days=i % 365)
    season = "Rabi"

    # Normal price fluctuation
    modal_price = base_price + np.random.normal(0, 2)

    # Introduce anomalies randomly (5%)
    if random.random() < 0.05:
        modal_price *= random.choice([0.5, 0.6, 1.5, 1.7])

    modal_price = max(5, round(modal_price, 2))

    min_price = round(modal_price - random.uniform(2, 4), 2)
    max_price = round(modal_price + random.uniform(2, 4), 2)

    price_prev_day = round(modal_price + np.random.normal(0, 1.5), 2)
    avg_price_7d = round(base_price + np.random.normal(0, 1.5), 2)
    avg_price_30d = round(base_price + np.random.normal(0, 1), 2)

    quantity = int(abs(np.random.normal(12000, 3000)))

    weather = random.choice(weather_options)
    transport_strike = random.choice([0, 1]) if weather == "Flood" else 0
    import_arrival = random.choice([0, 1]) if crop in ["Onion", "Tomato"] else 0

    rows.append([
        district, market, crop, date.strftime("%Y-%m-%d"), season,
        modal_price, min_price, max_price,
        price_prev_day, avg_price_7d, avg_price_30d,
        quantity, weather, transport_strike, import_arrival
        ])

columns = [
"district", "market_name", "crop_type", "date", "season",
"modal_price", "min_price", "max_price",
"price_prev_day", "avg_price_7d", "avg_price_30d",
"quantity_arrived_kg", "weather_event",
"transport_strike", "import_arrival"
]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("synthetic_mandi_10000.csv", index=False)

print("✅ Dataset generated: synthetic_mandi_10000.csv")
