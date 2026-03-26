"""
Streamlit Dashboard — Online Food Delivery Analysis
Run: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🍔 Food Delivery Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .section-title { font-size: 18px; font-weight: 700;
                     border-left: 4px solid #2d6a9f;
                     padding-left: 10px; margin: 20px 0 10px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, 'data', 'cleaned', 'featured_food_delivery.csv')
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    # Convert Profit_Margin from fraction to percentage if needed
    if 'Profit_Margin' in df.columns and df['Profit_Margin'].abs().max() <= 1.5:
        df['Profit_Margin'] = df['Profit_Margin'] * 100
    return df

df_raw = load_data()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.title("🍔 Online Food Delivery — Business Intelligence Dashboard")
st.markdown("**Data-driven insights on 100,000 orders · Customer · Revenue · Delivery · Restaurant**")

if df_raw is None:
    st.error("⚠️  Dataset not found. Run `python main.py --step all` first.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

min_date = df_raw['Order_Date'].min()
max_date = df_raw['Order_Date'].max()
date_range = st.sidebar.date_input("Date Range",
    value=(min_date.date(), max_date.date()),
    min_value=min_date.date(), max_value=max_date.date())

all_cities   = ['All'] + sorted(df_raw['City'].dropna().unique().tolist())
all_cuisines = ['All'] + sorted(df_raw['Cuisine_Type'].dropna().unique().tolist())
all_statuses = ['All'] + sorted(df_raw['Order_Status'].dropna().unique().tolist())

sel_city    = st.sidebar.selectbox("City",         all_cities)
sel_cuisine = st.sidebar.selectbox("Cuisine Type", all_cuisines)
sel_status  = st.sidebar.selectbox("Order Status", all_statuses)

# Apply filters
df = df_raw.copy()
if len(date_range) == 2:
    df = df[(df['Order_Date'] >= pd.Timestamp(date_range[0])) &
            (df['Order_Date'] <= pd.Timestamp(date_range[1]))]
if sel_city    != 'All': df = df[df['City']         == sel_city]
if sel_cuisine != 'All': df = df[df['Cuisine_Type'] == sel_cuisine]
if sel_status  != 'All': df = df[df['Order_Status'] == sel_status]

st.sidebar.markdown(f"**Filtered Records:** {len(df):,}")

# ─────────────────────────────────────────────
# KPI CARDS  — FIX: compute directly from data
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

total_orders   = len(df)
total_revenue  = df['Order_Value'].sum()
avg_order_val  = df['Order_Value'].mean()
avg_del_time   = df['Delivery_Time_Min'].mean()
cancel_rate    = df['Order_Status'].str.lower().str.contains('cancel', na=False).mean() * 100
avg_rating     = df['Delivery_Rating'].mean()
avg_margin     = df['Profit_Margin'].mean()   # already converted to % on load

kpis = [
    ("🛒 Total Orders",          f"{total_orders:,}"),
    ("💰 Total Revenue",         f"₹{total_revenue:,.0f}"),
    ("🧾 Avg Order Value",       f"₹{avg_order_val:,.2f}"),
    ("🚴 Avg Delivery Time",     f"{avg_del_time:.1f} min"),
    ("❌ Cancellation Rate",     f"{cancel_rate:.1f}%"),
    ("⭐ Avg Delivery Rating",   f"{avg_rating:.2f}"),
    ("📈 Avg Profit Margin",     f"{avg_margin:.1f}%"),
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

# ─────────────────────────────────────────────
# HELPER: matplotlib figure → streamlit
# ─────────────────────────────────────────────
def show_fig(fig):
    st.pyplot(fig)
    plt.close(fig)

# ─────────────────────────────────────────────
# ALL 15 ANALYTICS TASKS
# ─────────────────────────────────────────────

# ── SECTION 1: CUSTOMER & ORDER ANALYSIS ─────────────────────────
st.markdown('<div class="section-title">👥 Customer & Order Analysis</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Task 1 — Top 10 Spending Customers**")
    top_cust = df.groupby('Customer_ID')['Order_Value'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top_cust.index.astype(str), top_cust.values, color='steelblue')
    ax.set_xlabel('Total Spend (₹)')
    ax.invert_yaxis()
    ax.set_title('Top 10 Customers by Spend')
    plt.tight_layout()
    show_fig(fig)

with col2:
    st.markdown("**Task 2 — Age Group vs Order Value**")
    if 'customer_age_group' in df.columns:
        grp = df.groupby('customer_age_group', observed=True)['Order_Value'].mean()
        fig, ax = plt.subplots(figsize=(6, 4))
        grp.plot(kind='bar', ax=ax, color='coral', edgecolor='white')
        ax.set_title('Avg Order Value by Age Group')
        ax.set_ylabel('Avg Value (₹)')
        ax.set_xlabel('Age Group')
        plt.xticks(rotation=0)
        plt.tight_layout()
        show_fig(fig)

with col3:
    st.markdown("**Task 3 — Weekend vs Weekday**")
    day_col = 'order_day_type' if 'order_day_type' in df.columns else 'Order_Day'
    if day_col in df.columns:
        grp = df.groupby(day_col)['Order_Value'].agg(['count','mean'])
        fig, axes = plt.subplots(1, 2, figsize=(6, 4))
        axes[0].bar(grp.index, grp['count'], color=['#66b3ff','#ff9999'])
        axes[0].set_title('Order Count')
        axes[0].tick_params(axis='x', rotation=0)
        axes[1].bar(grp.index, grp['mean'], color=['#66b3ff','#ff9999'])
        axes[1].set_title('Avg Value (₹)')
        axes[1].tick_params(axis='x', rotation=0)
        plt.tight_layout()
        show_fig(fig)

# ── SECTION 2: REVENUE & PROFIT ───────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">💰 Revenue & Profit Analysis</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Task 4 — Monthly Revenue Trend**")
    tmp = df.dropna(subset=['Order_Date'])
    monthly = tmp.groupby(tmp['Order_Date'].dt.to_period('M'))['Order_Value'].sum()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(monthly.index.astype(str), monthly.values, marker='o', color='royalblue', linewidth=2)
    ax.fill_between(range(len(monthly)), monthly.values, alpha=0.15, color='royalblue')
    ax.set_title('Monthly Revenue Trend')
    ax.set_ylabel('Revenue (₹)')
    plt.xticks(range(len(monthly)), monthly.index.astype(str), rotation=45, fontsize=7)
    plt.tight_layout()
    show_fig(fig)

with col2:
    st.markdown("**Task 5 — Discount Impact on Profit**")
    buckets = pd.cut(df['Discount_Applied'], bins=5)
    disc_profit = df.groupby(buckets, observed=True)['Profit_Margin'].mean()
    fig, ax = plt.subplots(figsize=(6, 4))
    disc_profit.plot(kind='bar', ax=ax, color='mediumpurple', edgecolor='white')
    ax.set_title('Profit Margin by Discount Tier')
    ax.set_xlabel('Discount Range')
    ax.set_ylabel('Avg Profit Margin (%)')
    plt.xticks(rotation=25, fontsize=7)
    plt.tight_layout()
    show_fig(fig)

with col3:
    st.markdown("**Task 6 — High-Revenue Cities & Cuisines**")
    fig, axes = plt.subplots(1, 2, figsize=(6, 4))
    city_rev = df.groupby('City')['Order_Value'].sum().sort_values(ascending=False).head(5)
    axes[0].barh(city_rev.index, city_rev.values, color='seagreen')
    axes[0].set_title('Top 5 Cities', fontsize=9)
    axes[0].invert_yaxis()
    axes[0].tick_params(labelsize=7)
    cuisine_rev = df.groupby('Cuisine_Type')['Order_Value'].sum().sort_values(ascending=False).head(5)
    axes[1].barh(cuisine_rev.index, cuisine_rev.values, color='orchid')
    axes[1].set_title('Top 5 Cuisines', fontsize=9)
    axes[1].invert_yaxis()
    axes[1].tick_params(labelsize=7)
    plt.tight_layout()
    show_fig(fig)

# ── SECTION 3: DELIVERY PERFORMANCE ──────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">🚴 Delivery Performance</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Task 7 — Avg Delivery Time by City**")
    city_time = df.groupby('City')['Delivery_Time_Min'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(city_time.index, city_time.values, color='tomato')
    ax.set_xlabel('Avg Delivery Time (min)')
    ax.set_title('Delivery Time by City')
    ax.invert_yaxis()
    plt.tight_layout()
    show_fig(fig)

with col2:
    st.markdown("**Task 8 — Distance vs Delivery Delay**")
    tmp = df[['Distance_km','Delivery_Time_Min']].dropna().sample(min(5000, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(tmp['Distance_km'], tmp['Delivery_Time_Min'], alpha=0.2, s=5, color='teal')
    m, b = np.polyfit(tmp['Distance_km'], tmp['Delivery_Time_Min'], 1)
    x = np.linspace(tmp['Distance_km'].min(), tmp['Distance_km'].max(), 100)
    ax.plot(x, m*x+b, color='red', linewidth=2)
    corr = tmp[['Distance_km','Delivery_Time_Min']].corr().iloc[0,1]
    ax.set_title(f'Distance vs Delay (r={corr:.2f})')
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Delivery Time (min)')
    plt.tight_layout()
    show_fig(fig)

with col3:
    st.markdown("**Task 9 — Rating vs Delivery Time**")
    rat_time = df.groupby('Delivery_Rating')['Delivery_Time_Min'].mean().sort_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(rat_time.index.astype(str), rat_time.values,
                  color=sns.color_palette('RdYlGn', len(rat_time)))
    ax.set_title('Avg Delivery Time by Rating')
    ax.set_xlabel('Delivery Rating')
    ax.set_ylabel('Avg Time (min)')
    plt.tight_layout()
    show_fig(fig)

# ── SECTION 4: RESTAURANT PERFORMANCE ────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">🍽️ Restaurant Performance</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Task 10 — Top Rated Restaurants**")
    counts   = df['Restaurant_Name'].value_counts()
    eligible = counts[counts >= 30].index
    top_rest = (df[df['Restaurant_Name'].isin(eligible)]
                .groupby('Restaurant_Name')['Restaurant_Rating']
                .mean().sort_values(ascending=False).head(10))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top_rest.index, top_rest.values, color='gold')
    ax.set_xlabel('Avg Rating')
    ax.set_xlim(0, 5)
    ax.set_title('Top 10 Rated Restaurants')
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=7)
    plt.tight_layout()
    show_fig(fig)

with col2:
    st.markdown("**Task 11 — Cancellation Rate by Restaurant**")
    cancel_rest = (df.groupby('Restaurant_Name')['Order_Status']
                   .apply(lambda x: x.str.lower().str.contains('cancel', na=False).mean()*100)
                   .sort_values(ascending=False).head(10))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(cancel_rest.index, cancel_rest.values, color='salmon')
    ax.set_xlabel('Cancellation Rate (%)')
    ax.set_title('Top 10 by Cancellation Rate')
    ax.invert_yaxis()
    ax.tick_params(axis='y', labelsize=7)
    plt.tight_layout()
    show_fig(fig)

with col3:
    st.markdown("**Task 12 — Cuisine-wise Performance**")
    cuis_perf = df.groupby('Cuisine_Type').agg(
        Avg_Value=('Order_Value','mean'),
        Avg_Rating=('Restaurant_Rating','mean'),
        Count=('Order_Value','count')
    ).sort_values('Count', ascending=False).head(8)
    fig, axes = plt.subplots(1, 2, figsize=(6, 4))
    cuis_perf['Avg_Value'].plot(kind='bar', ax=axes[0], color='teal', edgecolor='white')
    axes[0].set_title('Avg Order Value', fontsize=9)
    axes[0].tick_params(axis='x', rotation=45, labelsize=6)
    axes[0].set_ylabel('₹')
    cuis_perf['Avg_Rating'].plot(kind='bar', ax=axes[1], color='gold', edgecolor='white')
    axes[1].set_title('Avg Rating', fontsize=9)
    axes[1].tick_params(axis='x', rotation=45, labelsize=6)
    axes[1].set_ylim(0, 5)
    plt.tight_layout()
    show_fig(fig)

# ── SECTION 5: OPERATIONAL INSIGHTS ──────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">⚙️ Operational Insights</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Task 13 — Peak vs Non-Peak Demand**")
    # Dataset has Peak_Hour (True/False) — no raw hour field available
    peak_counts = df['Peak_Hour'].map({1: 'Peak Hour', 0: 'Non-Peak', True: 'Peak Hour', False: 'Non-Peak'}).value_counts()
    peak_revenue = df.groupby(df['Peak_Hour'].map({1: 'Peak Hour', 0: 'Non-Peak', True: 'Peak Hour', False: 'Non-Peak'}))['Order_Value'].mean()
    fig, axes = plt.subplots(1, 2, figsize=(6, 4))
    axes[0].bar(peak_counts.index, peak_counts.values,
                color=['tomato' if 'Peak' in str(x) else 'steelblue' for x in peak_counts.index],
                edgecolor='white')
    axes[0].set_title('Orders by Hour Type', fontsize=9)
    axes[0].set_ylabel('Order Count')
    axes[1].bar(peak_revenue.index, peak_revenue.values,
                color=['tomato' if 'Peak' in str(x) else 'steelblue' for x in peak_revenue.index],
                edgecolor='white')
    axes[1].set_title('Avg Value by Hour Type', fontsize=9)
    axes[1].set_ylabel('Avg Order Value (₹)')
    red_patch  = mpatches.Patch(color='tomato',    label='Peak Hour')
    blue_patch = mpatches.Patch(color='steelblue', label='Non-Peak')
    fig.legend(handles=[red_patch, blue_patch], loc='lower center', ncol=2, fontsize=7)
    plt.tight_layout()
    show_fig(fig)

with col2:
    st.markdown("**Task 14 — Payment Mode Preferences**")
    pay = df['Payment_Mode'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts, autotexts = ax.pie(
        pay.values, labels=pay.index, autopct='%1.1f%%',
        colors=sns.color_palette('Set2', len(pay)), startangle=90)
    for t in autotexts: t.set_fontsize(8)
    ax.set_title('Payment Mode Distribution')
    plt.tight_layout()
    show_fig(fig)

with col3:
    st.markdown("**Task 15 — Cancellation Reasons**")
    cancelled_df = df[df['Order_Status'].str.lower().str.contains('cancel', na=False)]
    reasons = (cancelled_df[cancelled_df['Cancellation_Reason'] != 'Not Cancelled']
               ['Cancellation_Reason'].value_counts().head(8))
    if not reasons.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(reasons.index, reasons.values, color=sns.color_palette('Reds_r', len(reasons)))
        ax.set_xlabel('Count')
        ax.set_title(f'Cancellation Reasons\n(Rate: {cancel_rate:.1f}%)')
        ax.invert_yaxis()
        ax.tick_params(axis='y', labelsize=8)
        plt.tight_layout()
        show_fig(fig)

# ── RAW DATA TABLE ────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Data (first 500 rows)"):
    display_cols = ['Order_ID','Customer_ID','City','Cuisine_Type','Order_Value',
                    'Discount_Applied','Delivery_Time_Min','Order_Status',
                    'Restaurant_Name','Restaurant_Rating','Delivery_Rating','Profit_Margin']
    show_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[show_cols].head(500), use_container_width=True)

st.markdown("---")
# st.markdown("📊 **Online Food Delivery Analysis** · Built with Streamlit & Matplotlib")
