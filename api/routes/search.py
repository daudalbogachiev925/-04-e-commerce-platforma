from fastapi import APIRouter
from elasticsearch import Elasticsearch

router = APIRouter()
ES = Elasticsearch("http://localhost:9200")

@router.get("/")
def search(q: str, limit: int = 20):
    res = ES.search(index="products", body={
        "query": {"multi_match": {
            "query": q,
            "fields": ["name^3", "description"]
        }},
        "size": limit
    })
    return [{"id": h["_id"], "score": h["_score"], **h["_source"]}
            for h in res["hits"]["hits"]]
