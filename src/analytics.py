import pandas as pd


# ===============================
# 1️⃣ CUSTOMER & ORDER ANALYSIS
# ===============================

def top_spending_customers(df):
    print("\nTop 10 Spending Customers:")
    result = (
        df.groupby("Customer_ID")["Order_Value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print(result)


def age_group_vs_order_value(df):
    print("\nAge Group vs Average Order Value:")

    bins = [15, 25, 35, 45, 60]
    labels = ["18-25", "26-35", "36-45", "46+"]

    df["Age_Group"] = pd.cut(df["Customer_Age"], bins=bins, labels=labels)

    result = df.groupby("Age_Group")["Order_Value"].mean()
    print(result)


def weekend_vs_weekday(df):
    print("\nWeekend vs Weekday Orders:")
    result = df["Order_Day_Type"].value_counts()
    print(result)


# ===============================
# 2️⃣ REVENUE & PROFIT ANALYSIS
# ===============================

def monthly_revenue_trend(df):
    print("\nMonthly Revenue Trend:")
    df["Month"] = df["Order_Date"].dt.month
    result = df.groupby("Month")["Order_Value"].sum()
    print(result)


def discount_impact_on_profit(df):
    print("\nDiscount Impact on Profit Margin:")
    result = df.groupby("Discount_Applied")["Profit_Margin"].mean()
    print(result)


def high_revenue_city_cuisine(df):
    print("\nHigh Revenue Cities:")
    city = df.groupby("City")["Order_Value"].sum().sort_values(ascending=False)
    print(city.head())

    print("\nHigh Revenue Cuisines:")
    cuisine = df.groupby("Cuisine_Type")["Order_Value"].sum().sort_values(ascending=False)
    print(cuisine.head())


# ===============================
# 3️⃣ DELIVERY PERFORMANCE
# ===============================

def avg_delivery_time_by_city(df):
    print("\nAverage Delivery Time by City:")
    result = df.groupby("City")["Delivery_Time_Min"].mean()
    print(result.sort_values(ascending=False))


def distance_vs_delivery_time(df):
    print("\nDistance vs Delivery Time Correlation:")
    correlation = df["Distance_km"].corr(df["Delivery_Time_Min"])
    print("Correlation:", correlation)


def rating_vs_delivery_time(df):
    print("\nDelivery Rating vs Delivery Time:")
    result = df.groupby("Delivery_Rating")["Delivery_Time_Min"].mean()
    print(result)


# ===============================
# 4️⃣ RESTAURANT PERFORMANCE
# ===============================

def top_rated_restaurants(df):
    print("\nTop Rated Restaurants:")
    result = (
        df.groupby("Restaurant_Name")["Restaurant_Rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    print(result)


def cancellation_rate_by_restaurant(df):
    print("\nCancellation Rate by Restaurant:")

    cancel_df = df[df["Order_Status"] == "Cancelled"]
    rate = cancel_df.groupby("Restaurant_Name").size() / df.groupby("Restaurant_Name").size()
    print(rate.sort_values(ascending=False).head(10))


def cuisine_performance(df):
    print("\nCuisine-wise Average Revenue:")
    result = df.groupby("Cuisine_Type")["Order_Value"].mean()
    print(result.sort_values(ascending=False))


# ===============================
# 5️⃣ OPERATIONAL INSIGHTS
# ===============================

def peak_hour_analysis(df):
    print("\nPeak Hour Demand:")
    result = df["Peak_Hour"].value_counts()
    print(result)


def payment_mode_preferences(df):
    print("\nPayment Mode Preferences:")
    result = df["Payment_Mode"].value_counts()
    print(result)


def cancellation_reason_analysis(df):
    print("\nCancellation Reason Analysis:")
    result = df["Cancellation_Reason"].value_counts()
    print(result)
