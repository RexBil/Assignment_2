-- =====================================
-- STEP 1: CREATE DATABASE
-- =====================================

DROP DATABASE IF EXISTS food_delivery_db;
CREATE DATABASE food_delivery_db;
USE food_delivery_db;

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS delivery_partners;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS customers;

-- =====================================
-- CUSTOMERS TABLE
-- =====================================

CREATE TABLE customers (
    Customer_ID INT PRIMARY KEY,
    Customer_Age INT NOT NULL,
    Customer_Gender VARCHAR(10) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Area VARCHAR(150),

    CHECK (Customer_Age BETWEEN 15 AND 80),
    CHECK (Customer_Gender IN ('Male','Female','Other'))
);

-- =====================================
-- RESTAURANTS TABLE
-- =====================================

CREATE TABLE restaurants (
    Restaurant_ID INT PRIMARY KEY,
    Restaurant_Name VARCHAR(200) NOT NULL,
    Cuisine_Type VARCHAR(100) NOT NULL,
    Restaurant_Rating DECIMAL(3,2),

    CHECK (Restaurant_Rating BETWEEN 0 AND 5)
);

-- =====================================
-- DELIVERY PARTNERS TABLE
-- =====================================

CREATE TABLE delivery_partners (
    Delivery_Partner_ID INT PRIMARY KEY
);

-- =====================================
-- ORDERS TABLE
-- =====================================

CREATE TABLE orders (
    Order_ID INT PRIMARY KEY,

    Customer_ID INT NOT NULL,
    Restaurant_ID INT NOT NULL,
    Delivery_Partner_ID INT NOT NULL,

    Order_Date DATE NOT NULL,
    Order_Time TIME NOT NULL,

    Delivery_Time_Min INT,
    Distance_km DECIMAL(6,2),

    Order_Value DECIMAL(10,2) NOT NULL,
    Discount_Applied DECIMAL(10,2) DEFAULT 0,
    Final_Amount DECIMAL(10,2) NOT NULL,

    Payment_Mode VARCHAR(50),
    Order_Status VARCHAR(50),
    Cancellation_Reason VARCHAR(200),

    Delivery_Rating DECIMAL(3,2),
    Profit_Margin DECIMAL(6,2),

    Order_Day VARCHAR(20),
    Peak_Hour VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- ======================
    -- FOREIGN KEYS
    -- ======================
    FOREIGN KEY (Customer_ID)
        REFERENCES customers(Customer_ID)
        ON DELETE CASCADE,

    FOREIGN KEY (Restaurant_ID)
        REFERENCES restaurants(Restaurant_ID)
        ON DELETE CASCADE,

    FOREIGN KEY (Delivery_Partner_ID)
        REFERENCES delivery_partners(Delivery_Partner_ID)
        ON DELETE CASCADE,

    -- ======================
    -- ADVANCED CONSTRAINTS
    -- ======================
    CHECK (Delivery_Time_Min >= 0),
    CHECK (Distance_km >= 0),
    CHECK (Order_Value >= 0),
    CHECK (Final_Amount >= 0),
    CHECK (Delivery_Rating BETWEEN 0 AND 5)
);

-- =====================================
-- INDEXES
-- =====================================

CREATE INDEX idx_customer_city ON customers(City);
CREATE INDEX idx_restaurant_cuisine ON restaurants(Cuisine_Type);
CREATE INDEX idx_order_date ON orders(Order_Date);
CREATE INDEX idx_order_status ON orders(Order_Status);
CREATE INDEX idx_payment_mode ON orders(Payment_Mode);

DELIMITER //

CREATE PROCEDURE Get_Overall_KPIs()
BEGIN
    SELECT 
        COUNT(*) AS Total_Orders,
        SUM(Order_Value) AS Total_Revenue,
        AVG(Delivery_Time_Min) AS Avg_Delivery_Time,
        AVG(Delivery_Rating) AS Avg_Delivery_Rating,
        SUM(CASE WHEN Order_Status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) 
        AS Cancellation_Rate
    FROM orders;
END //

DELIMITER ;

CREATE PROCEDURE Get_City_Revenue(IN city_name VARCHAR(100))
BEGIN
    SELECT 
        c.City,
        SUM(o.Order_Value) AS Total_Revenue
    FROM orders o
    JOIN customers c ON o.Customer_ID = c.Customer_ID
    WHERE c.City = city_name
    GROUP BY c.City;
END //

DELIMITER ;