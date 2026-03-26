"""
Step 3: Data Cleaning & Preprocessing
Online Food Delivery Analysis Project

Actual Dataset Columns:
Order_ID, Customer_ID, Customer_Age, Customer_Gender, City, Area,
Restaurant_ID, Restaurant_Name, Cuisine_Type, Order_Date, Order_Time,
Delivery_Time_Min, Distance_km, Order_Value, Discount_Applied, Final_Amount,
Payment_Mode, Order_Status, Cancellation_Reason, Delivery_Partner_ID,
Delivery_Rating, Restaurant_Rating, Order_Day, Peak_Hour, Profit_Margin
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')


def load_data(filepath):
    ext = os.path.splitext(filepath)[-1].lower()
    df = pd.read_csv(filepath) if ext == '.csv' else pd.read_excel(filepath)
    print(f"✅ Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df


def initial_inspection(df):
    print("\n📋 DATASET OVERVIEW")
    print("=" * 50)
    print(f"Shape: {df.shape}")
    missing = df.isnull().sum()
    print(f"\nMissing Values:\n{missing[missing > 0]}")
    print(f"\nDuplicate Rows: {df.duplicated().sum()}")


def remove_duplicates(df):
    before = len(df)
    df = df.drop_duplicates()
    print(f"\n🔁 Duplicates removed: {before - len(df)}")
    return df


def parse_datetime_columns(df):
    print("\n📅 Parsing Date Columns...")
    if 'Order_Date' in df.columns:
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
        print("  Order_Date: converted to datetime")
    return df


def handle_missing_values(df):
    print("\n🧹 Handling Missing Values...")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        missing = df[col].isnull().sum()
        if missing > 0:
            val = df[col].median()
            df[col] = df[col].fillna(val)
            print(f"  {col}: filled {missing:,} nulls with median ({val:.2f})")

    cat_cols = df.select_dtypes(include=['object']).columns
    skip = ['Cancellation_Reason']
    for col in cat_cols:
        if col in skip:
            continue
        missing = df[col].isnull().sum()
        if missing > 0:
            val = df[col].mode()[0]
            df[col] = df[col].fillna(val)
            print(f"  {col}: filled {missing:,} nulls with mode ('{val}')")

    if 'Cancellation_Reason' in df.columns:
        mask = df['Cancellation_Reason'].isnull()
        df.loc[mask, 'Cancellation_Reason'] = 'Not Cancelled'
        print(f"  Cancellation_Reason: filled {mask.sum():,} nulls with 'Not Cancelled'")

    if 'Peak_Hour' in df.columns:
        df['Peak_Hour'] = df['Peak_Hour'].map(
            {'TRUE': 1, 'FALSE': 0, 'True': 1, 'False': 0, True: 1, False: 0, 1: 1, 0: 0}
        ).fillna(0).astype(int)
        print("  Peak_Hour: standardized to 0/1")

    print(f"  Remaining nulls: {df.isnull().sum().sum()}")
    return df


def correct_invalid_values(df):
    print("\n🔧 Correcting Invalid Values...")

    for col in ['Delivery_Rating', 'Restaurant_Rating']:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            invalid = (df[col] > 5) | (df[col] < 0)
            if invalid.sum() > 0:
                df.loc[invalid, col] = df[col].median()
                print(f"  {col}: fixed {invalid.sum():,} invalid ratings")

    if 'Delivery_Time_Min' in df.columns:
        invalid = (df['Delivery_Time_Min'] <= 0) | (df['Delivery_Time_Min'] > 180)
        if invalid.sum() > 0:
            df.loc[invalid, 'Delivery_Time_Min'] = df['Delivery_Time_Min'].median()
            print(f"  Delivery_Time_Min: fixed {invalid.sum():,} invalid values")

    for col in ['Order_Value', 'Final_Amount', 'Discount_Applied']:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            invalid = df[col] < 0
            if invalid.sum() > 0:
                df.loc[invalid, col] = df[col].median()
                print(f"  {col}: fixed {invalid.sum():,} negative values")

    if 'Profit_Margin' in df.columns:
        df['Profit_Margin'] = np.clip(df['Profit_Margin'], -100, 100)

    if 'Customer_Age' in df.columns:
        invalid = (df['Customer_Age'] < 10) | (df['Customer_Age'] > 100)
        if invalid.sum() > 0:
            df.loc[invalid, 'Customer_Age'] = df['Customer_Age'].median()
            print(f"  Customer_Age: fixed {invalid.sum():,} invalid ages")

    if 'Distance_km' in df.columns:
        invalid = df['Distance_km'] <= 0
        if invalid.sum() > 0:
            df.loc[invalid, 'Distance_km'] = df['Distance_km'].median()
            print(f"  Distance_km: fixed {invalid.sum():,} non-positive values")

    return df


def treat_outliers(df):
    print("\n📊 Treating Outliers (IQR Capping)...")
    cols = ['Delivery_Time_Min', 'Distance_km', 'Order_Value',
            'Final_Amount', 'Discount_Applied', 'Customer_Age']
    for col in cols:
        if col not in df.columns:
            continue
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        before = ((df[col] < lower) | (df[col] > upper)).sum()
        df[col] = np.clip(df[col], lower, upper)
        if before > 0:
            print(f"  {col}: capped {before:,} outliers → [{lower:.2f}, {upper:.2f}]")
    return df


def standardize_categoricals(df):
    print("\n🔠 Standardizing Categorical Columns...")
    cols = ['City', 'Area', 'Cuisine_Type', 'Payment_Mode',
            'Order_Status', 'Customer_Gender', 'Order_Day']
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            print(f"  {col}: standardized")
    return df


def validate_business_logic(df):
    print("\n✅ Validating Business Logic...")
    if 'Order_Status' in df.columns and 'Delivery_Rating' in df.columns:
        cancelled = df['Order_Status'].str.lower().str.contains('cancel', na=False)
        count = (cancelled & df['Delivery_Rating'].notna()).sum()
        df.loc[cancelled, 'Delivery_Rating'] = np.nan
        df['Delivery_Rating'] = df['Delivery_Rating'].fillna(df['Delivery_Rating'].median())
        print(f"  Cleared {count:,} delivery ratings for cancelled orders")
    return df


def clean_data(input_path, output_path):
    df = load_data(input_path)
    initial_inspection(df)
    df = remove_duplicates(df)
    df = parse_datetime_columns(df)
    df = handle_missing_values(df)
    df = correct_invalid_values(df)
    df = treat_outliers(df)
    df = standardize_categoricals(df)
    df = validate_business_logic(df)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n💾 Cleaned data saved: {output_path}  |  Shape: {df.shape}")
    return df


if __name__ == "__main__":
    clean_data("data/raw/online_food_delivery.csv",
               "data/cleaned/cleaned_food_delivery.csv")
