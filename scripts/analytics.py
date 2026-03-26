"""
Analytics — 15 Business Tasks
Online Food Delivery Analysis Project
All columns mapped to actual dataset names.
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

OUTPUT_DIR = "outputs/analytics_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f"  📊 {path}")


def task1_top_spending_customers(df):
    print("\n📌 Task 1: Top Spending Customers")
    if 'Customer_ID' not in df.columns or 'Order_Value' not in df.columns: return
    result = df.groupby('Customer_ID')['Order_Value'].sum().sort_values(ascending=False).head(10)
    print(result.to_string())
    plt.figure(figsize=(10, 5))
    sns.barplot(x=result.values, y=result.index.astype(str), palette='Blues_r')
    plt.title('Top 10 Customers by Total Spend')
    plt.xlabel('Total Order Value (₹)')
    save_fig('task01_top_spending_customers')


def task2_age_group_vs_order_value(df):
    print("\n📌 Task 2: Age Group vs Order Value")
    col = 'customer_age_group' if 'customer_age_group' in df.columns else None
    if not col or 'Order_Value' not in df.columns: return
    result = df.groupby(col, observed=True)['Order_Value'].agg(['mean', 'median', 'sum', 'count'])
    result.columns = ['Avg', 'Median', 'Total', 'Count']
    print(result.to_string())
    plt.figure(figsize=(10, 5))
    result['Avg'].plot(kind='bar', color='coral', edgecolor='white')
    plt.title('Average Order Value by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Avg Order Value (₹)')
    plt.xticks(rotation=0)
    save_fig('task02_age_group_vs_order_value')


def task3_weekend_vs_weekday(df):
    print("\n📌 Task 3: Weekend vs Weekday Patterns")
    col = 'order_day_type' if 'order_day_type' in df.columns else 'Order_Day'
    if col not in df.columns or 'Order_Value' not in df.columns: return
    result = df.groupby(col)['Order_Value'].agg(['count', 'mean', 'sum'])
    result.columns = ['Orders', 'Avg Value', 'Total Revenue']
    print(result.to_string())
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    result['Orders'].plot(kind='bar', ax=axes[0], color=['steelblue', 'salmon'], edgecolor='white')
    axes[0].set_title('Order Count')
    axes[0].tick_params(axis='x', rotation=0)
    result['Avg Value'].plot(kind='bar', ax=axes[1], color=['steelblue', 'salmon'], edgecolor='white')
    axes[1].set_title('Avg Order Value (₹)')
    axes[1].tick_params(axis='x', rotation=0)
    save_fig('task03_weekend_vs_weekday')


def task4_monthly_revenue(df):
    print("\n📌 Task 4: Monthly Revenue Trends")
    if 'Order_Date' not in df.columns or 'Order_Value' not in df.columns: return
    tmp = df.copy()
    tmp['Order_Date'] = pd.to_datetime(tmp['Order_Date'], errors='coerce')
    monthly = tmp.groupby(tmp['Order_Date'].dt.to_period('M'))['Order_Value'].sum()
    print(monthly.to_string())
    plt.figure(figsize=(12, 5))
    monthly.plot(marker='o', color='royalblue', linewidth=2)
    plt.title('Monthly Revenue Trend')
    plt.ylabel('Total Revenue (₹)')
    plt.xticks(rotation=45)
    save_fig('task04_monthly_revenue')


def task5_discount_impact_on_profit(df):
    print("\n📌 Task 5: Discount Impact on Profit")
    if 'Discount_Applied' not in df.columns or 'Profit_Margin' not in df.columns: return
    buckets = pd.cut(df['Discount_Applied'], bins=5)
    result = df.groupby(buckets, observed=True)['Profit_Margin'].mean()
    print(result.to_string())
    plt.figure(figsize=(10, 5))
    result.plot(kind='bar', color='mediumpurple', edgecolor='white')
    plt.title('Avg Profit Margin by Discount Bucket')
    plt.xlabel('Discount Range')
    plt.ylabel('Avg Profit Margin (%)')
    plt.xticks(rotation=20)
    save_fig('task05_discount_impact')


def task6_high_revenue_cities_cuisines(df):
    print("\n📌 Task 6: High-Revenue Cities & Cuisines")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    if 'City' in df.columns and 'Order_Value' in df.columns:
        city = df.groupby('City')['Order_Value'].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=city.values, y=city.index, ax=axes[0], palette='Greens_r')
        axes[0].set_title('Top 10 Cities by Revenue')
        axes[0].set_xlabel('Revenue (₹)')
    if 'Cuisine_Type' in df.columns and 'Order_Value' in df.columns:
        cuisine = df.groupby('Cuisine_Type')['Order_Value'].sum().sort_values(ascending=False).head(10)
        sns.barplot(x=cuisine.values, y=cuisine.index, ax=axes[1], palette='Purples_r')
        axes[1].set_title('Top 10 Cuisines by Revenue')
        axes[1].set_xlabel('Revenue (₹)')
    save_fig('task06_high_revenue_cities_cuisines')


def task7_avg_delivery_time_by_city(df):
    print("\n📌 Task 7: Avg Delivery Time by City")
    if 'City' not in df.columns or 'Delivery_Time_Min' not in df.columns: return
    result = df.groupby('City')['Delivery_Time_Min'].mean().sort_values(ascending=False).head(15)
    print(result.to_string())
    plt.figure(figsize=(10, 6))
    sns.barplot(x=result.values, y=result.index, palette='YlOrRd')
    plt.title('Average Delivery Time by City (Top 15)')
    plt.xlabel('Avg Delivery Time (minutes)')
    save_fig('task07_delivery_time_by_city')


def task8_distance_vs_delay(df):
    print("\n📌 Task 8: Distance vs Delivery Delay")
    if 'Distance_km' not in df.columns or 'Delivery_Time_Min' not in df.columns: return
    corr = df[['Distance_km', 'Delivery_Time_Min']].corr().iloc[0, 1]
    print(f"  Pearson Correlation: {corr:.4f}")
    plt.figure(figsize=(10, 5))
    plt.hexbin(df['Distance_km'], df['Delivery_Time_Min'], gridsize=40, cmap='YlOrRd', mincnt=1)
    plt.colorbar(label='Count')
    plt.title(f'Distance vs Delivery Time (r={corr:.2f})')
    plt.xlabel('Distance (km)')
    plt.ylabel('Delivery Time (min)')
    save_fig('task08_distance_vs_delay')


def task9_rating_vs_delivery_time(df):
    print("\n📌 Task 9: Delivery Rating vs Delivery Time")
    if 'Delivery_Rating' not in df.columns or 'Delivery_Time_Min' not in df.columns: return
    result = df.groupby('Delivery_Rating')['Delivery_Time_Min'].mean().sort_index()
    print(result.to_string())
    plt.figure(figsize=(10, 5))
    sns.barplot(x=result.index, y=result.values, palette='RdYlGn')
    plt.title('Avg Delivery Time by Rating')
    plt.xlabel('Delivery Rating')
    plt.ylabel('Avg Delivery Time (min)')
    save_fig('task09_rating_vs_delivery_time')


def task10_top_rated_restaurants(df):
    print("\n📌 Task 10: Top Rated Restaurants")
    if 'Restaurant_Name' not in df.columns or 'Restaurant_Rating' not in df.columns: return
    counts = df['Restaurant_Name'].value_counts()
    eligible = counts[counts >= 50].index
    result = (df[df['Restaurant_Name'].isin(eligible)]
              .groupby('Restaurant_Name')['Restaurant_Rating']
              .mean().sort_values(ascending=False).head(10))
    print(result.to_string())
    plt.figure(figsize=(10, 5))
    sns.barplot(x=result.values, y=result.index, palette='Greens_r')
    plt.title('Top 10 Rated Restaurants (min 50 orders)')
    plt.xlabel('Average Rating')
    plt.xlim(0, 5)
    save_fig('task10_top_rated_restaurants')


def task11_cancellation_by_restaurant(df):
    print("\n📌 Task 11: Cancellation Rate by Restaurant")
    if 'Restaurant_Name' not in df.columns or 'Order_Status' not in df.columns: return
    rate = (df.groupby('Restaurant_Name')['Order_Status']
            .apply(lambda x: x.str.lower().str.contains('cancel', na=False).mean() * 100)
            .sort_values(ascending=False).head(10))
    print(rate.to_string())
    plt.figure(figsize=(10, 5))
    sns.barplot(x=rate.values, y=rate.index, palette='Reds_r')
    plt.title('Top 10 Restaurants by Cancellation Rate')
    plt.xlabel('Cancellation Rate (%)')
    save_fig('task11_cancellation_by_restaurant')


def task12_cuisinewise_performance(df):
    print("\n📌 Task 12: Cuisine-wise Performance")
    if 'Cuisine_Type' not in df.columns: return
    result = df.groupby('Cuisine_Type').agg(
        Order_Count=('Order_Value', 'count'),
        Avg_Order_Value=('Order_Value', 'mean'),
        Total_Revenue=('Order_Value', 'sum'),
        Avg_Rating=('Restaurant_Rating', 'mean')
    ).sort_values('Total_Revenue', ascending=False)
    print(result.head(10).to_string())
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    result.head(10)['Avg_Order_Value'].plot(kind='bar', ax=axes[0], color='teal', edgecolor='white')
    axes[0].set_title('Avg Order Value by Cuisine')
    axes[0].tick_params(axis='x', rotation=45)
    result.head(10)['Avg_Rating'].plot(kind='bar', ax=axes[1], color='gold', edgecolor='white')
    axes[1].set_title('Avg Rating by Cuisine')
    axes[1].tick_params(axis='x', rotation=45)
    save_fig('task12_cuisinewise_performance')


def task13_peak_hour_demand(df):
    print("\n📌 Task 13: Peak Hour Demand")
    col = 'order_hour' if 'order_hour' in df.columns else None
    if not col: return
    hourly = df.groupby(col).size().reset_index(name='count')
    print(hourly.to_string(index=False))
    plt.figure(figsize=(12, 5))
    colors = ['tomato' if (12 <= h <= 14 or 19 <= h <= 22) else 'steelblue'
              for h in hourly[col]]
    plt.bar(hourly[col], hourly['count'], color=colors, edgecolor='white')
    plt.title('Hourly Order Volume (Red = Peak Hours)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Orders')
    save_fig('task13_peak_hour_demand')


def task14_payment_modes(df):
    print("\n📌 Task 14: Payment Mode Preferences")
    if 'Payment_Mode' not in df.columns: return
    result = df['Payment_Mode'].value_counts()
    print(result.to_string())
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    result.plot(kind='pie', autopct='%1.1f%%', ax=axes[0],
                colors=sns.color_palette('Set2', len(result)))
    axes[0].set_ylabel('')
    axes[0].set_title('Payment Mode Distribution')
    sns.barplot(x=result.values, y=result.index, ax=axes[1], palette='Set2')
    axes[1].set_title('Orders by Payment Mode')
    save_fig('task14_payment_modes')


def task15_cancellation_reasons(df):
    print("\n📌 Task 15: Cancellation Reason Analysis")
    if 'Cancellation_Reason' not in df.columns or 'Order_Status' not in df.columns: return
    cancelled = df[df['Order_Status'].str.lower().str.contains('cancel', na=False)]
    rate = len(cancelled) / len(df) * 100
    print(f"  Overall Cancellation Rate: {rate:.2f}%")
    reasons = cancelled[cancelled['Cancellation_Reason'] != 'Not Cancelled']['Cancellation_Reason'].value_counts()
    print(reasons.to_string())
    if reasons.empty: return
    plt.figure(figsize=(10, 6))
    sns.barplot(x=reasons.values, y=reasons.index, palette='Reds_r')
    plt.title(f'Cancellation Reasons (Rate: {rate:.1f}%)')
    plt.xlabel('Count')
    save_fig('task15_cancellation_reasons')


def compute_kpis(df):
    print("\n📊 KEY PERFORMANCE INDICATORS")
    print("=" * 45)
    kpis = {
        'Total Orders'           : f"{len(df):,}",
        'Total Revenue (₹)'      : f"{df['Order_Value'].sum():,.2f}" if 'Order_Value' in df.columns else 'N/A',
        'Avg Order Value (₹)'    : f"{df['Order_Value'].mean():.2f}" if 'Order_Value' in df.columns else 'N/A',
        'Avg Delivery Time (min)': f"{df['Delivery_Time_Min'].mean():.2f}" if 'Delivery_Time_Min' in df.columns else 'N/A',
        'Avg Delivery Rating'    : f"{df['Delivery_Rating'].mean():.2f}" if 'Delivery_Rating' in df.columns else 'N/A',
        'Cancellation Rate (%)'  : f"{df['Order_Status'].str.lower().str.contains('cancel', na=False).mean()*100:.2f}" if 'Order_Status' in df.columns else 'N/A',
        'Avg Profit Margin (%)'  : f"{df['Profit_Margin'].mean():.2f}" if 'Profit_Margin' in df.columns else 'N/A',
    }
    for k, v in kpis.items():
        print(f"  {k:<30}: {v:>15}")
    return kpis


def run_all_analytics(df):
    print("\n🚀 RUNNING ALL 15 ANALYTICS TASKS\n" + "=" * 50)
    compute_kpis(df)
    task1_top_spending_customers(df)
    task2_age_group_vs_order_value(df)
    task3_weekend_vs_weekday(df)
    task4_monthly_revenue(df)
    task5_discount_impact_on_profit(df)
    task6_high_revenue_cities_cuisines(df)
    task7_avg_delivery_time_by_city(df)
    task8_distance_vs_delay(df)
    task9_rating_vs_delivery_time(df)
    task10_top_rated_restaurants(df)
    task11_cancellation_by_restaurant(df)
    task12_cuisinewise_performance(df)
    task13_peak_hour_demand(df)
    task14_payment_modes(df)
    task15_cancellation_reasons(df)
    print(f"\n✅ All tasks complete. Charts saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned/featured_food_delivery.csv")
    run_all_analytics(df)
