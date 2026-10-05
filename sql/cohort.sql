WITH first_order AS (
    SELECT user_id, MIN(date_trunc('month', created)) AS cohort
    FROM orders
    GROUP BY user_id
)
SELECT f.cohort,
       date_trunc('month', o.created) AS month,
       COUNT(DISTINCT o.user_id) AS users,
       SUM(o.total) AS revenue
FROM orders o
JOIN first_order f ON f.user_id = o.user_id
GROUP BY f.cohort, month
ORDER BY f.cohort, month;
