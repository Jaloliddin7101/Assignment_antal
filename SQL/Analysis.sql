WITH 
    ##calculate total sales and number of transactions for each month
    MonthlySales AS (
    SELECT
    EXTRACT(YEAR FROM purchase_date) AS year,
    EXTRACT(MONTH FROM purchase_date) AS month,
    COUNT(transaction_id) AS total_transactions,
    SUM(p.price * st.quantity_purchased) AS total_sales
    FROM sales_transactions st
    JOIN products p ON st.product_id = p.product_id
    GROUP BY year, month
),
    ##calculate moving average for each month
MovingAverage AS (
    SELECT 
    year,
    month,
    total_sales,
    AVG(total_sales) OVER (ORDER BY year, month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_sales
    FROM MonthlySales
)
SELECT
year,
month,
total_transactions,
total_sales,
moving_avg_sales
FROM MovingAverage
ORDER BY
year, month;
