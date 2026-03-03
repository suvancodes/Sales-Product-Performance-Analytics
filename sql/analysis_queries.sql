-- Active: 1771784571765@@127.0.0.1@3306@ecommerce_analytics

GRANT ALL PRIVILEGES ON ecommerce_analytics.* TO 'root'@'localhost';
FLUSH PRIVILEGES;


USE ecommerce_analytics;
SELECT* FROM master_sales;

-- monthly_revenue

SELECT
    MONTH(order_date) AS month,
    SUM(revenue) AS monthly_revenue
FROM master_sales
GROUP BY MONTH(order_date)
ORDER BY month;

-- country wise revenue
SELECT
    country,
    SUM(revenue) AS total_revenue
FROM master_sales
GROUP BY country
ORDER BY total_revenue DESC;

SELECT
    source,
    SUM(revenue) AS total_revenue
FROM master_sales
GROUP BY source;

CREATE TABLE IF NOT EXISTS products AS
SELECT DISTINCT
    sku,
    'General' AS category,
    'NA' AS size,
    'NA' AS color
FROM master_sales;

SELECT
    m.sku,
    p.category,
    SUM(m.revenue) AS total_revenue
FROM master_sales m
JOIN products p
ON m.sku = p.sku
GROUP BY m.sku, p.category
ORDER BY total_revenue DESC
LIMIT 10;
DROP TABLE products;



SELECT COUNT(*) AS total_rows FROM master_sales;

