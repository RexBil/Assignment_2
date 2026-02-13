import pandas as pd
import numpy as np

def clean_data(df):

    # Standardize column names
    df.columns = df.columns.str.strip()

    # Remove duplicates
    df = df.drop_duplicates().copy()

    # Handle numeric missing values
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Handle categorical missing values
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Fix invalid ratings
    df.loc[df['Delivery_Rating'] > 5, 'Delivery_Rating'] = 5
    df.loc[df['Restaurant_Rating'] > 5, 'Restaurant_Rating'] = 5

    # Remove negative values
    df = df[df['Order_Value'] >= 0]
    df = df[df['Final_Amount'] >= 0]

    # Handle categorical missing values safely
    categorical_cols = df.select_dtypes(include='object').columns

    for col in categorical_cols:
        mode_value = df[col].mode()[0]
        df[col] = df[col].fillna(mode_value)

    # Explicitly fix dtype inference (future safe)
    df = df.infer_objects(copy=False)

    return df
