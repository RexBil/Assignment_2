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

-- ── Task 1: Top 10 Spending Customers ──
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id)       AS total_orders,
    SUM(o.order_value)      AS total_spend,
    AVG(o.order_value)      AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status != 'Cancelled'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_spend DESC
LIMIT 10;


-- ── Task 2: Age Group vs Order Value ──
SELECT
    CASE
        WHEN c.customer_age < 18             THEN 'Under 18'
        WHEN c.customer_age BETWEEN 18 AND 25 THEN '18-25'
        WHEN c.customer_age BETWEEN 26 AND 35 THEN '26-35'
        WHEN c.customer_age BETWEEN 36 AND 45 THEN '36-45'
        WHEN c.customer_age BETWEEN 46 AND 60 THEN '46-60'
        ELSE '60+'
    END AS age_group,
    COUNT(o.order_id)   AS total_orders,
    AVG(o.order_value)  AS avg_order_value,
    SUM(o.order_value)  AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY age_group
ORDER BY avg_order_value DESC;


-- ── Task 3: Weekend vs Weekday Order Patterns ──
SELECT
    CASE WHEN DAYOFWEEK(o.order_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    COUNT(*)            AS total_orders,
    AVG(o.order_value)  AS avg_order_value,
    SUM(o.order_value)  AS total_revenue
FROM orders o
GROUP BY day_type;


-- ── Task 4: Monthly Revenue Trends ──
SELECT
    DATE_FORMAT(order_date, '%Y-%m')    AS month,
    COUNT(*)                            AS total_orders,
    SUM(order_value)                    AS total_revenue,
    AVG(order_value)                    AS avg_order_value
FROM orders
WHERE order_status != 'Cancelled'
GROUP BY month
ORDER BY month;


-- ── Task 5: Discount Impact on Profit ──
SELECT
    CASE
        WHEN o.discount_amount = 0             THEN 'No Discount'
        WHEN o.discount_amount BETWEEN 1 AND 50 THEN 'Low (1-50)'
        WHEN o.discount_amount BETWEEN 51 AND 150 THEN 'Medium (51-150)'
        ELSE 'High (150+)'
    END AS discount_tier,
    COUNT(*)                AS order_count,
    AVG(f.profit_margin)    AS avg_profit_margin,
    SUM(f.revenue)          AS total_revenue
FROM orders o
JOIN financials f ON o.order_id = f.order_id
GROUP BY discount_tier
ORDER BY avg_profit_margin DESC;


-- ── Task 6: High-Revenue Cities ──
SELECT
    city,
    COUNT(*)            AS total_orders,
    SUM(order_value)    AS total_revenue,
    AVG(order_value)    AS avg_order_value
FROM orders
WHERE order_status != 'Cancelled'
GROUP BY city
ORDER BY total_revenue DESC
LIMIT 10;


-- ── Task 7: Avg Delivery Time by City ──
SELECT
    o.city,
    AVG(d.delivery_time_minutes)    AS avg_delivery_time,
    MIN(d.delivery_time_minutes)    AS min_delivery_time,
    MAX(d.delivery_time_minutes)    AS max_delivery_time,
    COUNT(*)                        AS deliveries
FROM orders o
JOIN deliveries d ON o.order_id = d.order_id
WHERE o.order_status = 'Delivered'
GROUP BY o.city
ORDER BY avg_delivery_time DESC
LIMIT 15;


-- ── Task 8: Distance vs Delivery Delay ──
SELECT
    CASE
        WHEN d.distance_km <= 3   THEN '0-3 km'
        WHEN d.distance_km <= 7   THEN '3-7 km'
        WHEN d.distance_km <= 12  THEN '7-12 km'
        ELSE '12+ km'
    END AS distance_range,
    AVG(d.delivery_time_minutes) AS avg_delivery_time,
    COUNT(*)                     AS order_count
FROM deliveries d
GROUP BY distance_range
ORDER BY avg_delivery_time;


-- ── Task 9: Delivery Rating vs Delivery Time ──
SELECT
    ROUND(d.delivery_rating) AS rating,
    AVG(d.delivery_time_minutes) AS avg_delivery_time,
    COUNT(*) AS order_count
FROM deliveries d
WHERE d.delivery_rating IS NOT NULL
GROUP BY ROUND(d.delivery_rating)
ORDER BY rating;


-- ── Task 10: Top Rated Restaurants ──
SELECT
    r.restaurant_name,
    r.cuisine_type,
    r.city,
    r.restaurant_rating,
    COUNT(o.order_id) AS total_orders
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.restaurant_name, r.cuisine_type, r.city, r.restaurant_rating
HAVING total_orders >= 50
ORDER BY r.restaurant_rating DESC
LIMIT 10;


-- ── Task 11: Cancellation Rate by Restaurant ──
SELECT
    r.restaurant_name,
    COUNT(o.order_id)                                                   AS total_orders,
    SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END)      AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END)
        / COUNT(o.order_id) * 100, 2
    )                                                                   AS cancellation_rate_pct
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id, r.restaurant_name
HAVING total_orders >= 30
ORDER BY cancellation_rate_pct DESC
LIMIT 10;


-- ── Task 12: Cuisine-wise Performance ──
SELECT
    cuisine_type,
    COUNT(*)            AS total_orders,
    SUM(order_value)    AS total_revenue,
    AVG(order_value)    AS avg_order_value,
    ROUND(
        SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END)
        / COUNT(*) * 100, 2
    )                   AS cancellation_rate_pct
FROM orders
GROUP BY cuisine_type
ORDER BY total_revenue DESC;


-- ── Task 13: Peak Hour Demand ──
SELECT
    HOUR(order_date)    AS order_hour,
    COUNT(*)            AS total_orders,
    SUM(order_value)    AS total_revenue
FROM orders
GROUP BY order_hour
ORDER BY order_hour;


-- ── Task 14: Payment Mode Preferences ──
SELECT
    payment_mode,
    COUNT(*)            AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) AS pct_share,
    AVG(order_value)    AS avg_order_value
FROM orders
GROUP BY payment_mode
ORDER BY total_orders DESC;


-- ── Task 15: Cancellation Reason Analysis ──
SELECT
    cancellation_reason,
    COUNT(*)            AS cancellation_count,
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM orders WHERE order_status = 'Cancelled'
    ), 2)               AS pct_of_cancellations
FROM orders
WHERE order_status = 'Cancelled'
  AND cancellation_reason IS NOT NULL
GROUP BY cancellation_reason
ORDER BY cancellation_count DESC;
