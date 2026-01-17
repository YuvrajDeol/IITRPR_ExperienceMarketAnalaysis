import streamlit as st
import pandas as pd

st.set_page_config(page_title="Show Forecast Dashboard", layout="wide")

st.title("🎯 Show Forecast Dashboard")
st.caption("Show Type → City → Month → Price → Recommendation (Add / Remove / Increase / Decrease)")

@st.cache_data
def load_data():
    return pd.read_csv("final_trends_seasonality.csv")

df = load_data()

# -----------------------------
# Show Type -> Keyword mapping
# -----------------------------
category_map = {
    "Concert": [
        "Music Festival India: (India)",
        "Sunburn Festival: (India)",
        "Lollapalooza India: (India)",
        "Coldplay India: (India)",
        "Diljit Dosanjh tour: (India)",
        "Karan Aujla concert: (India)"
    ],
    "Standup": [
        "Stand up comedy near me: (India)",
        "Comedy show tickets: (India)",
        "Comedy club: (India)",
        "Zakir Khan: (India)",
        "Samay Raina: (India)",
        "Abhishek Upmanyu: (India)",
        "Anubhav Singh Bassi: (India)"
    ],
    "Workshop": [
        "Pottery workshop: (India)",
        "Painting workshop: (India)"
    ]
}

# -----------------------------
# City payment power multiplier (heuristic)
# -----------------------------
city_multiplier = {
    "Mumbai": 1.30,
    "Delhi": 1.25,
    "Bengaluru": 1.20,
    "Bangalore": 1.20,
    "Gurgaon": 1.20,
    "Gurugram": 1.20,
    "Noida": 1.15,
    "Hyderabad": 1.15,
    "Pune": 1.15,
    "Chennai": 1.10,
    "Kolkata": 1.05,
    "Ahmedabad": 1.00,
    "Surat": 0.98,
    "Jaipur": 0.98,
    "Chandigarh": 1.05,
    "Lucknow": 0.95,
    "Indore": 0.95,
    "Vadodara": 0.95,
    "Bhopal": 0.92,
    "Nagpur": 0.92,
    "Coimbatore": 0.92,
    "Visakhapatnam": 0.92,
    "Patna": 0.85,
    "Ranchi": 0.85,
    "Raipur": 0.88,
    "Guwahati": 0.88,
    "Bhubaneswar": 0.90,
    "Kanpur": 0.88,
    "Varanasi": 0.88,
    "Ludhiana": 0.90,
    "Amritsar": 0.90,
    "Jalandhar": 0.90
}

# -----------------------------
# Base prices (category baseline)
# -----------------------------
base_price = {
    "Concert": 3500,
    "Standup": 1200,
    "Workshop": 800
}

# -----------------------------
# Inputs
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    show_type = st.selectbox("Select Show Type", ["Concert", "Standup", "Workshop"])
with col2:
    city = st.selectbox(
        "Select City / Market",
        sorted(city_multiplier.keys())
    )

month_choice = st.selectbox(
    "Target Month",
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
)

price = st.slider("Your Planned Ticket Price (₹)", min_value=0, max_value=20000, value=2000, step=100)

month_map = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
target_month = month_map[month_choice]

# -----------------------------
# Demand calc (India-level)
# -----------------------------
keywords = category_map[show_type]
subset = df[(df["Keyword"].isin(keywords)) & (df["Month"] == target_month)]

avg_demand = float(subset["Demand_Index"].mean()) if len(subset) else 0.0
avg_trend = float(subset["Trend_Score"].mean()) if len(subset) else 0.0

mult = city_multiplier.get(city, 1.00)
city_adjusted_demand = avg_demand * mult

# -----------------------------
# NEW: Recommended Price formula
# -----------------------------
# demand_factor: neutral at 50, higher demand increases price
demand_factor = city_adjusted_demand / 50.0
demand_factor = max(0.70, min(demand_factor, 1.60))  # clamp

recommended_price = base_price[show_type] * mult * demand_factor
recommended_price = int(round(recommended_price / 100) * 100)  # round to nearest 100

# -----------------------------
# Recommendation (price vs recommended)
# -----------------------------
def price_action(demand, user_price, rec_price):
    # If demand is extremely low, pause regardless
    if demand < 25:
        return "REMOVE / PAUSE", "Demand is too low for this month. Pause or shift month/city."

    # Compare user price with recommended price
    diff = user_price - rec_price
    diff_pct = diff / max(rec_price, 1)

    if diff_pct < -0.15:
        return "INCREASE PRICE", f"Your price is low vs recommended ₹{rec_price}."
    elif diff_pct > 0.15:
        return "DECREASE PRICE", f"Your price is high vs recommended ₹{rec_price}."
    else:
        return "KEEP", f"Your price is close to recommended ₹{rec_price}."

action, reason = price_action(city_adjusted_demand, price, recommended_price)

# -----------------------------
# Display
# -----------------------------
st.subheader("📌 Demand Snapshot")
m1, m2, m3 = st.columns(3)
m1.metric("Avg Demand Index (Month)", round(avg_demand, 2))
m2.metric("City Multiplier", mult)
m3.metric("City Adjusted Demand", round(city_adjusted_demand, 2))

st.subheader("💰 Pricing Recommendation")
p1, p2 = st.columns(2)
p1.metric("Recommended Price (₹)", recommended_price)
p2.metric("Your Price (₹)", price)

st.subheader("✅ Final Recommendation")
st.write(f"**Action:** {action}")
st.write(f"**Reason:** {reason}")

# -----------------------------
# Plan table (optional)
# -----------------------------
st.divider()
st.subheader("📋 Plan Table")

if "plan" not in st.session_state:
    st.session_state.plan = pd.DataFrame(columns=[
        "Show_Type","City","Month","Your_Price","Recommended_Price",
        "Adj_Demand","Recommendation"
    ])

if st.button("➕ Add to Plan"):
    row = {
        "Show_Type": show_type,
        "City": city,
        "Month": month_choice,
        "Your_Price": price,
        "Recommended_Price": recommended_price,
        "Adj_Demand": round(city_adjusted_demand, 2),
        "Recommendation": action
    }
    st.session_state.plan = pd.concat([st.session_state.plan, pd.DataFrame([row])], ignore_index=True)
    st.success("Added.")

st.dataframe(st.session_state.plan, use_container_width=True)

st.download_button(
    "⬇️ Download Plan CSV",
    data=st.session_state.plan.to_csv(index=False).encode("utf-8"),
    file_name="show_plan.csv",
    mime="text/csv"
)
