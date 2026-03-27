-- ============================================================
-- Online Food Delivery Analysis — MySQL Schema
-- Matches exact dataset columns
-- ============================================================

CREATE DATABASE IF NOT EXISTS food_delivery_db;
USE food_delivery_db;

DROP TABLE IF EXISTS food_orders;

CREATE TABLE food_orders (
    Order_ID              VARCHAR(50),
    Customer_ID           VARCHAR(50),
    Customer_Age          FLOAT,
    Customer_Gender       VARCHAR(20),
    City                  VARCHAR(100),
    Area                  VARCHAR(100),
    Restaurant_ID         VARCHAR(50),
    Restaurant_Name       VARCHAR(200),
    Cuisine_Type          VARCHAR(100),
    Order_Date            DATE,
    Order_Time            VARCHAR(20),
    Delivery_Time_Min     FLOAT,
    Distance_km           FLOAT,
    Order_Value           FLOAT,
    Discount_Applied      FLOAT,
    Final_Amount          FLOAT,
    Payment_Mode          VARCHAR(50),
    Order_Status          VARCHAR(30),
    Cancellation_Reason   VARCHAR(200),
    Delivery_Partner_ID   VARCHAR(50),
    Delivery_Rating       FLOAT,
    Restaurant_Rating     FLOAT,
    Order_Day             VARCHAR(20),
    Peak_Hour             TINYINT,
    Profit_Margin         FLOAT,
    order_hour            INT,
    order_day_type        VARCHAR(20),
    is_peak_hour          INT,
    profit_margin_pct     FLOAT,
    delivery_performance  VARCHAR(20),
    customer_age_group    VARCHAR(20),
    order_value_segment   VARCHAR(20),
    discount_applied_flag INT,
    order_month           INT,
    order_year            INT,
    PRIMARY KEY (Order_ID),
    INDEX idx_customer    (Customer_ID),
    INDEX idx_restaurant  (Restaurant_Name),
    INDEX idx_city        (City),
    INDEX idx_date        (Order_Date),
    INDEX idx_status      (Order_Status),
    INDEX idx_cuisine     (Cuisine_Type)
);
