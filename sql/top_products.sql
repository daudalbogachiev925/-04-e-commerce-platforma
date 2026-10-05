SELECT p.id, p.name, p.price,
       COUNT(oi.order_id) AS orders,
       SUM(oi.qty) AS units_sold,
       SUM(oi.qty * oi.price) AS revenue
FROM products p
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o ON o.id = oi.order_id AND o.status = 'paid'
GROUP BY p.id
ORDER BY revenue DESC
LIMIT 20;
