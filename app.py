import streamlit as st
import pandas as pd
import joblib
import time
import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="AgriSentinel AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --green-deep: #1a3a2a;
    --green-mid: #2d6a4f;
    --green-bright: #52b788;
    --green-light: #95d5b2;
    --gold: #f4a261;
    --gold-light: #ffd166;
    --cream: #fefae0;
    --cream-dark: #f0e8c8;
    --red-warn: #e63946;
    --bg-dark: #0d1f17;
    --text-primary: #fefae0;
    --text-muted: #95d5b2;
    --card-bg: rgba(45, 106, 79, 0.15);
    --card-border: rgba(82, 183, 136, 0.25);
}

* { font-family: 'DM Sans', sans-serif; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-dark) !important;
    color: var(--text-primary) !important;
}

[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(ellipse at 20% 20%, rgba(45,106,79,0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(26,58,42,0.4) 0%, transparent 50%),
        var(--bg-dark) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1f17 0%, #1a3a2a 100%) !important;
    border-right: 1px solid var(--card-border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Main title style */
.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #95d5b2, #52b788, #f4a261);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}

.subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-weight: 300;
    letter-spacing: 0.05em;
    margin-bottom: 2rem;
}

/* Cards */
.metric-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: var(--green-bright);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(82,183,136,0.15);
}

/* Stat badge */
.stat-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    font-weight: 500;
}

.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--cream);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--green-mid), var(--green-deep)) !important;
    color: var(--cream) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--green-bright), var(--green-mid)) !important;
    border-color: var(--green-bright) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(82,183,136,0.3) !important;
}

/* Primary action button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), #e07b39) !important;
    border-color: var(--gold) !important;
    color: var(--green-deep) !important;
    font-weight: 700 !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Number input */
[data-testid="stNumberInput"] > div > div > input {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Text input */
[data-testid="stTextInput"] > div > div > input {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Text area */
textarea {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: var(--cream) !important;
    font-size: 1.6rem !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}

/* Divider */
hr {
    border-color: var(--card-border) !important;
    margin: 1.5rem 0 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Label text */
label, [data-testid="stWidgetLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* Toggle */
[data-testid="stToggle"] label {
    color: var(--text-primary) !important;
    text-transform: none !important;
    letter-spacing: normal !important;
    font-size: 0.9rem !important;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(82,183,136,0.1) !important;
    border-color: rgba(82,183,136,0.3) !important;
}

/* Nav divider */
.nav-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--green-bright), transparent);
    margin: 1rem 0;
}

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--green-light);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Subsidy card */
.subsidy-card {
    background: linear-gradient(135deg, rgba(45,106,79,0.2), rgba(26,58,42,0.3));
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.subsidy-card:hover {
    border-color: var(--green-bright);
    box-shadow: 0 8px 32px rgba(82,183,136,0.1);
}

/* Tag badge */
.tag {
    display: inline-block;
    background: rgba(82,183,136,0.15);
    border: 1px solid rgba(82,183,136,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    color: var(--green-light);
    font-weight: 500;
    letter-spacing: 0.05em;
}

.tag-gold {
    background: rgba(244,162,97,0.15);
    border-color: rgba(244,162,97,0.3);
    color: var(--gold-light);
}

/* Login card */
.login-card {
    background: linear-gradient(135deg, rgba(45,106,79,0.2), rgba(26,58,42,0.4));
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2.5rem;
    backdrop-filter: blur(20px);
    max-width: 420px;
    margin: 0 auto;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--green-mid); border-radius: 3px; }

/* Hide streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Stagger animation */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeInUp 0.5s ease forwards;
}

/* Pulse animation for risk */
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(230,57,70,0.4); }
    50% { box-shadow: 0 0 0 10px rgba(230,57,70,0); }
}

.risk-high { animation: pulse-red 2s infinite; }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODEL & DATA =====
model = joblib.load("agrisentinel_model.pkl")
price_model = joblib.load("price_predictor.pkl")
encoders = joblib.load("label_encoders.pkl")
df = pd.read_csv("synthetic_mandi_10000.csv")

# ===== DEMO USERS =====
USERS = {
    "Rohith": "1234",
    "demo": "demo"
}

# ===== TRANSLATIONS =====
LANG = {
    "English": {
        "app_title": "AgriSentinel AI",
        "app_sub": "Smart Market Intelligence for Farmers",
        "login_title": "Welcome Back",
        "login_sub": "Sign in to your farmer account",
        "username": "Username",
        "password": "Password",
        "login_btn": "Sign In →",
        "invalid_login": "Invalid username or password",
        "logout": "🔓 Logout",
        "marketplace": "🌐 Marketplace",
        "collaboration": "🤝 Collective sale",
        "trends": "📈 Trends",
        "subsidies": "🏦 Subsidies",
        "market_analysis": "Market Price Analysis",
        "market_sub": "Enter details to check if the offered price is fair",
        "district": "District",
        "market": "Market",
        "crop": "Crop Type",
        "offered_price": "Offered Price (₹/kg)",
        "analyze_btn": "Analyze Price →",
        "no_data": "No data available for this selection",
        "market_safety": "Analysis Results",
        "risk_score": "Risk Score",
        "price_low": "⚠️ Price is suspiciously LOW — you may be getting cheated!",
        "price_high": "🎉 Price is HIGHER than usual — great time to sell!",
        "price_normal": "✅ Price appears fair and normal",
        "recommendation": "Smart Recommendation",
        "avoid_selling": "❌ Strongly avoid selling — price is way too low",
        "below_avg": "⚠️ Price is below average — try negotiating or wait",
        "excellent_price": "✅ Excellent price — sell now!",
        "fair_price": "🟡 Fair price — selling is okay",
        "avg_30": "30-Day Average",
        "your_price": "Your Price",
        "difference": "Difference",
        "marketplace_title": "Farmer Marketplace",
        "marketplace_sub": "Share and discover crop prices in your community",
        "back_analysis": "⬅ Analysis",
        "farmer_name": "Farmer Name (optional)",
        "submit_price": "Submit Price →",
        "submitted": "✅ Price submitted successfully!",
        "community_prices": "Community Prices",
        "no_submissions": "No submissions yet — be the first!",
        "collab_title": "Collective Sale",
        "collab_sub": "Join forces with other farmers for better prices",
        "post_request": "Post a Request",
        "your_name": "Your Name",
        "quantity": "Your Quantity (kg)",
        "expected_price": "Expected Min Price (₹/kg)",
        "target_qty": "Target Total Quantity (kg)",
        "contact": "Contact Number (optional)",
        "note": "Additional Note (optional)",
        "post_btn": "Post Request →",
        "name_error": "Please enter your name",
        "qty_error": "Please enter a valid quantity",
        "request_posted": "✅ Request posted! Looking for farmers to collectively sell",
        "open_requests": "Open Requests",
        "filter_crop": "Filter by Crop",
        "join_request": "How to Join",
        "join_info": "Contact the farmer directly using the number listed above to join their collective sale.",
        "no_requests": "No requests yet — be the first to post!",
        "trends_title": "Market Trends",
        "trends_sub": "Track price movements and market patterns",
        "date_from": "From Date",
        "date_to": "To Date",
        "current_price": "Current Price",
        "day7_avg": "7-Day Avg",
        "day30_avg": "30-Day Avg",
        "price_change": "Change",
        "price_trend": "Price Trend",
        "qty_arrived": "Quantity Arrived",
        "auto_refresh": "🔄 Auto-refresh (10s)",
        "refreshing": "🔄 Live mode active — refreshing every 10 seconds",
        "raw_data": "📊 View Raw Data",
        "subsidies_title": "Subsidies & Schemes",
        "subsidies_sub": "Government support available for farmers",
        "filter_category": "Filter by Category",
        "benefit": "Benefit",
        "view_details": "View Details & Apply",
        "eligibility": "Eligibility",
        "how_to_apply": "How to Apply",
        "documents": "Documents Required",
        "interested": "✅ I'm Interested",
        "notify_title": "Get Notified",
        "notify_name": "Your Name",
        "notify_phone": "Phone Number",
        "subscribe": "Subscribe →",
        "notify_error": "Please enter both name and phone number",
        "notify_success": "you'll be notified about new subsidies!",
        "language": "Language",
    },
    "Malayalam": {
        "app_title": "അഗ്രിസെന്റിനൽ AI",
        "app_sub": "കർഷകർക്കായി സ്മാർട്ട് വിപണി ഇൻ്റലിജൻസ്",
        "login_title": "സ്വാഗതം",
        "login_sub": "നിങ്ങളുടെ കർഷക അക്കൗണ്ടിലേക്ക് സൈൻ ഇൻ ചെയ്യുക",
        "username": "യൂസർനെയിം",
        "password": "പാസ്‌വേഡ്",
        "login_btn": "സൈൻ ഇൻ →",
        "invalid_login": "തെറ്റായ യൂസർനെയിം അല്ലെങ്കിൽ പാസ്‌വേഡ്",
        "logout": "🔓 ലോഗൗട്ട്",
        "marketplace": "🌐 മാർക്കറ്റ്",
        "collaboration": "🤝 സഹകരണം",
        "trends": "📈 ട്രെൻഡുകൾ",
        "subsidies": "🏦 സബ്സിഡി",
        "market_analysis": "വിപണി വില വിശകലനം",
        "market_sub": "വാഗ്ദാനം ചെയ്ത വില ന്യായമാണോ എന്ന് പരിശോധിക്കുക",
        "district": "ജില്ല",
        "market": "മണ്ടി",
        "crop": "വിളയുടെ തരം",
        "offered_price": "വാഗ്ദാനം ചെയ്ത വില (₹/കിലോ)",
        "analyze_btn": "വില വിശകലനം ചെയ്യുക →",
        "no_data": "ഈ തിരഞ്ഞെടുപ്പിന് ഡാറ്റ ലഭ്യമല്ല",
        "market_safety": "വിശകലന ഫലങ്ങൾ",
        "risk_score": "റിസ്ക് സ്കോർ",
        "price_low": "⚠️ വില സംശയാസ്പദമായി കുറവാണ് — നിങ്ങൾ വഞ്ചിക്കപ്പെടുന്നുണ്ടാകാം!",
        "price_high": "🎉 വില സാധാരണയേക്കാൾ കൂടുതലാണ് — വിൽക്കാൻ നല്ല സമയം!",
        "price_normal": "✅ വില ന്യായമായി കാണപ്പെടുന്നു",
        "recommendation": "സ്മാർട്ട് ശുപാർശ",
        "avoid_selling": "❌ വിൽക്കരുത് — വില വളരെ കുറവാണ്",
        "below_avg": "⚠️ വില ശരാശരിയിൽ താഴെ — ചർച്ച ചെയ്യുക",
        "excellent_price": "✅ മികച്ച വില — ഇപ്പോൾ വിൽക്കുക!",
        "fair_price": "🟡 ന്യായമായ വില — വിൽക്കാം",
        "avg_30": "30 ദിവസ ശരാശരി",
        "your_price": "നിങ്ങളുടെ വില",
        "difference": "വ്യത്യാസം",
        "marketplace_title": "കർഷക മാർക്കറ്റ്",
        "marketplace_sub": "കമ്മ്യൂണിറ്റിയിൽ വില പങ്കിടുക",
        "back_analysis": "⬅ വിശകലനം",
        "farmer_name": "കർഷകന്റെ പേര് (ഐച്ഛികം)",
        "submit_price": "വില സമർപ്പിക്കുക →",
        "submitted": "✅ വില വിജയകരമായി സമർപ്പിച്ചു!",
        "community_prices": "കമ്മ്യൂണിറ്റി വിലകൾ",
        "no_submissions": "ഇതുവരെ സമർപ്പണങ്ങളൊന്നുമില്ല",
        "collab_title": "കൂട്ടായ വിൽപ്പന",
        "collab_sub": "മികച്ച വിലകൾക്കായി മറ്റ് കർഷകരുമായി ചേരുക",
        "post_request": "അഭ്യർത്ഥന പോസ്റ്റ് ചെയ്യുക",
        "your_name": "നിങ്ങളുടെ പേര്",
        "quantity": "നിങ്ങളുടെ അളവ് (കിലോ)",
        "expected_price": "പ്രതീക്ഷിക്കുന്ന കുറഞ്ഞ വില (₹/കിലോ)",
        "target_qty": "ലക്ഷ്യ അളവ് (കിലോ)",
        "contact": "ഫോൺ നമ്പർ (ഐച്ഛികം)",
        "note": "അധിക കുറിപ്പ് (ഐച്ഛികം)",
        "post_btn": "അഭ്യർത്ഥന പോസ്റ്റ് ചെയ്യുക →",
        "name_error": "ദയവായി നിങ്ങളുടെ പേര് നൽകുക",
        "qty_error": "ദയവായി സാധുവായ അളവ് നൽകുക",
        "request_posted": "✅ അഭ്യർത്ഥന പോസ്റ്റ് ചെയ്തു!",
        "open_requests": "തുറന്ന അഭ്യർത്ഥനകൾ",
        "filter_crop": "വിളയനുസരിച്ച് ഫിൽട്ടർ",
        "join_request": "എങ്ങനെ ചേരാം",
        "join_info": "ചേരാൻ മുകളിലെ നമ്പർ ഉപയോഗിച്ച് കർഷകനെ നേരിട്ട് ബന്ധപ്പെടുക.",
        "no_requests": "ഇതുവരെ അഭ്യർത്ഥനകളൊന്നുമില്ല",
        "trends_title": "വിപണി ട്രെൻഡുകൾ",
        "trends_sub": "വില ചലനങ്ങൾ ട്രാക്ക് ചെയ്യുക",
        "date_from": "തുടക്ക തീയതി",
        "date_to": "അവസാന തീയതി",
        "current_price": "നിലവിലെ വില",
        "day7_avg": "7 ദിവസ ശരാശരി",
        "day30_avg": "30 ദിവസ ശരാശരി",
        "price_change": "മാറ്റം",
        "price_trend": "വില ട്രെൻഡ്",
        "qty_arrived": "എത്തിയ അളവ്",
        "auto_refresh": "🔄 സ്വയം പുതുക്കൽ (10s)",
        "refreshing": "🔄 ലൈവ് മോഡ് — 10 സെക്കൻഡിൽ പുതുക്കുന്നു",
        "raw_data": "📊 അസംസ്കൃത ഡാറ്റ",
        "subsidies_title": "സബ്സിഡികളും പദ്ധതികളും",
        "subsidies_sub": "കർഷകർക്ക് ലഭ്യമായ സർക്കാർ പിന്തുണ",
        "filter_category": "വിഭാഗം അനുസരിച്ച് ഫിൽട്ടർ",
        "benefit": "ആനുകൂല്യം",
        "view_details": "വിശദാംശങ്ങൾ & അപേക്ഷ",
        "eligibility": "യോഗ്യത",
        "how_to_apply": "എങ്ങനെ അപേക്ഷിക്കാം",
        "documents": "ആവശ്യമായ രേഖകൾ",
        "interested": "✅ എനിക്ക് താൽപ്പര്യമുണ്ട്",
        "notify_title": "അറിയിപ്പ് നേടുക",
        "notify_name": "നിങ്ങളുടെ പേര്",
        "notify_phone": "ഫോൺ നമ്പർ",
        "subscribe": "സബ്സ്ക്രൈബ് →",
        "notify_error": "ദയവായി പേരും ഫോൺ നമ്പറും നൽകുക",
        "notify_success": "പുതിയ സബ്സിഡികളെക്കുറിച്ച് നിങ്ങളെ അറിയിക്കും!",
        "language": "ഭാഷ",
    },
    "Hindi": {
        "app_title": "एग्रीसेंटिनल AI",
        "app_sub": "किसानों के लिए स्मार्ट मार्केट इंटेलिजेंस",
        "login_title": "स्वागत है",
        "login_sub": "अपने किसान खाते में साइन इन करें",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "login_btn": "साइन इन करें →",
        "invalid_login": "अमान्य उपयोगकर्ता नाम या पासवर्ड",
        "logout": "🔓 लॉगआउट",
        "marketplace": "🌐 बाज़ार (Marketplace)",
        "collaboration": "🤝 सामूहिक बिक्री",
        "trends": "📈 रुझान (Trends)",
        "subsidies": "🏦 सब्सिडी",
        "market_analysis": "बाज़ार मूल्य विश्लेषण",
        "market_sub": "विवरण दर्ज करें और जानें कि कीमत उचित है या नहीं",
        "district": "ज़िला",
        "market": "मंडी",
        "crop": "फसल का प्रकार",
        "offered_price": "प्रस्तावित मूल्य (₹/किग्रा)",
        "analyze_btn": "मूल्य का विश्लेषण करें →",
        "no_data": "इस चयन के लिए कोई डेटा उपलब्ध नहीं है",
        "market_safety": "विश्लेषण परिणाम",
        "risk_score": "जोखिम स्कोर",
        "price_low": "⚠️ कीमत संदिग्ध रूप से कम है — आपके साथ धोखा हो सकता है!",
        "price_high": "🎉 कीमत सामान्य से अधिक है — बेचने का सही समय!",
        "price_normal": "✅ कीमत उचित और सामान्य लग रही है",
        "recommendation": "स्मार्ट सुझाव",
        "avoid_selling": "❌ बेचने से बचें — कीमत बहुत कम है",
        "below_avg": "⚠️ कीमत औसत से कम है — बातचीत करें या प्रतीक्षा करें",
        "excellent_price": "✅ बेहतरीन कीमत — अभी बेचें!",
        "fair_price": "🟡 उचित कीमत — बेचना ठीक है",
        "avg_30": "30-दिन का औसत",
        "your_price": "आपकी कीमत",
        "difference": "अंतर",
        "marketplace_title": "किसान बाज़ार",
        "marketplace_sub": "समुदाय में फसल की कीमतें साझा करें और जानें",
        "back_analysis": "⬅ विश्लेषण",
        "farmer_name": "किसान का नाम (वैकल्पिक)",
        "submit_price": "कीमत जमा करें →",
        "submitted": "✅ कीमत सफलतापूर्वक जमा की गई!",
        "community_prices": "सामुदायिक कीमतें",
        "no_submissions": "अभी तक कोई प्रविष्टि नहीं — सबसे पहले आप करें!",
        "collab_title": "सामूहिक बिक्री",
        "collab_sub": "बेहतर कीमतों के लिए अन्य किसानों के साथ जुड़ें",
        "post_request": "अनुरोध पोस्ट करें",
        "your_name": "आपका नाम",
        "quantity": "आपकी मात्रा (किग्रा)",
        "expected_price": "अपेक्षित न्यूनतम मूल्य (₹/किग्रा)",
        "target_qty": "लक्ष्य कुल मात्रा (किग्रा)",
        "contact": "संपर्क नंबर (वैकल्पिक)",
        "note": "अतिरिक्त नोट (वैकल्पिक)",
        "post_btn": "अनुरोध पोस्ट करें →",
        "name_error": "कृपया अपना नाम दर्ज करें",
        "qty_error": "कृपया एक मान्य मात्रा दर्ज करें",
        "request_posted": "✅ अनुरोध पोस्ट किया गया! सामूहिक बिक्री के लिए किसानों की तलाश",
        "open_requests": "खुले अनुरोध",
        "filter_crop": "फसल के अनुसार फ़िल्टर करें",
        "join_request": "कैसे शामिल हों",
        "join_info": "सामूहिक बिक्री में शामिल होने के लिए ऊपर दिए गए नंबर पर किसान से सीधे संपर्क करें।",
        "no_requests": "अभी तक कोई अनुरोध नहीं — सबसे पहले आप पोस्ट करें!",
        "trends_title": "बाज़ार रुझान",
        "trends_sub": "मूल्य आंदोलनों और बाज़ार पैटर्न को ट्रैक करें",
        "date_from": "इस तारीख से",
        "date_to": "इस तारीख तक",
        "current_price": "वर्तमान मूल्य",
        "day7_avg": "7-दिन का औसत",
        "day30_avg": "30-दिन का औसत",
        "price_change": "परिवर्तन",
        "price_trend": "मूल्य रुझान",
        "qty_arrived": "पहुंची मात्रा",
        "auto_refresh": "🔄 ऑटो-रिफ्रेश (10s)",
        "refreshing": "🔄 लाइव मोड सक्रिय — हर 10 सेकंड में रिफ्रेश हो रहा है",
        "raw_data": "📊 कच्चा डेटा देखें",
        "subsidies_title": "सब्सिडी और योजनाएं",
        "subsidies_sub": "किसानों के लिए उपलब्ध सरकारी सहायता",
        "filter_category": "श्रेणी के अनुसार फ़िल्टर करें",
        "benefit": "लाभ",
        "view_details": "विवरण देखें और आवेदन करें",
        "eligibility": "पात्रता",
        "how_to_apply": "आवेदन कैसे करें",
        "documents": "आवश्यक दस्तावेज़",
        "interested": "✅ मुझे दिलचस्पी है",
        "notify_title": "अधिसूचना प्राप्त करें",
        "notify_name": "आपका नाम",
        "notify_phone": "फ़ोन नंबर",
        "subscribe": "सदस्यता लें →",
        "notify_error": "कृपया नाम और फ़ोन नंबर दोनों दर्ज करें",
        "notify_success": "आपको नई सब्सिडी के बारे में सूचित किया जाएगा!",
        "language": "भाषा",
    }
}

# ===== SESSION STATE =====
if "page" not in st.session_state:
    st.session_state.page = "login"
if "language" not in st.session_state:
    st.session_state.language = "English"

# ===== HELPER: NAV SIDEBAR =====
# ===== HELPER: NAV SIDEBAR =====
# ===== HELPER: NAV SIDEBAR =====
# ===== HELPER: NAV SIDEBAR =====
# ===== HELPER: NAV SIDEBAR =====
def render_sidebar(T, current_page):
    with st.sidebar:
        # 1. HEADER (Logo & Title)
        st.markdown(f"""
        <div style="padding: 1rem 0 0.5rem;">
            <div style="font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800;
                background: linear-gradient(135deg, #95d5b2, #f4a261);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text;">🌾 AgriSentinel</div>
            <div style="font-size: 0.7rem; color: #52b788; letter-spacing: 0.1em; margin-top: 0.2rem;">
                SMART FARM INTELLIGENCE
            </div>
        </div>
        <div class="nav-divider"></div>
        """, unsafe_allow_html=True)

        # 2. LANGUAGE SELECTOR
        lang_choice = st.selectbox(
            T["language"],
            ["English", "Malayalam","Hindi"],
            index=0 if st.session_state.language == "English" else 1,
            key="lang_sidebar"
        )
        if lang_choice != st.session_state.language:
            st.session_state.language = lang_choice
            st.rerun()

        # 3. NAVIGATION MENU
        st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.7rem; color:#52b788; letter-spacing:0.1em; padding: 0.3rem 0;'>NAVIGATION</div>", unsafe_allow_html=True)

        pages = [
            ("app", "📊 " + T["market_analysis"].split()[0] + " Analysis"),
            ("marketplace", T["marketplace"]),
            ("collaboration", T["collaboration"]),
            ("trends", T["trends"]),
            ("subsidies", T["subsidies"]),
        ]

        for page_key, label in pages:
            is_active = (current_page == page_key)
            # Use disabled button for active state to maintain exact alignment
            if st.button(label, key=f"nav_{page_key}", use_container_width=True, disabled=is_active):
                st.session_state.page = page_key
                st.rerun()

        st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)
        
        # 4. LOGOUT BUTTON
        if st.button(T["logout"], key="logout_btn", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

        # 5. COPYRIGHT TEXT (Fixed Position)
        st.markdown("""
        <div style="margin-top: 4rem; padding-bottom: 2rem;
            font-size: 0.7rem; color: #2d6a4f; text-align: center; letter-spacing: 0.05em;">
            © 2025 AgriSentinel AI<br>Protecting Farmers
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# 🔐 LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    # --- CSS MODIFICATIONS ---
    st.markdown("""
    <style>
        /* 1. Adjust top padding */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* 2. HIDE "Press Enter to apply" TEXT */
        [data-testid="InputInstructions"] {
            display: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Top Right Language Selector ---
    col_spacer, col_lang = st.columns([5, 1.2]) 
    with col_lang:
        lang_choice = st.selectbox(
            "🌐 Languages",
            ["English", "Malayalam"],
            index=0 if st.session_state.language == "English" else 1,
            key="lang_login"
        )
    st.session_state.language = lang_choice
    T = LANG[st.session_state.language]

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- LOGO & WELCOME TEXT ---
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;
                background: linear-gradient(to bottom, #95d5b2, #52b788);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;">🌾</div>
            <div class="main-title" style="font-size: 2.2rem; text-align: center;">{T['app_title']}</div>
            <div class="subtitle" style="text-align: center;">{T['app_sub']}</div>
        </div>
        
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700;
                color: #fefae0; margin-bottom: 0.3rem;">{T['login_title']}</div>
            <div style="font-size: 0.85rem; color: #95d5b2;">{T['login_sub']}</div>
        </div>
        """, unsafe_allow_html=True)

        # --- INPUTS ---
        username = st.text_input(T["username"], key="login_user", placeholder="Enter username")
        password = st.text_input(T["password"], type="password", key="login_pass", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(T["login_btn"], key="login_btn", use_container_width=True, type="primary"):
            if username in USERS and USERS[username] == password:
                st.session_state.page = "app"
                # --- SAVE USERNAME FOR PROFILE ---
                st.session_state.username = username 
                st.rerun()
            else:
                st.error(T["invalid_login"])

        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; font-size: 0.8rem; color: #52b788;">
            Demo: Rohith / 1234
        </div>
        """, unsafe_allow_html=True)

    st.stop()
# =====================================================
# 🌾 MARKET ANALYSIS PAGE
# =====================================================
if st.session_state.page == "app":
    T = LANG[st.session_state.language]
    render_sidebar(T, "app")

    # --- 1. NEW HEADER WITH PROFILE SECTION ---
    # Split layout: 75% for Title, 25% for Profile
    col_header, col_profile = st.columns([3, 1]) 

    with col_header:
        st.markdown(f'<div class="main-title">{T["market_analysis"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="subtitle">{T["market_sub"]}</div>', unsafe_allow_html=True)

    with col_profile:
        # Get username (default to 'Guest' if not found)
        user_display = st.session_state.get("username", "Guest")
        
        # Display Profile "Card" aligned to the right
        st.markdown(f"""
        <div style="
            background: rgba(45, 106, 79, 0.4); 
            border: 1px solid rgba(82, 183, 136, 0.3);
            border-radius: 50px; 
            padding: 0.5rem 1rem; 
            display: flex; 
            align-items: center; 
            gap: 0.8rem;
            width: fit-content;
            margin-left: auto;">
            <div style="
                width: 35px; height: 35px; 
                background: linear-gradient(135deg, #f4a261, #e76f51); 
                border-radius: 50%; 
                display: flex; justify-content: center; align-items: center; 
                font-weight: bold; color: white;">
                {user_display[0].upper()}
            </div>
            <div style="line-height: 1.2;">
                <div style="font-size: 0.7rem; color: #95d5b2; text-transform: uppercase;">Farmer</div>
                <div style="font-family: 'Syne', sans-serif; font-weight: 600; color: #fefae0;">{user_display}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    # --- 2. INPUTS ---
    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox(T["district"], sorted(df["district"].unique()), key="analysis_district")
    with col2:
        markets = df[df["district"] == district]["market_name"].unique()
        market = st.selectbox(T["market"], sorted(markets), key="analysis_market")
    with col3:
        crop_options = df[
            (df["district"] == district) &
            (df["market_name"] == market)
        ]["crop_type"].unique()
        crop = st.selectbox(T["crop"], sorted(crop_options), key="analysis_crop")

    col_price, col_btn = st.columns([2, 1])
    with col_price:
        # Allow negative numbers so we can test the error logic (-100.0)
        price = st.number_input(T["offered_price"], -100.0, 10000.0, 30.0, key="analysis_price")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze = st.button(T["analyze_btn"], key="analyze_btn", use_container_width=True, type="primary")

    if analyze:
        subset = df[
            (df["district"] == district) &
            (df["market_name"] == market) &
            (df["crop_type"] == crop)
        ]

        if subset.empty:
            st.error(T["no_data"])
            st.stop()

        # --- 3. AI ESTIMATION ---
        current_date = pd.Timestamp.now()
        try:
            d_enc = encoders["district"].transform([district])[0]
            m_enc = encoders["market"].transform([market])[0]
            c_enc = encoders["crop"].transform([crop])[0]
            
            ai_input = [[d_enc, m_enc, c_enc, current_date.month, current_date.day]]
            ai_fair_price = price_model.predict(ai_input)[0]
            price_source = "🤖 AI Estimate"
        except:
            ai_fair_price = subset["avg_price_30d"].iloc[-1]
            price_source = "📊 30-Day Avg"

        # --- 4. SMART VALIDATION GATES ---
        if price <= 0:
            st.error("❌ Error: Price must be greater than zero.")
            st.stop()
        elif price > ai_fair_price * 1.5:
            st.error(f"⚠️ Price Rejected: This is 50% higher than the expected market rate (₹{ai_fair_price:.2f}). Please check for typos.")
            st.stop()
        elif price < ai_fair_price * 0.5:
            st.error(f"⚠️ Price Rejected: This is suspiciously low compared to the market rate (₹{ai_fair_price:.2f}). Potential manipulation detected.")
            st.stop()

        # --- 5. DISPLAY RESULTS (Corrected Colors) ---
        diff = price - ai_fair_price

        st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="section-header">📊 {T["market_safety"]}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"Fair Price ({price_source})", f"₹{ai_fair_price:.2f}")
        with col2:
            st.metric(T["your_price"], f"₹{price:.2f}")
        with col3:
            # delta_color="normal" -> Green for Positive, Red for Negative
            st.metric(T["difference"], f"₹{diff:.2f}", delta=f"{diff:.2f}", delta_color="normal")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- 6. RECOMMENDATION ---
        if price < ai_fair_price * 0.80:
            st.error(T["price_low"])
        elif price > ai_fair_price * 1.20:
            st.success(T["price_high"])
        else:
            st.success(T["price_normal"])

        st.markdown(f'<div class="section-header" style="margin-top:1.5rem;">💡 {T["recommendation"]}</div>', unsafe_allow_html=True)
        
        if price < ai_fair_price * 0.70:
            st.error(T["avoid_selling"])
        elif price < ai_fair_price * 0.90:
            st.warning(T["below_avg"])
        elif price > ai_fair_price * 1.15:
            st.success(T["excellent_price"])
        else:
            st.info(T["fair_price"])

# =====================================================
# 🌐 FARMER MARKETPLACE PAGE
# =====================================================
elif st.session_state.page == "marketplace":
    T = LANG[st.session_state.language]
    render_sidebar(T, "marketplace")

    st.markdown(f'<div class="main-title">{T["marketplace_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{T["marketplace_sub"]}</div>', unsafe_allow_html=True)
    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        district = st.selectbox(T["district"], sorted(df["district"].unique()), key="marketplace_district")
        markets = df[df["district"] == district]["market_name"].unique()
        market = st.selectbox(T["market"], sorted(markets), key="marketplace_market")
    with col2:
        crop_options = df[
            (df["district"] == district) &
            (df["market_name"] == market)
        ]["crop_type"].unique()
        crop = st.selectbox(T["crop"], sorted(crop_options), key="marketplace_crop")
        offered_price = st.number_input(T["offered_price"], 0.0, 100.0, 30.0, key="marketplace_price")

    farmer_name = st.text_input(T["farmer_name"], key="marketplace_farmer")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(T["submit_price"], key="submit_price", type="primary"):
        new_entry = {
            "District": district,
            "Market": market,
            "Crop": crop,
            "Price (₹/kg)": offered_price,
            "Farmer": farmer_name if farmer_name else "Anonymous"
        }
        if "market_data" not in st.session_state:
            st.session_state.market_data = []
        st.session_state.market_data.append(new_entry)
        st.success(T["submitted"])

    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🌐 {T["community_prices"]}</div>', unsafe_allow_html=True)

    if "market_data" in st.session_state and len(st.session_state.market_data) > 0:
        st.dataframe(pd.DataFrame(st.session_state.market_data), use_container_width=True)
    else:
        st.info(T["no_submissions"])

# =====================================================
# 🤝 COLLABORATION PAGE
# =====================================================
elif st.session_state.page == "collaboration":
    T = LANG[st.session_state.language]
    render_sidebar(T, "collaboration")

    st.markdown(f'<div class="main-title">{T["collab_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{T["collab_sub"]}</div>', unsafe_allow_html=True)
    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    st.markdown(f'<div class="section-header">📢 {T["post_request"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        farmer_name = st.text_input(T["your_name"], key="collab_farmer_name")
        district = st.selectbox(T["district"], sorted(df["district"].unique()), key="collab_district")
        markets = df[df["district"] == district]["market_name"].unique()
        market = st.selectbox(T["market"], sorted(markets), key="collab_market")
        crop_options = df[
            (df["district"] == district) &
            (df["market_name"] == market)
        ]["crop_type"].unique()
        crop = st.selectbox(T["crop"], sorted(crop_options), key="collab_crop")
    with col2:
        quantity = st.number_input(T["quantity"], 0.0, 10000.0, 100.0, key="collab_quantity")
        expected_price = st.number_input(T["expected_price"], 0.0, 100.0, 30.0, key="collab_price")
        target_quantity = st.number_input(T["target_qty"], 0.0, 50000.0, 500.0, key="collab_target")
        contact = st.text_input(T["contact"], key="collab_contact")
        note = st.text_area(T["note"], key="collab_note", height=80)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(T["post_btn"], key="collab_submit", type="primary"):
        if farmer_name.strip() == "":
            st.error(T["name_error"])
        elif quantity <= 0:
            st.error(T["qty_error"])
        else:
            new_request = {
                "Farmer": farmer_name,
                "District": district,
                "Market": market,
                "Crop": crop,
                "Quantity (kg)": quantity,
                "Min Price (₹/kg)": expected_price,
                "Target Qty (kg)": target_quantity,
                "Contact": contact if contact else "Not provided",
                "Note": note if note else "-",
                "Status": "🟢 Open"
            }
            if "collab_requests" not in st.session_state:
                st.session_state.collab_requests = []
            st.session_state.collab_requests.append(new_request)
            st.success(f"{T['request_posted']} {crop} in {market}.")

    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">📋 {T["open_requests"]}</div>', unsafe_allow_html=True)

    if "collab_requests" in st.session_state and len(st.session_state.collab_requests) > 0:
        collab_df = pd.DataFrame(st.session_state.collab_requests)
        filter_crop = st.selectbox(
            T["filter_crop"],
            ["All"] + sorted(collab_df["Crop"].unique().tolist()),
            key="collab_filter_crop"
        )
        if filter_crop != "All":
            collab_df = collab_df[collab_df["Crop"] == filter_crop]
        st.dataframe(collab_df, use_container_width=True)
        st.markdown(f'<div class="section-header" style="margin-top:1rem;">🙋 {T["join_request"]}</div>', unsafe_allow_html=True)
        st.info(T["join_info"])
    else:
        st.info(T["no_requests"])

# =====================================================
# 📈 MARKET TRENDS PAGE
# =====================================================
elif st.session_state.page == "trends":
    T = LANG[st.session_state.language]
    render_sidebar(T, "trends")

    st.markdown(f'<div class="main-title">{T["trends_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{T["trends_sub"]}</div>', unsafe_allow_html=True)
    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox(T["district"], sorted(df["district"].unique()), key="trends_district")
    with col2:
        markets = df[df["district"] == district]["market_name"].unique()
        market = st.selectbox(T["market"], sorted(markets), key="trends_market")
    with col3:
        crop_options = df[
            (df["district"] == district) &
            (df["market_name"] == market)
        ]["crop_type"].unique()
        crop = st.selectbox(T["crop"], sorted(crop_options), key="trends_crop")

    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(T["date_from"], value=min_date, min_value=min_date, max_value=max_date, key="trends_start")
    with col2:
        end_date = st.date_input(T["date_to"], value=max_date, min_value=min_date, max_value=max_date, key="trends_end")

    subset = df[
        (df["district"] == district) &
        (df["market_name"] == market) &
        (df["crop_type"] == crop) &
        (df["date"] >= pd.Timestamp(start_date)) &
        (df["date"] <= pd.Timestamp(end_date))
    ].sort_values("date")

    if subset.empty:
        st.error(T["no_data"])
        st.stop()

    # --- 1. PREPARE HISTORICAL DATA ---
    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(T["current_price"], f"₹{subset['modal_price'].iloc[-1]:.2f}")
    with col2:
        st.metric(T["day7_avg"], f"₹{subset['avg_price_7d'].iloc[-1]:.2f}")
    with col3:
        st.metric(T["day30_avg"], f"₹{subset['avg_price_30d'].iloc[-1]:.2f}")
    with col4:
        price_change = subset['modal_price'].iloc[-1] - subset['modal_price'].iloc[-2] if len(subset) > 1 else 0
        st.metric(T["price_change"], f"₹{price_change:.2f}", delta=f"{price_change:.2f}")

    # --- 2. GENERATE AI FORECAST (Next 7 Days) ---
    forecast_df = pd.DataFrame()
    try:
        # OLD BROKEN WAY: Started from "Today" (Caused the gap)
        # future_dates = [pd.Timestamp.now() + datetime.timedelta(days=i) for i in range(1, 8)]
        
        # NEW FIXED WAY: Start immediately after the last historical date
        last_date = subset["date"].max()
        future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, 8)]
        
        # Prepare inputs
        d_enc = encoders["district"].transform([district])[0]
        m_enc = encoders["market"].transform([market])[0]
        c_enc = encoders["crop"].transform([crop])[0]
        
        predictions = []
        for d in future_dates:
            # Ask AI for price on this specific future date
            pred_price = price_model.predict([[d_enc, m_enc, c_enc, d.month, d.day]])[0]
            predictions.append(pred_price)
            
        forecast_df = pd.DataFrame({"date": future_dates, "Forecast": predictions})
        forecast_df.set_index("date", inplace=True)
    except:
        pass
    # --- 3. PLOT GRAPH ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">💰 {T["price_trend"]} + 7 Day Forecast</div>', unsafe_allow_html=True)
    
    # Organize History
    history_data = subset[["date", "modal_price"]].set_index("date")
    history_data.columns = ["History"]
    
    # Combine History + Forecast
    if not forecast_df.empty:
        # Combine both datasets. 'outer' ensures we keep old dates AND new dates.
        final_chart = history_data.join(forecast_df, how='outer')
        # Plot: Green for History, Orange for Forecast
        st.line_chart(final_chart, color=["#52b788", "#f4a261"])
    else:
        st.line_chart(history_data, color=["#52b788"])

    st.markdown(f'<div class="section-header">📦 {T["qty_arrived"]} — {crop} in {market}</div>', unsafe_allow_html=True)
    qty_data = subset[["date", "quantity_arrived_kg"]].set_index("date")
    qty_data.columns = ["Quantity (kg)"]
    st.bar_chart(qty_data, color="#2d6a4f")

# =====================================================
# 🏦 SUBSIDIES PAGE
# =====================================================
elif st.session_state.page == "subsidies":
    T = LANG[st.session_state.language]
    render_sidebar(T, "subsidies")

    st.markdown(f'<div class="main-title">{T["subsidies_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{T["subsidies_sub"]}</div>', unsafe_allow_html=True)
    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    subsidies = [
        {
            "id": 1,
            "title": "PM-KISAN Samman Nidhi",
            "category": "Direct Income Support",
            "amount": "₹6,000/year",
            "eligibility": "All small and marginal farmers with less than 2 hectares of land",
            "deadline": "March 31, 2025",
            "status": "🟢 Active",
            "description": "Eligible farmer families receive ₹6,000 per year in three equal installments of ₹2,000 each directly into their bank accounts. No middlemen involved.",
            "how_to_apply": "Visit your nearest Common Service Centre (CSC) or apply at pmkisan.gov.in",
            "documents": ["Aadhaar Card", "Land Records", "Bank Passbook"]
        },
        {
            "id": 2,
            "title": "Pradhan Mantri Fasal Bima Yojana",
            "category": "Crop Insurance",
            "amount": "Up to ₹2,00,000",
            "eligibility": "All farmers growing notified crops in notified areas",
            "deadline": "Before sowing season",
            "status": "🟢 Active",
            "description": "Financial support for crop loss due to floods, drought, pests, or diseases. Premium as low as 2% for Kharif crops.",
            "how_to_apply": "Apply through nearest bank branch or at pmfby.gov.in",
            "documents": ["Aadhaar Card", "Land Records", "Bank Passbook", "Sowing Certificate"]
        },
        {
            "id": 3,
            "title": "Kerala Karshaka Kshemasree",
            "category": "State Welfare",
            "amount": "₹1,000/month",
            "eligibility": "Kerala farmers above 60 years with less than 1 acre land",
            "deadline": "Rolling applications",
            "status": "🟢 Active",
            "description": "Monthly pension for elderly small farmers with no other income source. Administered through the Kerala Agriculture Department.",
            "how_to_apply": "Apply at your local Krishi Bhavan with required documents",
            "documents": ["Aadhaar Card", "Age Proof", "Land Records", "Income Certificate"]
        },
    ]

    categories = ["All"] + list(set(s["category"] for s in subsidies))
    selected_category = st.selectbox(T["filter_category"], categories, key="subsidy_filter")
    st.markdown("<br>", unsafe_allow_html=True)

    for subsidy in subsidies:
        if selected_category != "All" and subsidy["category"] != selected_category:
            continue

        st.markdown(f"""
        <div class="subsidy-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem;">
                <div>
                    <div style="font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700;
                        color: #fefae0; margin-bottom: 0.4rem;">{subsidy['title']}</div>
                    <span class="tag">{subsidy['category']}</span>
                    <span class="tag" style="margin-left: 0.4rem;">{subsidy['status']}</span>
                    <span class="tag-gold tag" style="margin-left: 0.4rem;">⏰ {subsidy['deadline']}</span>
                </div>
                <div style="text-align: right;">
                    <div style="font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800;
                        color: #f4a261;">{subsidy['amount']}</div>
                    <div style="font-size: 0.75rem; color: #52b788;">{T['benefit']}</div>
                </div>
            </div>
            <div style="font-size: 0.88rem; color: #95d5b2; line-height: 1.6;">{subsidy['description']}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"📋 {T['view_details']} — {subsidy['title']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**✅ {T['eligibility']}**")
                st.write(subsidy["eligibility"])
                st.markdown(f"**📝 {T['how_to_apply']}**")
                st.write(subsidy["how_to_apply"])
            with col2:
                st.markdown(f"**📁 {T['documents']}**")
                for doc in subsidy["documents"]:
                    st.markdown(f"• {doc}")
            st.button(T["interested"], key=f"interest_btn_{subsidy['id']}", type="primary")

        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🔔 {T["notify_title"]}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        notify_name = st.text_input(T["notify_name"], key="notify_name")
    with col2:
        notify_phone = st.text_input(T["notify_phone"], key="notify_phone")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(T["subscribe"], key="notify_submit", use_container_width=True, type="primary"):
            if notify_name.strip() == "" or notify_phone.strip() == "":
                st.error(T["notify_error"])
            else:
                st.success(f"✅ {notify_name}, {T['notify_success']}")