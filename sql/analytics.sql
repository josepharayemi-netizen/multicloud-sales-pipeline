-- Executive KPIs
SELECT COUNT(*) AS orders, SUM(revenue) AS revenue, SUM(profit) AS profit,
       AVG(revenue) AS average_order_value
FROM sales;

-- Regional performance
SELECT region, SUM(revenue) AS revenue, SUM(profit) AS profit
FROM sales GROUP BY region ORDER BY revenue DESC;

-- Product performance
SELECT product, SUM(quantity) AS units, SUM(revenue) AS revenue,
       SUM(profit) AS profit
FROM sales GROUP BY product ORDER BY revenue DESC;
