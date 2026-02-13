import pandas as pd

def add_features(df):

    # Convert date
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    df['Month'] = df['Order_Date'].dt.month
    df['Day_Name'] = df['Order_Date'].dt.day_name()

    # Weekend / Weekday
    df['Order_Day_Type'] = df['Day_Name'].apply(
        lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday'
    )

    # Profit Margin % already exists, just rename for clarity
    df['Profit_Margin_%'] = df['Profit_Margin']

    return df
