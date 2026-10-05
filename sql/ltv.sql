SELECT u.id, u.email,
       COUNT(o.id) AS orders,
       COALESCE(SUM(o.total),0) AS ltv,
       COALESCE(AVG(o.total),0) AS avg_order,
       MAX(o.created) AS last_order
FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'paid'
GROUP BY u.id
ORDER BY ltv DESC;
