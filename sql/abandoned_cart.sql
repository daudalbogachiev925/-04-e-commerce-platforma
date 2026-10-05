SELECT c.id AS cart_id,
       c.user_id,
       COUNT(ci.product_id) AS items,
       SUM(ci.qty * p.price) AS cart_value,
       c.created
FROM carts c
JOIN cart_items ci ON ci.cart_id = c.id
JOIN products p ON p.id = ci.product_id
WHERE c.status = 'open'
  AND c.created < NOW() - INTERVAL '24 hours'
GROUP BY c.id
ORDER BY cart_value DESC;
