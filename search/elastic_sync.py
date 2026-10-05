from elasticsearch import Elasticsearch
import psycopg2

ES = Elasticsearch("http://localhost:9200")
INDEX = "products"

def recreate_index():
    if ES.indices.exists(index=INDEX):
        ES.indices.delete(index=INDEX)
    ES.indices.create(index=INDEX, body={
        "mappings": {"properties": {
            "sku": {"type": "keyword"},
            "name": {"type": "text"},
            "description": {"type": "text"},
            "price": {"type": "float"}
        }}})

def sync_products():
    conn = psycopg2.connect("dbname=shop user=shop password=shop host=localhost")
    cur = conn.cursor()
    cur.execute("SELECT id, sku, name, description, price FROM products WHERE active")
    for row in cur.fetchall():
        ES.index(index=INDEX, id=row[0], document={
            "sku": row[1], "name": row[2], "description": row[3], "price": float(row[4])})

if __name__ == "__main__":
    recreate_index()
    sync_products()
    print("Готово")
