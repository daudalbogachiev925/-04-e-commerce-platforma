# Архитектура

API (FastAPI) → Postgres (данные) + Redis (корзина, сессии) + Elastic (поиск).

Поток оформления заказа:
1. POST /cart/add → Redis + Postgres
2. POST /orders/checkout → транзакция (заказ + списание остатков)
3. Ответ с order_id

Аналитика читает напрямую Postgres, не нагружает API.
