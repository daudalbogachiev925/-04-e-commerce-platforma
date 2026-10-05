from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_session
from models import Product

router = APIRouter()

@router.get("/")
def list_products(category_id: int | None = None,
                  q: str | None = None,
                  limit: int = Query(20, le=100),
                  offset: int = 0,
                  db: Session = Depends(get_session)):
    query = db.query(Product).filter(Product.active == True)
    if category_id: query = query.filter(Product.category_id == category_id)
    if q: query = query.filter(Product.name.ilike(f"%{q}%"))
    return query.limit(limit).offset(offset).all()

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_session)):
    p = db.query(Product).get(product_id)
    if not p: raise HTTPException(404, "Товар не найден")
    return p
