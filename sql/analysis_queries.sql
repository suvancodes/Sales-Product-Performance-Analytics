-- Active: 1770901343716@@127.0.0.1@3306@mysql

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

CREATE TABLE products (
    sku VARCHAR(50),
    category VARCHAR(100),
    size VARCHAR(20),
    color VARCHAR(20)
);


SELECT
    m.sku,
    p.category,
    SUM(m.revenue) AS total_revenue
FROM master_sales m
JOIN products p
ON m.sku = p.sku
GROUP BY m.sku, p.category
ORDER BY total_revenue DESC;


SELECT * FROM products;
SELECT COUNT(*) FROM products;