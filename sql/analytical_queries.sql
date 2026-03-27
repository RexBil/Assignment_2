-- ============================================================
-- Online Food Delivery Analysis — MySQL Schema & Queries
-- ============================================================

-- ─────────────────────────────────────────────
-- CREATE DATABASE
-- ─────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS food_delivery_db;
USE food_delivery_db;

-- ─────────────────────────────────────────────
-- TABLE: orders
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    order_id            VARCHAR(50)     PRIMARY KEY,
    order_date          DATETIME        NOT NULL,
    customer_id         VARCHAR(50)     NOT NULL,
    restaurant_id       VARCHAR(50)     NOT NULL,
    cuisine_type        VARCHAR(100),
    city                VARCHAR(100),
    order_value         DECIMAL(10, 2)  NOT NULL,
    discount_amount     DECIMAL(10, 2)  DEFAULT 0.00,
    payment_mode        VARCHAR(50),
    order_status        VARCHAR(30),
    cancellation_reason VARCHAR(200),
    INDEX idx_customer  (customer_id),
    INDEX idx_restaurant(restaurant_id),
    INDEX idx_date      (order_date),
    INDEX idx_status    (order_status)
);

-- ─────────────────────────────────────────────
-- TABLE: customers
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS customers (
    customer_id         VARCHAR(50)     PRIMARY KEY,
    customer_name       VARCHAR(200),
    customer_age        INT,
    customer_gender     VARCHAR(20),
    customer_city       VARCHAR(100),
    customer_since      DATE
);

-- ─────────────────────────────────────────────
-- TABLE: restaurants
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id       VARCHAR(50)     PRIMARY KEY,
    restaurant_name     VARCHAR(200),
    cuisine_type        VARCHAR(100),
    city                VARCHAR(100),
    restaurant_rating   DECIMAL(3, 2),
    INDEX idx_rating    (restaurant_rating)
);

-- ─────────────────────────────────────────────
-- TABLE: deliveries
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id         VARCHAR(50)     PRIMARY KEY,
    order_id            VARCHAR(50)     NOT NULL,
    delivery_time_minutes INT,
    distance_km         DECIMAL(6, 2),
    delivery_rating     DECIMAL(3, 2),
    delivery_partner_id VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- ─────────────────────────────────────────────
-- TABLE: financials
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS financials (
    record_id           INT             AUTO_INCREMENT PRIMARY KEY,
    order_id            VARCHAR(50)     NOT NULL,
    revenue             DECIMAL(10, 2),
    cost                DECIMAL(10, 2),
    profit_margin       DECIMAL(6, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- ============================================================
-- ANALYTICAL QUERIES
-- ============================================================

-- ── Task : All Cities
SELECT DISTINCT City FROM food_orders 
    WHERE 1=1 
    {{WHERE}} 
    ORDER BY City

-- ── Task : Country Type
SELECT DISTINCT Cuisine_Type FROM food_orders 
    WHERE 1=1 
    {{WHERE}} 
    ORDER BY Cuisine_Type

-- ── Task : Cancel Status
SELECT DISTINCT Order_Status FROM food_orders  
    WHERE 1=1 
    {{WHERE}} 
    ORDER BY Order_Status

-- ── Task : KPI Summary

SELECT
        COUNT(*) AS total_orders,
        SUM(Order_Value) AS total_revenue,
        AVG(Order_Value) AS avg_order_value,
        AVG(Delivery_Time_Min) AS avg_delivery_time,
        AVG(Delivery_Rating) AS avg_rating,
        SUM(CASE WHEN LOWER(Order_Status) LIKE '%%cancel%%' THEN 1 ELSE 0 END)
            * 100.0 / COUNT(*) AS cancel_rate,
        AVG(profit_margin_pct)  AS avg_profit_margin
    FROM food_orders
    WHERE 1=1
    {{WHERE}}

-- ── Task : Top 10 Spending Customers
SELECT Customer_ID, SUM(Order_Value) AS total_spend
         FROM food_orders
         WHERE 1=1 
         {{WHERE}}
         GROUP BY Customer_ID
         ORDER BY total_spend DESC LIMIT 10

-- ── Task : Age Group vs Order Value
SELECT 
        customer_age_group, 
        AVG(Order_Value) AS avg_value, 
        COUNT(*) AS cnt
    FROM food_orders 
    WHERE 1=1
    {{WHERE}}
    AND customer_age_group IS NOT NULL
    GROUP BY customer_age_group
    ORDER BY FIELD(customer_age_group,'<18','18-25','26-35','36-45','46-60','60+');


-- ── Task : Weekend vs Weekday Order Patterns
SELECT order_day_type AS order_day_type,
               COUNT(*) AS order_count,
               AVG(Order_Value) AS avg_value
    FROM food_orders 
    WHERE 1=1
    {{WHERE}}
    AND order_day_type IS NOT NULL
    GROUP BY order_day_type


-- ── Task : Monthly Revenue Trends
SELECT DATE_FORMAT(Order_Date, '%%Y-%%m') AS month,
               SUM(Order_Value) AS revenue
    FROM food_orders  
    WHERE 1=1
    {{WHERE}}
    AND Order_Date IS NOT NULL
    GROUP BY month ORDER BY month


-- ── Task : Discount Impact on Profit
SELECT
            CASE
                WHEN Discount_Applied = 0        THEN 'No Discount'
                WHEN Discount_Applied <= 50      THEN 'Low (1-50)'
                WHEN Discount_Applied <= 100     THEN 'Medium (51-100)'
                WHEN Discount_Applied <= 150     THEN 'High (101-150)'
                ELSE 'Very High (150+)'
            END AS discount_tier,
            AVG(Profit_Margin) * 100 AS avg_profit_margin,
            COUNT(*) AS cnt
        FROM food_orders 
        WHERE 1=1
        {{WHERE}}
        GROUP BY discount_tier
        ORDER BY MIN(Discount_Applied)


-- ── Task : High-Revenue Cities
SELECT City, SUM(Order_Value) AS revenue
        FROM food_orders
        WHERE 1=1 {{WHERE}}
        GROUP BY City
        ORDER BY revenue DESC
        LIMIT 5

-- ── Task : High-Revenue Country
SELECT Cuisine_Type, SUM(Order_Value) AS revenue
        FROM food_orders
        WHERE 1=1 
        {{WHERE}}
        GROUP BY Cuisine_Type
        ORDER BY revenue DESC
        LIMIT 5


-- ── Task : Avg Delivery Time by City
SELECT City, AVG(Delivery_Time_Min) AS avg_time
        FROM food_orders
        WHERE 1=1 
        {{WHERE}}
        GROUP BY City
        ORDER BY avg_time DESC
        LIMIT 10


-- ── Task : Distance vs Delivery Delay
SELECT Distance_km, Delivery_Time_Min
        FROM food_orders
        WHERE 1=1 {{WHERE}}
          AND Distance_km IS NOT NULL
          AND Delivery_Time_Min IS NOT NULL
        ORDER BY RAND() LIMIT 3000


-- ── Task : Delivery Rating vs Delivery Time
SELECT ROUND(Delivery_Rating) AS rating,
               AVG(Delivery_Time_Min) AS avg_time
        FROM food_orders
        WHERE 1=1 {{WHERE}}
          AND Delivery_Rating IS NOT NULL
        GROUP BY rating ORDER BY rating


-- ── Task : Top Rated Restaurants
SELECT Restaurant_Name,
               AVG(Restaurant_Rating) AS avg_rating,
               COUNT(*) AS total_orders
        FROM food_orders
        WHERE 1=1 {{WHERE}}
        GROUP BY Restaurant_Name
        HAVING total_orders >= 30
        ORDER BY avg_rating DESC LIMIT 10


-- ── Task : Cancellation Rate by Restaurant
SELECT Restaurant_Name,
               COUNT(*) AS total_orders,
               SUM(CASE WHEN LOWER(Order_Status) LIKE '%%cancel%%' THEN 1 ELSE 0 END)
               * 100.0 / COUNT(*) AS cancel_rate
        FROM food_orders
        WHERE 1=1 {{WHERE}}
        GROUP BY Restaurant_Name
        HAVING total_orders >= 30
        ORDER BY cancel_rate DESC LIMIT 10;


-- ── Task : Cuisine-wise Performance
SELECT Cuisine_Type,
               AVG(Order_Value) AS avg_value,
               AVG(Restaurant_Rating) AS avg_rating
        FROM food_orders
        WHERE 1=1 {{WHERE}}
        GROUP BY Cuisine_Type
        ORDER BY COUNT(*) DESC LIMIT 8


-- ── Task : Peak Hour Demand
SELECT
            CASE WHEN Peak_Hour = 1 THEN 'Peak Hour' ELSE 'Non-Peak' END AS hour_type,
            COUNT(*) AS order_count,
            AVG(Order_Value) AS avg_value
        FROM food_orders
        WHERE 1=1 {{WHERE}}
        GROUP BY hour_type


-- ── Task : Payment Mode Preferences
SELECT Payment_Mode, COUNT(*) AS cnt
        FROM food_orders
        WHERE 1=1 {{WHERE}}
          AND Payment_Mode IS NOT NULL
        GROUP BY Payment_Mode ORDER BY cnt DESC


-- ── Task : Cancellation Reason Analysis
SELECT Cancellation_Reason, COUNT(*) AS cnt
        FROM food_orders
        WHERE 1=1 {{WHERE}}
          AND LOWER(Order_Status) LIKE '%%cancel%%'
          AND Cancellation_Reason IS NOT NULL
          AND Cancellation_Reason != 'Not Cancelled'
        GROUP BY Cancellation_Reason
        ORDER BY cnt DESC LIMIT 8
