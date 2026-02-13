from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.feature_engineering import add_features
from src.database import upload_to_mysql
from src.eda import revenue_by_city
from src.analytics import *
from src.data_insertion import  insert_data

def run_pipeline():

    df = load_data("data/ONINE_FOOD_DELIVERY_ANALYSIS.csv")
    df = clean_data(df)
    df = add_features(df)

    insert_data(df)

    # Customer Analysis
    top_spending_customers(df)
    age_group_vs_order_value(df)
    weekend_vs_weekday(df)

    # Revenue & Profilt
    monthly_revenue_trend(df)
    discount_impact_on_profit(df)
    high_revenue_city_cuisine(df)

    # Delivery
    avg_delivery_time_by_city(df)
    distance_vs_delivery_time(df)
    rating_vs_delivery_time(df)

    # Restaurant
    top_rated_restaurants(df)
    cancellation_rate_by_restaurant(df)
    cuisine_performance(df)

    # Operational
    peak_hour_analysis(df)
    payment_mode_preferences(df)
    cancellation_reason_analysis(df)

    # revenue_by_city(df)

    upload_to_mysql(df)

if __name__ == "__main__":
    run_pipeline()
