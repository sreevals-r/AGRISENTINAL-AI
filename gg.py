import streamlit as st
import pandas as pd
import joblib
import time

# ===== LOAD MODEL & DATA =====
model = joblib.load("agrisentinel_model.pkl")
df = pd.read_csv("synthetic_mandi_10000.csv")

# ===== DEMO USERS =====
USERS = {
    "farmer1": "1234",
    "demo": "demo"
}

# ===== SESSION STATE =====
if "page" not in st.session_state:
    st.session_state.page = "login"

# =====================================================
# 🔐 LOGIN PAGE
# =====================================================
if st.session_state.page == "login":
    st.title("🌾 AgriSentinel AI")
    st.subheader("Farmer Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        if username in USERS and USERS[username] == password:
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.stop()

# =====================================================
# 🌾 MARKET ANALYSIS PAGE
# =====================================================
elif st.session_state.page == "app":
    st.title("🌾 Market Price Anomaly Detector")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("🔓 Logout", key="logout_btn"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("🌐 Marketplace", key="goto_marketplace"):
            st.session_state.page = "marketplace"
            st.rerun()
    with col3:
        if st.button("🤝 Collaboration", key="goto_collaboration"):
            st.session_state.page = "collaboration"
            st.rerun()
    with col4:
        if st.button("📈 Market Trends", key="goto_trends"):
            st.session_state.page = "trends"
            st.rerun()
    with col5:
        if st.button("🏦 Subsidies", key="goto_subsidies"):
            st.session_state.page = "subsidies"
            st.rerun()

    st.markdown("---")

    # ===== USER INPUTS =====
    district = st.selectbox("District", sorted(df["district"].unique()), key="analysis_district")

    markets = df[df["district"] == district]["market_name"].unique()
    market = st.selectbox("Market", sorted(markets), key="analysis_market")

    crop_options = df[
        (df["district"] == district) &
        (df["market_name"] == market)
    ]["crop_type"].unique()
    crop = st.selectbox("Crop", sorted(crop_options), key="analysis_crop")

    price = st.number_input("Offered price (₹/kg)", 0.0, 100.0, 30.0, key="analysis_price")

    # ===== ANALYZE =====
    if st.button("Analyze Price", key="analyze_btn"):
        subset = df[
            (df["district"] == district) &
            (df["market_name"] == market) &
            (df["crop_type"] == crop)
        ]

        if subset.empty:
            st.error("No data available")
            st.stop()

        latest = subset.sort_values("date").iloc[-1:]

        features = latest[
            ["price_prev_day", "avg_price_7d", "avg_price_30d", "quantity_arrived_kg"]
        ].copy()

        features["modal_price"] = price
        features = features[
            ["modal_price", "price_prev_day", "avg_price_7d", "avg_price_30d", "quantity_arrived_kg"]
        ]

        result = model.predict(features)[0]
        score = model.decision_function(features)[0]
        anomaly_percent = int((1 - score) * 50)
        anomaly_percent = max(0, min(100, anomaly_percent))

        avg_price = subset["avg_price_30d"].iloc[-1]

        st.subheader("📊 Market Safety Analysis")
        st.metric("Market Risk Score", f"{anomaly_percent}%")

        if price < avg_price * 0.80:
            st.error("⚠️ Price is suspiciously LOW — you may be getting cheated!")
        elif price > avg_price * 1.20:
            st.success("🎉 Price is HIGHER than usual — great time to sell!")
        else:
            st.success("✅ Price appears fair and normal")

        st.subheader("💡 Smart Recommendation")
        if price < avg_price * 0.70:
            st.error("❌ Strongly avoid selling — price is way too low")
        elif price < avg_price * 0.80:
            st.warning("⚠️ Price is below average — try negotiating or wait")
        elif price > avg_price * 1.20:
            st.success("✅ Excellent price — sell now!")
        else:
            st.info("🟡 Fair price — selling is okay")

        st.metric("30-Day Average Price", f"₹{avg_price:.2f}")
        st.metric("Your Offered Price", f"₹{price:.2f}")
        diff = price - avg_price
        st.metric("Difference from Average", f"₹{diff:.2f}", delta=f"{diff:.2f}")

# =====================================================
# 🌐 FARMER MARKETPLACE PAGE
# =====================================================
elif st.session_state.page == "marketplace":
    st.title("🌐 Farmer Marketplace")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️ Market Analysis", key="back_btn"):
            st.session_state.page = "app"
            st.rerun()
    with col2:
        if st.button("🤝 Collaboration", key="goto_collaboration"):
            st.session_state.page = "collaboration"
            st.rerun()
    with col3:
        if st.button("📈 Market Trends", key="goto_trends"):
            st.session_state.page = "trends"
            st.rerun()
    with col4:
        if st.button("🏦 Subsidies", key="goto_subsidies"):
            st.session_state.page = "subsidies"
            st.rerun()
    with col5:
        if st.button("🔓 Logout", key="logout_btn"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("---")

    district = st.selectbox("District", sorted(df["district"].unique()), key="marketplace_district")

    markets = df[df["district"] == district]["market_name"].unique()
    market = st.selectbox("Market", sorted(markets), key="marketplace_market")

    crop_options = df[
        (df["district"] == district) &
        (df["market_name"] == market)
    ]["crop_type"].unique()
    crop = st.selectbox("Crop", sorted(crop_options), key="marketplace_crop")

    offered_price = st.number_input("Price offered (₹/kg)", 0.0, 100.0, 30.0, key="marketplace_price")
    farmer_name = st.text_input("Farmer Name (optional)", key="marketplace_farmer")

    if st.button("Submit Price", key="submit_price"):
        new_entry = {
            "district": district,
            "market_name": market,
            "crop_type": crop,
            "price": offered_price,
            "farmer": farmer_name
        }

        if "market_data" not in st.session_state:
            st.session_state.market_data = []

        st.session_state.market_data.append(new_entry)
        st.success("Price submitted successfully!")

    st.subheader("📊 Community Submitted Prices")
    if "market_data" in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state.market_data))
    else:
        st.info("No submissions yet")

# =====================================================
# 🤝 COLLABORATION PAGE
# =====================================================
elif st.session_state.page == "collaboration":
    st.title("🤝 Collective Sale Collaboration")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️ Market Analysis", key="collab_back_btn"):
            st.session_state.page = "app"
            st.rerun()
    with col2:
        if st.button("🌐 Marketplace", key="collab_marketplace_btn"):
            st.session_state.page = "marketplace"
            st.rerun()
    with col3:
        if st.button("📈 Market Trends", key="collab_trends_btn"):
            st.session_state.page = "trends"
            st.rerun()
    with col4:
        if st.button("🏦 Subsidies", key="collab_subsidies_btn"):
            st.session_state.page = "subsidies"
            st.rerun()
    with col5:
        if st.button("🔓 Logout", key="logout_btn"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("---")

    st.subheader("📢 Post a Collective Sale Request")

    farmer_name = st.text_input("Your Name", key="collab_farmer_name")

    district = st.selectbox("District", sorted(df["district"].unique()), key="collab_district")

    markets = df[df["district"] == district]["market_name"].unique()
    market = st.selectbox("Market", sorted(markets), key="collab_market")

    crop_options = df[
        (df["district"] == district) &
        (df["market_name"] == market)
    ]["crop_type"].unique()
    crop = st.selectbox("Crop", sorted(crop_options), key="collab_crop")

    quantity = st.number_input("Quantity you can contribute (kg)", 0.0, 10000.0, 100.0, key="collab_quantity")
    expected_price = st.number_input("Expected minimum price (₹/kg)", 0.0, 100.0, 30.0, key="collab_price")
    target_quantity = st.number_input("Target total quantity for collective sale (kg)", 0.0, 50000.0, 500.0, key="collab_target")
    contact = st.text_input("Contact number (optional)", key="collab_contact")
    note = st.text_area("Additional note (optional)", key="collab_note")

    if st.button("Post Request", key="collab_submit"):
        if farmer_name.strip() == "":
            st.error("Please enter your name")
        elif quantity <= 0:
            st.error("Please enter a valid quantity")
        else:
            new_request = {
                "Farmer": farmer_name,
                "District": district,
                "Market": market,
                "Crop": crop,
                "My Quantity (kg)": quantity,
                "Expected Price (₹/kg)": expected_price,
                "Target Quantity (kg)": target_quantity,
                "Contact": contact if contact else "Not provided",
                "Note": note if note else "-",
                "Status": "🟢 Open"
            }

            if "collab_requests" not in st.session_state:
                st.session_state.collab_requests = []

            st.session_state.collab_requests.append(new_request)
            st.success(f"✅ Request posted! Looking for farmers to collectively sell {crop} in {market}.")

    st.markdown("---")

    st.subheader("📋 Open Collective Sale Requests")

    if "collab_requests" in st.session_state and len(st.session_state.collab_requests) > 0:
        collab_df = pd.DataFrame(st.session_state.collab_requests)

        filter_crop = st.selectbox(
            "Filter by Crop",
            ["All"] + sorted(collab_df["Crop"].unique().tolist()),
            key="collab_filter_crop"
        )

        if filter_crop != "All":
            collab_df = collab_df[collab_df["Crop"] == filter_crop]

        st.dataframe(collab_df, use_container_width=True)

        st.subheader("🙋 Join a Request")
        st.info("To join a collective sale, contact the farmer directly using the contact number above.")

    else:
        st.info("No collective sale requests yet. Be the first to post one!")

# =====================================================
# 📈 MARKET TRENDS PAGE
# =====================================================
elif st.session_state.page == "trends":
    st.title("📈 Market Price Trends")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️ Market Analysis", key="trends_back"):
            st.session_state.page = "app"
            st.rerun()
    with col2:
        if st.button("🌐 Marketplace", key="trends_marketplace"):
            st.session_state.page = "marketplace"
            st.rerun()
    with col3:
        if st.button("🤝 Collaboration", key="trends_collab"):
            st.session_state.page = "collaboration"
            st.rerun()
    with col4:
        if st.button("🏦 Subsidies", key="trends_subsidies"):
            st.session_state.page = "subsidies"
            st.rerun()
    with col5:
        if st.button("🔓 Logout", key="logout_btn"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District", sorted(df["district"].unique()), key="trends_district")
    with col2:
        markets = df[df["district"] == district]["market_name"].unique()
        market = st.selectbox("Market", sorted(markets), key="trends_market")
    with col3:
        crop_options = df[
            (df["district"] == district) &
            (df["market_name"] == market)
        ]["crop_type"].unique()
        crop = st.selectbox("Crop", sorted(crop_options), key="trends_crop")

    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, key="trends_start")
    with col2:
        end_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date, key="trends_end")

    st.markdown("---")

    subset = df[
        (df["district"] == district) &
        (df["market_name"] == market) &
        (df["crop_type"] == crop) &
        (df["date"] >= pd.Timestamp(start_date)) &
        (df["date"] <= pd.Timestamp(end_date))
    ].sort_values("date")

    if subset.empty:
        st.error("No data found for this selection")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"₹{subset['modal_price'].iloc[-1]:.2f}")
    with col2:
        st.metric("7-Day Avg", f"₹{subset['avg_price_7d'].iloc[-1]:.2f}")
    with col3:
        st.metric("30-Day Avg", f"₹{subset['avg_price_30d'].iloc[-1]:.2f}")
    with col4:
        price_change = subset['modal_price'].iloc[-1] - subset['modal_price'].iloc[-2] if len(subset) > 1 else 0
        st.metric("Price Change", f"₹{price_change:.2f}", delta=f"{price_change:.2f}")

    st.markdown("---")

    st.subheader(f"💰 Price Trend — {crop} in {market}")
    chart_data = subset[["date", "modal_price", "avg_price_7d", "avg_price_30d"]].set_index("date")
    chart_data.columns = ["Daily Price", "7-Day Avg", "30-Day Avg"]
    st.line_chart(chart_data)

    st.subheader(f"📦 Quantity Arrived — {crop} in {market}")
    qty_data = subset[["date", "quantity_arrived_kg"]].set_index("date")
    qty_data.columns = ["Quantity (kg)"]
    st.bar_chart(qty_data)

    st.markdown("---")
    auto_refresh = st.toggle("🔄 Auto-refresh every 10 seconds", key="auto_refresh")
    if auto_refresh:
        placeholder = st.empty()
        with placeholder.container():
            st.info("🔄 Auto-refreshing... live data will update every 10 seconds")
        time.sleep(10)
        st.rerun()

    with st.expander("🗂️ View Raw Data"):
        st.dataframe(
            subset[["date", "modal_price", "price_prev_day", "avg_price_7d", "avg_price_30d", "quantity_arrived_kg"]]
            .sort_values("date", ascending=False)
            .reset_index(drop=True),
            use_container_width=True
        )

# =====================================================
# 🏦 SUBSIDIES PAGE
# =====================================================
elif st.session_state.page == "subsidies":
    st.title("🏦 Government Subsidies & Schemes")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⬅️ Market Analysis", key="subsidies_back"):
            st.session_state.page = "app"
            st.rerun()
    with col2:
        if st.button("🌐 Marketplace", key="subsidies_marketplace"):
            st.session_state.page = "marketplace"
            st.rerun()
    with col3:
        if st.button("🤝 Collaboration", key="subsidies_collab"):
            st.session_state.page = "collaboration"
            st.rerun()
    with col4:
        if st.button("📈 Market Trends", key="subsidies_trends"):
            st.session_state.page = "trends"
            st.rerun()
    with col5:
        if st.button("🔓 Logout", key="logout_btn"):
            st.session_state.page = "login"
            st.rerun()

    st.markdown("---")

    subsidies = [
        {
            "id": 1,
            "title": "PM-KISAN Samman Nidhi",
            "category": "Direct Income Support",
            "amount": "₹6,000/year",
            "eligibility": "All small and marginal farmers with less than 2 hectares of land",
            "deadline": "March 31, 2025",
            "status": "🟢 Active",
            "description": (
                "Under this scheme, eligible farmer families receive ₹6,000 per year "
                "in three equal installments of ₹2,000 each directly into their bank accounts. "
                "No middlemen involved."
            ),
            "how_to_apply": "Visit your nearest Common Service Centre (CSC) or apply at pmkisan.gov.in",
            "documents": ["Aadhaar Card", "Land Records", "Bank Passbook"]
        },
        {
            "id": 2,
            "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
            "category": "Crop Insurance",
            "amount": "Up to ₹2,00,000 coverage",
            "eligibility": "All farmers growing notified crops in notified areas",
            "deadline": "Before sowing season",
            "status": "🟢 Active",
            "description": (
                "Provides financial support to farmers suffering crop loss or damage "
                "due to unforeseen events like floods, drought, pests, or diseases. "
                "Premium as low as 2% for Kharif crops."
            ),
            "how_to_apply": "Apply through nearest bank branch or insurance company or pmfby.gov.in",
            "documents": ["Aadhaar Card", "Land Records", "Bank Passbook", "Sowing Certificate"]
        },
        {
            "id": 3,
            "title": "Kerala Karshaka Kshemasree Scheme",
            "category": "State Welfare Scheme",
            "amount": "₹1,000/month pension",
            "eligibility": "Kerala farmers above 60 years with less than 1 acre land",
            "deadline": "Rolling applications",
            "status": "🟢 Active",
            "description": (
                "A Kerala state government welfare scheme providing monthly pension "
                "to elderly small farmers who have no other source of income. "
                "Administered through the Agriculture Department."
            ),
            "how_to_apply": "Apply at your local Krishi Bhavan with required documents",
            "documents": ["Aadhaar Card", "Age Proof", "Land Records", "Income Certificate"]
        },
    ]

    categories = ["All"] + list(set(s["category"] for s in subsidies))
    selected_category = st.selectbox("Filter by Category", categories, key="subsidy_filter")

    st.markdown("---")

    for subsidy in subsidies:
        if selected_category != "All" and subsidy["category"] != selected_category:
            continue

        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(f"{subsidy['title']}")
                st.caption(f"📂 {subsidy['category']}  |  {subsidy['status']}  |  ⏰ Deadline: {subsidy['deadline']}")
                st.write(subsidy["description"])

            with col2:
                st.metric("Benefit", subsidy["amount"])
                st.caption(f"👤 {subsidy['eligibility']}")

            with st.expander("📋 View Full Details & How to Apply"):
                st.markdown("**✅ Eligibility:**")
                st.write(subsidy["eligibility"])

                st.markdown("**📝 How to Apply:**")
                st.write(subsidy["how_to_apply"])

                st.markdown("**📁 Documents Required:**")
                for doc in subsidy["documents"]:
                    st.write(f"• {doc}")

                st.button(
                    "✅ I'm Interested",
                    key=f"interest_btn_{subsidy['id']}",
                    help="Save this scheme to your interest list"
                )

            st.markdown("---")

    st.subheader("🔔 Get Notified About New Schemes")
    notify_name = st.text_input("Your Name", key="notify_name")
    notify_phone = st.text_input("Phone Number", key="notify_phone")

    if st.button("Subscribe for Updates", key="notify_submit"):
        if notify_name.strip() == "" or notify_phone.strip() == "":
            st.error("Please enter both name and phone number")
        else:
            st.success(f"✅ {notify_name}, you'll be notified about new subsidies and schemes!")