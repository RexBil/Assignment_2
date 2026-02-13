
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Online Food Delivery Analytics Dashboard")
st.markdown("### Data-Driven Business Insights")

# =========================
# DATABASE CONNECTION
# =========================
engine = create_engine(
    "mysql+mysqlconnector://root:Test%40123@localhost/food_delivery_db"
)

df = pd.read_sql("SELECT * FROM orders", engine)

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filter Options")

selected_city = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

selected_cuisine = st.sidebar.multiselect(
    "Select Cuisine",
    options=df["Cuisine_Type"].unique(),
    default=df["Cuisine_Type"].unique()
)

df = df[
    (df["City"].isin(selected_city)) &
    (df["Cuisine_Type"].isin(selected_cuisine))
]

# =========================
# KPI CALCULATIONS
# =========================
total_orders = df["Order_ID"].nunique()
total_revenue = df["Final_Amount"].sum()
avg_order_value = df["Final_Amount"].mean()
avg_delivery = df["Delivery_Time_Min"].mean()
cancel_rate = (df["Order_Status"] == "Cancelled").mean() * 100
profit_margin = df["Profit_Margin_%"].mean()

# =========================
# KPI DISPLAY (Professional Layout)
# =========================
col1, col2, col3, col4, col5, col6 = st.columns(6)

st.metric("📦 Total Orders", f"{total_orders:,}")
st.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
st.metric("🛒 Avg Order Value", f"₹{avg_order_value:,.2f}")
st.metric("🚚 Avg Delivery Time", f"{avg_delivery:.2f} min")
st.metric("❌ Cancellation Rate", f"{cancel_rate:.2f}%")
st.metric("📊 Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# =========================
# MONTHLY REVENUE TREND
# =========================
st.subheader("📅 Monthly Revenue Trend")

monthly_revenue = (
    df.groupby("Month")["Final_Amount"]
    .sum()
    .reset_index()
    .sort_values("Month")
)

fig_month = px.line(
    monthly_revenue,
    x="Month",
    y="Final_Amount",
    markers=True,
    title="Monthly Revenue Trend",
    labels={"Final_Amount": "Revenue"}
)

st.plotly_chart(fig_month, use_container_width=True)

# =========================
# REVENUE BY CITY (ADVANCED)
# =========================
st.subheader("🏙 Revenue by City - Monthly Comparison")

# Group by City & Month
city_month = (
    df.groupby(["City", "Month"])["Final_Amount"]
    .sum()
    .reset_index()
)

# Get latest month
latest_month = city_month["Month"].max()
previous_month = latest_month - 1

current_data = city_month[city_month["Month"] == latest_month]
previous_data = city_month[city_month["Month"] == previous_month]

# Merge for comparison
comparison = pd.merge(
    current_data,
    previous_data,
    on="City",
    how="left",
    suffixes=("_Current", "_Previous")
)

comparison["Growth_%"] = (
    (comparison["Final_Amount_Current"] - comparison["Final_Amount_Previous"])
    / comparison["Final_Amount_Previous"]
) * 100

comparison = comparison.sort_values(
    "Final_Amount_Current", ascending=False
).head(10)

# =========================
# PLOTLY BAR CHART
# =========================

fig_city = px.bar(
    comparison,
    x="City",
    y="Final_Amount_Current",
    color="Growth_%",
    text="Final_Amount_Current",
    color_continuous_scale="Viridis",
    title=f"Top 10 Cities Revenue - Month {latest_month}"
)

fig_city.update_traces(
    texttemplate="₹%{text:,.0f}",
    textposition="outside"
)

fig_city.update_layout(
    xaxis_title="City",
    yaxis_title="Revenue",
    xaxis_tickangle=-45,
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

st.plotly_chart(fig_city, use_container_width=True)

# =========================
# CUISINE PERFORMANCE
# =========================
st.subheader("🍕 Revenue by Cuisine")

cuisine_revenue = (
    df.groupby("Cuisine_Type")["Final_Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_cuisine = px.pie(
    cuisine_revenue.head(8),
    names="Cuisine_Type",
    values="Final_Amount",
    hole=0.4,
    title="Cuisine Revenue Distribution"
)

st.plotly_chart(fig_cuisine, use_container_width=True)
