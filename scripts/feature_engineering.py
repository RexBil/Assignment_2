"""
Step 5: Feature Engineering
Online Food Delivery Analysis Project
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


def engineer_features(df, config=None):
    print("\n⚙️  FEATURE ENGINEERING\n" + "=" * 40)

    # ── Order Hour from Order_Time ──────────────────────────────
    if 'Order_Time' in df.columns:
        df['order_hour'] = pd.to_datetime(df['Order_Time'], errors='coerce').dt.hour
        df['order_hour'] = df['order_hour'].fillna(
            pd.to_datetime(df['Order_Time'], format='%H:%M', errors='coerce').dt.hour
        ).fillna(12).astype(int)
        print("✅ Added: order_hour")

    # ── Order Day Type (use existing Order_Day or derive from Order_Date) ──
    if 'Order_Day' in df.columns:
        df['order_day_type'] = df['Order_Day'].str.strip().str.title()
        print("✅ Added: order_day_type (from Order_Day)")
    elif 'Order_Date' in df.columns:
        df['order_day_type'] = pd.to_datetime(df['Order_Date'], errors='coerce').dt.day_name().apply(
            lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday'
        )
        print("✅ Added: order_day_type (derived from Order_Date)")

    # ── Peak Hour (use existing Peak_Hour column) ──
    if 'Peak_Hour' in df.columns:
        df['is_peak_hour'] = df['Peak_Hour'].astype(int)
        print("✅ Added: is_peak_hour (from Peak_Hour)")
    elif 'order_hour' in df.columns:
        df['is_peak_hour'] = df['order_hour'].apply(
            lambda h: 1 if (12 <= h <= 14) or (19 <= h <= 22) else 0
        )
        print("✅ Added: is_peak_hour (derived from order_hour)")

    # ── Profit Margin Pct (use existing Profit_Margin) ──
    if 'Profit_Margin' in df.columns:
        df['profit_margin_pct'] = df['Profit_Margin']
        print("✅ Added: profit_margin_pct (from Profit_Margin)")

    # ── Delivery Performance ──
    if 'Delivery_Time_Min' in df.columns:
        def classify(t):
            if t <= 25:   return 'Fast'
            elif t <= 45: return 'On-Time'
            else:         return 'Delayed'
        df['delivery_performance'] = df['Delivery_Time_Min'].apply(classify)
        print("✅ Added: delivery_performance")

    # ── Customer Age Group ──
    if 'Customer_Age' in df.columns:
        bins   = [0, 18, 25, 35, 45, 60, 120]
        labels = ['<18', '18-25', '26-35', '36-45', '46-60', '60+']
        df['customer_age_group'] = pd.cut(df['Customer_Age'], bins=bins,
                                           labels=labels, right=True)
        print("✅ Added: customer_age_group")

    # ── Order Value Segment ──
    if 'Order_Value' in df.columns:
        q1 = df['Order_Value'].quantile(0.33)
        q2 = df['Order_Value'].quantile(0.66)
        df['order_value_segment'] = df['Order_Value'].apply(
            lambda v: 'Low' if v <= q1 else ('Medium' if v <= q2 else 'High')
        )
        print("✅ Added: order_value_segment")

    # ── Discount Flag ──
    if 'Discount_Applied' in df.columns:
        df['discount_applied_flag'] = (df['Discount_Applied'] > 0).astype(int)
        print("✅ Added: discount_applied_flag")

    # ── Month & Year from Order_Date ──
    if 'Order_Date' in df.columns:
        dt = pd.to_datetime(df['Order_Date'], errors='coerce')
        df['order_month'] = dt.dt.month
        df['order_year']  = dt.dt.year
        print("✅ Added: order_month, order_year")

    print(f"\nTotal columns after engineering: {df.shape[1]}")
    return df


if __name__ == "__main__":
    INPUT  = "data/cleaned/cleaned_food_delivery.csv"
    OUTPUT = "data/cleaned/featured_food_delivery.csv"
    df = pd.read_csv(INPUT)
    df = engineer_features(df)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    print(f"💾 Saved: {OUTPUT}")
