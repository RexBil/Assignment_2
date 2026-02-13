from src.database import connect_db

def insert_data(df):

    engine = connect_db()

    # =============================
    # Insert Customers
    # =============================
    customers = df[[
        "Customer_ID",
        "Customer_Age",
        "Customer_Gender",
        "City",
        "Area"
    ]].drop_duplicates()

    customers.to_sql("customers", engine, if_exists="append", index=False)


    # =============================
    # Insert Restaurants
    # =============================
    restaurants = df[[
        "Restaurant_ID",
        "Restaurant_Name",
        "Cuisine_Type",
        "Restaurant_Rating"
    ]].drop_duplicates()

    restaurants.to_sql("restaurants", engine, if_exists="append", index=False)


    # =============================
    # Insert Delivery Partners
    # =============================
    partners = df[["Delivery_Partner_ID"]].drop_duplicates()

    partners.to_sql("delivery_partners", engine, if_exists="append", index=False)


    # =============================
    # Insert Orders (Fact Table)
    # =============================
    orders = df[[
        "Order_ID",
        "Customer_ID",
        "Restaurant_ID",
        "Delivery_Partner_ID",
        "Order_Date",
        "Order_Time",
        "Delivery_Time_Min",
        "Distance_km",
        "Order_Value",
        "Discount_Applied",
        "Final_Amount",
        "Payment_Mode",
        "Order_Status",
        "Cancellation_Reason",
        "Delivery_Rating",
        "Profit_Margin",
        "Order_Day",
        "Peak_Hour"
    ]]

    orders.to_sql("orders", engine, if_exists="append", index=False)

    print("Data inserted into normalized tables successfully.")
