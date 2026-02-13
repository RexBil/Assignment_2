
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
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🍔 Online Food Delivery Analytics Dashboard")
st.markdown("### Business Performance Dashboard")

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

top_bottom_toggle = st.sidebar.radio(
    "Select View",
    ["Top 5", "Bottom 5"]
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
avg_rating = df["Delivery_Rating"].mean()

# =========================
# KPI CARDS WITH COLOR ARROWS
# =========================

metrics_data = [
    {"label": "📦 Total Orders", "value": f"{total_orders:,}"},
    {"label": "💰 Total Revenue", "value": f"₹{total_revenue:,.2f}"},
    {"label": "🛒 Avg Order Value", "value": f"₹{avg_order_value:,.2f}"},
    {"label": "🚚 Avg Delivery Time", "value": f"{avg_delivery:.2f} min"},
    {"label": "❌ Cancellation Rate", "value": f"{cancel_rate:.2f}%"},
    {"label": "📊 Profit Margin", "value": f"{profit_margin:.2f}%"},
    {"label": "⭐ Avg Delivery Rating", "value": f"{avg_rating:.2f}"},
]
st.markdown("---")
num_cols = 3
# Loop through the metrics list 3 at a time
for i in range(0, len(metrics_data), num_cols):
    cols = st.columns(num_cols)
    
    # Place metrics in the current row's columns
    for j in range(num_cols):
        index = i + j
        if index < len(metrics_data):
            m = metrics_data[index]
            cols[j].metric(label=m["label"], value=m["value"])
    
    # Add vertical space between rows
    st.write("") 

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
    labels={"Final_Amount": "Revenue"},
    template="plotly_dark"
)

st.plotly_chart(fig_month, use_container_width=True)

# =========================
# REVENUE BY CITY (TOP/BOTTOM 5)
# =========================
st.subheader("🏙 Revenue by City")

city_revenue = (
    df.groupby("City")["Final_Amount"]
    .sum()
    .reset_index()
    .sort_values("Final_Amount", ascending=(top_bottom_toggle=="Bottom 5"))
)

fig_city = px.bar(
    city_revenue.head(5),
    x="City",
    y="Final_Amount",
    text="Final_Amount",
    title=f"{top_bottom_toggle} Cities by Revenue",
    color="Final_Amount",
    color_continuous_scale="Viridis",
    template="plotly_dark"
)

fig_city.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
fig_city.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_city, use_container_width=True)

# =========================
# CUISINE PERFORMANCE (TOP/BOTTOM 5)
# =========================
st.subheader("🍕 Revenue by Cuisine")

cuisine_revenue = (
    df.groupby("Cuisine_Type")["Final_Amount"]
    .sum()
    .reset_index()
    .sort_values("Final_Amount", ascending=(top_bottom_toggle=="Bottom 5"))
)

fig_cuisine = px.bar(
    cuisine_revenue.head(5),
    x="Cuisine_Type",
    y="Final_Amount",
    text="Final_Amount",
    title=f"{top_bottom_toggle} Cuisines by Revenue",
    color="Final_Amount",
    color_continuous_scale="Viridis",
    template="plotly_dark"
)

fig_cuisine.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
fig_cuisine.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig_cuisine, use_container_width=True)

# =========================
# DELIVERY TIME vs RATING SCATTER
# =========================
st.subheader("🚚 Delivery Time vs Rating (Impact Analysis)")

# =========================
# CREATE DELIVERY TIME BUCKETS
# =========================
df["Delivery_Time_Bucket"] = pd.cut(
    df["Delivery_Time_Min"],
    bins=[0, 20, 30, 40, 50, 60, 120],
    labels=["0-20", "20-30", "30-40", "40-50", "50-60", "60+"]
)

# =========================
# GROUP DATA
# =========================
rating_analysis = (
    df.groupby("Delivery_Time_Bucket")
    .agg(
        Avg_Rating=("Delivery_Rating", "mean"),
        Order_Count=("Order_ID", "count")
    )
    .reset_index()
)

# Remove empty buckets
rating_analysis = rating_analysis.dropna()

# =========================
# BAR CHART
# =========================
fig_bar = px.bar(
    rating_analysis,
    x="Delivery_Time_Bucket",
    y="Avg_Rating",
    text="Avg_Rating",
    color="Avg_Rating",
    color_continuous_scale="Viridis",
    template="plotly_dark",
    title="Average Delivery Rating by Delivery Time Range"
)

fig_bar.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_bar.update_layout(
    xaxis_title="Delivery Time Range (Minutes)",
    yaxis_title="Average Delivery Rating",
    yaxis=dict(range=[0, 5])
)

st.plotly_chart(fig_bar, use_container_width=True)

# =========================
# CANCELLATION REASON BREAKDOWN
# =========================
st.subheader("❌ Cancellation Reason Breakdown")

cancel_data = (
    df[df["Order_Status"]=="Cancelled"]
    .groupby("Cancellation_Reason")["Order_ID"]
    .count()
    .reset_index()
    .sort_values("Order_ID", ascending=False)
)

fig_cancel = px.pie(
    cancel_data,
    names="Cancellation_Reason",
    values="Order_ID",
    title="Cancellation Reasons Distribution",
    hole=0.4,
    template="plotly_dark"
)

st.plotly_chart(fig_cancel, use_container_width=True)
