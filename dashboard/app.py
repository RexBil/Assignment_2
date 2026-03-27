"""
Streamlit Dashboard — Online Food Delivery Analysis
All data fetched from MySQL via SQL queries.

Run:
    1. python scripts/db_upload.py        (upload data to MySQL first)
    2. streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

st.set_page_config(
    page_title="🍔 Food Delivery Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
)

st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        color: white;
        margin-bottom: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .kpi-label { font-size: 12px; opacity: 0.85; margin-bottom: 4px; }
    .kpi-value { font-size: 22px; font-weight: 800; }
    .section-title {
        font-size: 18px; font-weight: 700;
        border-left: 4px solid #2d6a9f;
        padding-left: 10px; margin: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

engine = create_engine(
    "mysql+pymysql://root:Test%40123@localhost/food_delivery_db",
    pool_pre_ping=True
)

# -------------------------------------------------
# Function to load SQL queries
# -------------------------------------------------
def load_queries(path):
    queries = {}
    with open(path, "r") as file:
        sql = file.read()

    parts = sql.split("-- ── Task :")
    for part in parts[1:]:
        name, query = part.split("\n", 1)
        queries[name.strip()] = query.strip()

    return queries

queries = load_queries("sql/analytical_queries.sql")

def get_query(name, WHERE=""):
    if name not in queries:
        raise ValueError(f"Query '{name}' not found. Available: {list(queries.keys())}")
    
    query = queries[name]
    return query.replace("{{WHERE}}", WHERE)

@st.cache_data
def run_query(query, _engine):
    with _engine.connect() as conn:
        return pd.read_sql(query, conn)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🍔 Online Food Delivery Analytics Dashboard")

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

all_cities = ['All'] + run_query(get_query("All Cities", ""), engine)['City'].tolist()
all_cuisines = ['All'] + run_query(get_query("Country Type", ""), engine)['Cuisine_Type'].tolist()
all_statuses = ['All'] + run_query(get_query("Cancel Status", ""), engine)['Order_Status'].tolist()

sel_city    = st.sidebar.selectbox("City",         all_cities)
sel_cuisine = st.sidebar.selectbox("Cuisine Type", all_cuisines)
sel_status  = st.sidebar.selectbox("Order Status", all_statuses)

# Filters
conditions = []

if sel_city != 'All':
    conditions.append(f"City = '{sel_city}'")

if sel_cuisine != 'All':
    conditions.append(f"Cuisine_Type = '{sel_cuisine}'")

if sel_status != 'All':
    conditions.append(f"Order_Status = '{sel_status}'")

WHERE = " AND " + " AND ".join(conditions) if conditions else ""


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────
def show_fig(fig):
    st.pyplot(fig)
    plt.close(fig)

def Q(sql): 
    return run_query(sql, engine)

# ─────────────────────────────────────────────
# KPI CARDS — pure SQL
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

kpi = run_query(get_query("KPI Summary", WHERE), engine)
kpi = kpi.iloc[0]

kpis = [
    ("🛒 Total Orders",        f"{int(kpi['total_orders']):,}"),
    ("💰 Total Revenue",       f"₹{kpi['total_revenue']:,.0f}"),
    ("🧾 Avg Order Value",     f"₹{kpi['avg_order_value']:,.2f}"),
    ("🚴 Avg Delivery Time",   f"{kpi['avg_delivery_time']:.1f} min"),
    ("❌ Cancellation Rate",   f"{kpi['cancel_rate']:.1f}%"),
    ("⭐ Avg Delivery Rating", f"{kpi['avg_rating']:.2f}"),
    ("📈 Avg Profit Margin",   f"{kpi['avg_profit_margin']:.1f}%"),
]

cols = st.columns(7)
for col, (label, value) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════
# SECTION 1 — CUSTOMER & ORDER ANALYSIS
# ══════════════════════════════════════════════
st.markdown('<div class="section-title">👥 Customer & Order Analysis</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Task 1 — Top 10 Spending Customers
with col1:
    st.markdown("**Task 1 — Top 10 Spending Customers**")
    df1 = run_query(get_query("Top 10 Spending Customers", WHERE), engine)
    fig = px.bar(
        df1,
        x="total_spend",
        y=df1['Customer_ID'].astype(str),
        orientation='h',
    )
    fig.update_traces(
        hovertemplate="Customer: %{y}<br>Spend: ₹%{x}<extra></extra>"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

# Task 2 — Age Group vs Order Value
with col2:
    st.markdown("**Task 2 — Age Group vs Order Value**")
    df2 = run_query(get_query("Age Group vs Order Value", WHERE), engine)
    fig = px.bar(
        df2,
        x="customer_age_group",
        y="avg_value",
        color_discrete_sequence=["#22C55E"]
    )
    fig.update_traces(
        hovertemplate="Age Group: %{x}<br>Avg Value: ₹%{y}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

# Task 3 — Weekend vs Weekday
with col3:
    st.markdown("**Task 3 — Weekend vs Weekday**")
    df3 = run_query(get_query("Weekend vs Weekday Order Patterns", WHERE), engine)
    color_map = {
        "Weekday": "#4F46E5",  # blue
        "Weekend": "#EF4444"   # red
    }
    fig1 = px.bar(
            df3,
            x="order_day_type",
            y="order_count",
            color="order_day_type",
            color_discrete_map=color_map
        )
    st.plotly_chart(fig1, use_container_width=True)

# ══════════════════════════════════════════════
# SECTION 2 — REVENUE & PROFIT
# ══════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">💰 Revenue & Profit Analysis</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Task 4 — Monthly Revenue
with col1:
    st.markdown("**Task 4 — Monthly Revenue Trend**")  
    df4 = run_query(get_query("Monthly Revenue Trends", WHERE), engine)
    fig = px.line(
        df4,
        x="month",
        y="revenue",
        markers=True,
    )
    fig.update_traces(
        hovertemplate="Month: %{x}<br>Revenue: ₹%{y}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)

# Task 5 — Discount Impact on Profit

with col2:
    st.markdown("**Task 5 — Discount Impact on Profit**")
    df5 = run_query(get_query("Discount Impact on Profit", WHERE), engine)
    fig = px.bar(
        df5,
        x="discount_tier",
        y="avg_profit_margin",
    )
    fig.update_traces(
        hovertemplate="Discount: %{x}<br>Profit: %{y:.2f}%<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True)


# Task 6 — High Revenue Cities & Cuisines
with col3:
    st.markdown("**Task 6 — High-Revenue Cities & Cuisines**")

    df6a = run_query(get_query("High-Revenue Cities", WHERE), engine) 
    df6b = run_query(get_query("High-Revenue Country", WHERE), engine)

    col6_1, col6_2 = st.columns(2)
    # 🔹 Chart 1 — Top Cities
    with col6_1:
        fig1 = px.bar(
            df6a,
            x="revenue",
            y="City",
            orientation='h',
            title="Top 5 Cities",
            color_discrete_sequence=["#22C55E"]  # green theme
        )
        fig1.update_traces(
            hovertemplate="City: %{y}<br>Revenue: ₹%{x}<extra></extra>"
        )
        fig1.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig1, use_container_width=True)

    # 🔹 Chart 2 — Top Cuisines
    with col6_2:
        fig2 = px.bar(
            df6b,
            x="revenue",
            y="Cuisine_Type",
            orientation='h',
            title="Top 5 Countries",
            color_discrete_sequence=["#A855F7"]  # purple theme
        )
        fig2.update_traces(
            hovertemplate="Cuisine: %{y}<br>Revenue: ₹%{x}<extra></extra>"
        )
        fig2.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════
# SECTION 3 — DELIVERY PERFORMANCE
# ══════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">🚴 Delivery Performance</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# Task 7 — Avg Delivery Time by City
with col1:
    st.markdown("**Task 7 — Delivery Time by City**")
    df7 = run_query(get_query("Avg Delivery Time by City", WHERE), engine)
    fig = px.bar(
        df7,
        x="avg_time",
        y="City",
        orientation='h',
        color_discrete_sequence=["#EF4444"]  # 🔥 red (delivery time = delay)
    )
    fig.update_traces(
        hovertemplate="City: %{y}<br>Avg Time: %{x:.2f} min<extra></extra>"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

# Task 8 — Distance vs Delivery Delay
# with col2:
#     st.markdown("**Task 8 — Distance vs Delivery Delay**")
#     df8 =run_query(get_query("Distance vs Delivery Delay", WHERE), engine)
#     fig = px.scatter(
#         df8,
#         x="Distance_km",
#         y="Delivery_Time_Min",
#         trendline="ols",
#     )
#     fig.update_traces(
#         marker=dict(size=6, opacity=0.4),
#         hovertemplate="Distance: %{x} km<br>Time: %{y} min<extra></extra>"
#     )
#     st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Task 8 — Distance vs Delivery Delay**")
    df8 = run_query(get_query("Distance vs Delivery Delay", WHERE), engine)
    # Scatter plot
    fig = px.scatter(
        df8,
        x="Distance_km",
        y="Delivery_Time_Min",
        opacity=0.3,
    )

    # 🔥 Manual regression line (NO statsmodels)
    m, b = np.polyfit(df8['Distance_km'], df8['Delivery_Time_Min'], 1)
    x_range = np.linspace(df8['Distance_km'].min(), df8['Distance_km'].max(), 100)
    y_range = m * x_range + b
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=y_range,
            mode='lines',
            name='Trendline'
        )
    )

    # Correlation
    corr = df8[['Distance_km','Delivery_Time_Min']].corr().iloc[0,1]
    st.plotly_chart(fig, use_container_width=True)


# Task 9 — Rating vs Delivery Time
with col3:
    st.markdown("**Task 9 — Rating vs Delivery Time**")
    df9 = run_query(get_query("Delivery Rating vs Delivery Time", WHERE), engine)
    fig = px.bar(
        df9,
        x="rating",
        y="avg_time",
        color="avg_time",
        color_continuous_scale="RdYlGn_r",
    )
    st.plotly_chart(fig, use_container_width=True)

# Task 10 — Top Rated Restaurants
with col1:
    st.markdown("**Task 10 — Top Rated Restaurants**")
    df10 = run_query(get_query("Top Rated Restaurants", WHERE), engine)
    fig = px.bar(
        df10,
        x="avg_rating",
        y="Restaurant_Name",
        orientation='h',
        color_discrete_sequence=["#F59E0B"]
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

# Task 11 — Cancellation Rate by Restaurant
with col2:
    st.markdown("**Task 11 — Cancellation Rate by Restaurant**")
    df11 = run_query(get_query("Cancellation Rate by Restaurant", WHERE), engine)
    fig = px.bar(
        df11,
        x="cancel_rate",
        y="Restaurant_Name",
        orientation='h',
        color_discrete_sequence=["#EF4444"]
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

# Task 12 — Cuisine-wise Performance
with col3:
    st.markdown("**Task 12 — Cuisine-wise Performance**")
    df12 = run_query(get_query("Cuisine-wise Performance", WHERE), engine)
    colA, colB = st.columns(2)

    with colA:
        fig1 = px.bar(df12, x="Cuisine_Type", y="avg_value",
                      color_discrete_sequence=["#06B6D4"],
                      title="Avg Order Value")
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(df12, x="Cuisine_Type", y="avg_rating",
                      color_discrete_sequence=["#F59E0B"],
                      title="Avg Rating")
        st.plotly_chart(fig2, use_container_width=True)

# Task 13 — Peak vs Non-Peak
with col1:
    st.markdown("**Task 13 — Peak vs Non-Peak Demand**")
    df13 = run_query(get_query("Peak Hour Demand", WHERE), engine)
    colA, colB = st.columns(2)

    with colA:
        fig1 = px.bar(df13, x="hour_type", y="order_count",
                      color="hour_type",
                      color_discrete_map={"Peak Hour":"#EF4444","Non-Peak":"#3B82F6"})
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(df13, x="hour_type", y="avg_value",
                      color="hour_type",
                      color_discrete_map={"Peak Hour":"#EF4444","Non-Peak":"#3B82F6"})
        st.plotly_chart(fig2, use_container_width=True)

# Task 14 — Payment Mode Preferences
with col2:
    st.markdown("**Task 14 — Payment Mode Preferences**")
    df14 = run_query(get_query("Payment Mode Preferences", WHERE), engine)
    fig = px.pie(
        df14,
        names="Payment_Mode",
        values="cnt",
    )
    st.plotly_chart(fig, use_container_width=True)

# Task 15 — Cancellation Reasons
with col3:
    st.markdown("**Task 15 — Cancellation Reasons**")
    df15 = run_query(get_query("Cancellation Reason Analysis", WHERE), engine)
    if not df15.empty:
        fig = px.pie(
            df15,
            names="Cancellation_Reason",
            values="cnt",
        )
        st.plotly_chart(fig, use_container_width=True)

# # ── RAW DATA TABLE (SQL) ──────────────────────────────────────────
# st.markdown("---")
# with st.expander("📋 View Raw Data from Database (first 500 rows)"):
#     df_raw_view = Q(f"""
#         SELECT Order_ID, Customer_ID, City, Cuisine_Type,
#                Order_Value, Discount_Applied, Delivery_Time_Min,
#                Order_Status, Restaurant_Name, Restaurant_Rating,
#                Delivery_Rating, Profit_Margin
#         FROM food_orders {WHERE}
#         LIMIT 500
#     """)
#     st.dataframe(df_raw_view, use_container_width=True)

# st.markdown("---")
# st.markdown("📊 **Online Food Delivery Analysis** · MySQL + Streamlit + Matplotlib")
