"""
Step 4: EDA — Online Food Delivery Analysis
All column references use actual dataset column names.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = "outputs/eda_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.rcParams.update({'figure.dpi': 120})


def save_fig(name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"  📊 {path}")


def plot_order_value_distribution(df):
    if 'Order_Value' not in df.columns: return
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(df['Order_Value'].dropna(), bins=40, color='steelblue', edgecolor='white')
    axes[0].set_title('Order Value Distribution')
    axes[0].set_xlabel('Order Value (₹)')
    axes[0].set_ylabel('Frequency')
    axes[1].boxplot(df['Order_Value'].dropna(), vert=False, patch_artist=True,
                    boxprops=dict(facecolor='lightblue'))
    axes[1].set_title('Order Value Boxplot')
    save_fig('01_order_value_distribution')


def plot_delivery_time_distribution(df):
    if 'Delivery_Time_Min' not in df.columns: return
    plt.figure(figsize=(10, 5))
    sns.histplot(df['Delivery_Time_Min'].dropna(), kde=True, bins=40, color='coral')
    plt.axvline(df['Delivery_Time_Min'].mean(),   color='red',   linestyle='--',
                label=f"Mean: {df['Delivery_Time_Min'].mean():.1f} min")
    plt.axvline(df['Delivery_Time_Min'].median(), color='green', linestyle='--',
                label=f"Median: {df['Delivery_Time_Min'].median():.1f} min")
    plt.title('Delivery Time Distribution')
    plt.xlabel('Delivery Time (minutes)')
    plt.legend()
    save_fig('02_delivery_time_distribution')


def plot_citywise_orders(df):
    if 'City' not in df.columns: return
    top = df['City'].value_counts().head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top.values, y=top.index, palette='Set2')
    plt.title('Top 10 Cities by Order Volume')
    plt.xlabel('Number of Orders')
    save_fig('03_citywise_orders')


def plot_cuisinewise_orders(df):
    if 'Cuisine_Type' not in df.columns: return
    top = df['Cuisine_Type'].value_counts().head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top.values, y=top.index, palette='rocket')
    plt.title('Top 10 Cuisines by Order Volume')
    plt.xlabel('Number of Orders')
    save_fig('04_cuisinewise_orders')


def plot_weekday_vs_weekend(df):
    col = 'order_day_type' if 'order_day_type' in df.columns else 'Order_Day'
    if col not in df.columns: return
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    df[col].value_counts().plot.pie(ax=axes[0], autopct='%1.1f%%',
                                     colors=['#66b3ff', '#ff9999'])
    axes[0].set_title('Order Count: Weekday vs Weekend')
    axes[0].set_ylabel('')
    if 'Order_Value' in df.columns:
        sns.boxplot(data=df, x=col, y='Order_Value', palette='pastel', ax=axes[1])
        axes[1].set_title('Order Value: Weekday vs Weekend')
    save_fig('05_weekday_vs_weekend')


def plot_distance_vs_delay(df):
    if 'Distance_km' not in df.columns or 'Delivery_Time_Min' not in df.columns: return
    tmp = df[['Distance_km', 'Delivery_Time_Min']].dropna()
    plt.figure(figsize=(10, 5))
    plt.scatter(tmp['Distance_km'], tmp['Delivery_Time_Min'], alpha=0.2, c='teal', s=8)
    m, b = np.polyfit(tmp['Distance_km'], tmp['Delivery_Time_Min'], 1)
    x = np.linspace(tmp['Distance_km'].min(), tmp['Distance_km'].max(), 100)
    plt.plot(x, m * x + b, color='red', linewidth=2, label=f'y={m:.2f}x+{b:.2f}')
    plt.title('Delivery Distance vs Delivery Time')
    plt.xlabel('Distance (km)')
    plt.ylabel('Delivery Time (minutes)')
    plt.legend()
    save_fig('06_distance_vs_delivery_time')


def plot_cancellation_reasons(df):
    if 'Cancellation_Reason' not in df.columns: return
    tmp = df[df['Cancellation_Reason'] != 'Not Cancelled']
    counts = tmp['Cancellation_Reason'].value_counts().head(8)
    if counts.empty: return
    plt.figure(figsize=(10, 5))
    sns.barplot(y=counts.index, x=counts.values, palette='Reds_r')
    plt.title('Top Cancellation Reasons')
    plt.xlabel('Count')
    save_fig('07_cancellation_reasons')


def plot_cancellation_by_restaurant(df):
    if 'Restaurant_Name' not in df.columns or 'Order_Status' not in df.columns: return
    rate = (df.groupby('Restaurant_Name')['Order_Status']
            .apply(lambda x: x.str.lower().str.contains('cancel', na=False).mean() * 100)
            .sort_values(ascending=False).head(10))
    plt.figure(figsize=(10, 5))
    sns.barplot(x=rate.values, y=rate.index, palette='OrRd')
    plt.title('Top 10 Restaurants by Cancellation Rate')
    plt.xlabel('Cancellation Rate (%)')
    save_fig('08_cancellation_by_restaurant')


def plot_correlation_heatmap(df):
    num = df.select_dtypes(include=[np.number])
    if num.shape[1] < 2: return
    plt.figure(figsize=(12, 8))
    corr = num.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=0.5)
    plt.title('Correlation Heatmap')
    save_fig('09_correlation_heatmap')


def plot_monthly_revenue(df):
    if 'Order_Date' not in df.columns or 'Order_Value' not in df.columns: return
    tmp = df.copy()
    tmp['Order_Date'] = pd.to_datetime(tmp['Order_Date'], errors='coerce')
    monthly = tmp.groupby(tmp['Order_Date'].dt.to_period('M'))['Order_Value'].sum().reset_index()
    monthly['Order_Date'] = monthly['Order_Date'].astype(str)
    plt.figure(figsize=(12, 5))
    plt.plot(monthly['Order_Date'], monthly['Order_Value'], marker='o',
             color='royalblue', linewidth=2)
    plt.fill_between(monthly['Order_Date'], monthly['Order_Value'], alpha=0.2, color='royalblue')
    plt.xticks(rotation=45)
    plt.title('Monthly Revenue Trend')
    plt.ylabel('Total Revenue (₹)')
    save_fig('10_monthly_revenue_trend')


def plot_payment_modes(df):
    if 'Payment_Mode' not in df.columns: return
    counts = df['Payment_Mode'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%',
            colors=sns.color_palette('Set2', len(counts)))
    plt.title('Payment Mode Preferences')
    save_fig('11_payment_mode_preferences')


def plot_peak_hour_demand(df):
    col = 'order_hour' if 'order_hour' in df.columns else None
    if not col: return
    hourly = df.groupby(col).size().reset_index(name='order_count')
    plt.figure(figsize=(12, 5))
    colors = ['tomato' if (12 <= h <= 14 or 19 <= h <= 22) else 'steelblue'
              for h in hourly[col]]
    plt.bar(hourly[col], hourly['order_count'], color=colors, edgecolor='white')
    plt.title('Hourly Order Demand (Red = Peak Hours)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Orders')
    save_fig('12_peak_hour_demand')


def run_eda(df):
    print("\n🔍 RUNNING EXPLORATORY DATA ANALYSIS\n" + "=" * 50)
    plot_order_value_distribution(df)
    plot_delivery_time_distribution(df)
    plot_citywise_orders(df)
    plot_cuisinewise_orders(df)
    plot_weekday_vs_weekend(df)
    plot_distance_vs_delay(df)
    plot_cancellation_reasons(df)
    plot_cancellation_by_restaurant(df)
    plot_correlation_heatmap(df)
    plot_monthly_revenue(df)
    plot_payment_modes(df)
    plot_peak_hour_demand(df)
    print(f"\n✅ EDA complete. Charts saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned/featured_food_delivery.csv")
    run_eda(df)
