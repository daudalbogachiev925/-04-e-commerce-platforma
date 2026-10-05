# E-commerce платформа

Полноценный интернет-магазин: каталог, корзина, заказ, оплата, аналитика.
Стек: FastAPI + PostgreSQL + Redis + Elasticsearch + Docker.

## Возможности
- Каталог товаров с категориями и тегами
- Поиск (Elasticsearch)
- Корзина (Redis)
- Оформление заказа с резервированием остатков
- История заказов пользователя
- Аналитика: LTV, когорты, брошенные корзины, топ товаров
- REST API + OpenAPI

## Быстрый старт
```bash
cp .env.example .env
docker-compose up -d
make migrate
make seed
make run

Сервисы
API: http://localhost:8000/docs

Postgres: localhost:5432

Redis: localhost:6379

Elastic: localhost:9200

db/         — SQL-схема и миграции
sql/        — аналитические отчёты
api/        — FastAPI-приложение
search/     — синхронизация с Elastic
tests/      — pytest-тесты
docs/       — архитектура


### .env.example

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=shop
POSTGRES_PASSWORD=shop
POSTGRES_DB=shop

REDIS_HOST=localhost
REDIS_PORT=6379

ELASTIC_URL=http://localhost:9200
SECRET_KEY=change-me


### requirements.txt

fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
redis==5.0.8
elasticsearch==8.15.0
pydantic==2.9.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pandas==2.2.3
pytest==8.3.3
httpx==0.27.2



### docker-compose.yml
```yaml
version: "3.9"
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: shop
      POSTGRES_PASSWORD: shop
      POSTGRES_DB: shop
    ports: ["5432:5432"]
    volumes: ["pg:/var/lib/postgresql/data"]

  redis:
    image: redis:7
    ports: ["6379:6379"]

  elastic:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    environment:
      discovery.type: single-node
      xpack.security.enabled: "false"
    ports: ["9200:9200"]

  api:
    build: ./api
    depends_on: [postgres, redis, elastic]
    ports: ["8000:8000"]
    env_file: .env
    command: uvicorn main:app --host 0.0.0.0 --port 8000

volumes:
  pg:
