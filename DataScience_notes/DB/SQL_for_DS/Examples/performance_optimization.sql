""" EXPLAIN to Analyze Query Performance/Query Execution Plan"""
EXPLAIN SELECT * FROM orders WHERE status = 'shipped';

EXPLAIN SELECT f.title, a.actor_name
FROM film f, film_actor fa,  actor a
WHERE f.film_id = fa.film_id and fa.actor_id = a.id 

""" Consider Denormalization for Performance"""

""" Partitioning Large Tables"""
ALTER TABLE sales
PARTITION BY RANGE (YEAR(sale_date)) (
  PARTITION p0 VALUES LESS THAN (2010),
  PARTITION p1 VALUES LESS THAN (2020),
  PARTITION p2 VALUES LESS THAN MAXVALUE
);

""" Avoid N+1 Query Problems i.e. SELECT *"""
""" Avoid SELECT Inside Loops"""

""" Retreiving relevant columns, refining the `WHERE` clause, and sorting efficiently with `ORDER BY`"""
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column;
LIMIT 5;

""" Avoid functions on columns eg. year[hire_date]"""
SELECT * 
FROM employees 
WHERE hire_date >= '2020-01-01' AND hire_date < '2021-01-01';

"""Avoid Unnecessary Ordering and Grouping
a. Use indexes. 
b. Push sorting to the application layer. If
c. Pre-aggregate data."""

""" Indexing columns that are frequently used in `WHERE`, `JOIN`, and `ORDER BY` clauses."""
CREATE INDEX idx_customer_id ON orders(customer_id);
SELECT order_id, total_amount
FROM orders
WHERE customer_id = 12345;


""" Subquery optimization with the use of 
a. un-correaled sub-queries
b. Use EXISTS Instead of IN for Subqueries
c. derived tables/CTE and 
d. efficient joins"""

""" EXISTS Instead of IN for Subqueries"""
SELECT * 
FROM orders o
WHERE EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id AND c.country = 'USA');

""" Derived tables/CTE"""
SELECT e.first_name, e.last_name, d.department_name
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE d.department_name = 'Engineering';

WITH SalesCTE AS ( 
             SELECT salesperson_id, SUM(sales_amount) AS total_sales 
             FROM sales GROUP BY salesperson_id ) 

SELECT salesperson_id, total_sales 
FROM SalesCTE WHERE total_sales > 5000;

""" Avoid Wildcards at the Start of LIKE: Using % at the beginning of a LIKE pattern disables index use and leads to full table scans."""
SELECT * FROM users WHERE name LIKE 'john%';

""" Use Joins Efficiently"""
CREATE INDEX idx_customer_id ON orders(customer_id); 
SELECT * 
FROM customers 
INNER JOIN orders ON customers.id = orders.customer_id;

WITH RecentOrders AS (
    SELECT customer_id, order_id
    FROM orders
    WHERE order_date >= DATE('now', '-30 days') 
)
SELECT c.customer_name, ro.order_id
FROM customers c
INNER JOIN RecentOrders ro ON c.customer_id = ro.customer_id;

""" Limit the use of DISTINCT through
a. remove duplicate data during data cleaning processes
b. Use GROUP BY instead of DISTINCT when possible.
c. Use window functions."""
SELECT city FROM customers GROUP BY city;

""" Use UNION ALL Instead of UNION"""
SELECT product_id FROM products WHERE category = 'Electronics'
UNION ALL
SELECT product_id FROM products WHERE category = 'Books';

""" Break Down Complex Queries"""
-- Create a materialized view
CREATE MATERIALIZED VIEW daily_sales AS
SELECT product_id, SUM(quantity) AS total_quantity
FROM order_items
GROUP BY product_id;

-- Query the materialized view
SELECT * FROM daily_sales;

""" Pagination Optimization: For deep pagination, use the “seek method” (also called keyset pagination or cursor-based pagination) to avoid scanning excessive data."""
""" Use search_after (or similar cursor-based techniques) instead of LIMIT for deep pagination."""
-- Deep pagination (poor performance)
SELECT * FROM orders ORDER BY order_time DESC LIMIT 9990, 10;

-- Optimized: use a cursor
SELECT * FROM orders
WHERE order_time < '2023-01-01 12:00:00'
ORDER BY order_time DESC
LIMIT 10;

""" Query Caching"""
SET GLOBAL query_cache_size = 1048576; 
SET GLOBAL query_cache_type = 1;

String result = redis.get("orders:user:123");
if (result == null) {
    result = database.query("SELECT * FROM orders WHERE user_id = 123");
    redis.set("orders:user:123", result, 3600); // Cache for 1 hour
}

""" Utilize stored procedures (a set of SQL commands/a reusable script. we save in our database so we don’t have to write the same SQL repeatedly)"""