from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class AddIn(BaseModel):
    product_id: int
    qty: int

@router.post("/add")
def add_to_cart(data: AddIn, user_id: int, db: Session = Depends(get_session)):
    cart = db.execute(text("SELECT id FROM carts WHERE user_id=:u AND status='open'"),
                      {"u": user_id}).fetchone()
    if not cart:
        cart = db.execute(text("INSERT INTO carts (user_id) VALUES (:u) RETURNING id"),
                          {"u": user_id}).fetchone()
    db.execute(text("""
        INSERT INTO cart_items (cart_id, product_id, qty) VALUES (:c, :p, :q)
        ON CONFLICT (cart_id, product_id) DO UPDATE SET qty = cart_items.qty + EXCLUDED.qty
    """), {"c": cart[0], "p": data.product_id, "q": data.qty})
    db.commit()
    return {"cart_id": cart[0], "status": "ok"}

@router.get("/")
def get_cart(user_id: int, db: Session = Depends(get_session)):
    rows = db.execute(text("""
        SELECT ci.product_id, p.name, ci.qty, p.price, ci.qty * p.price AS subtotal
        FROM carts c
        JOIN cart_items ci ON ci.cart_id = c.id
        JOIN products p ON p.id = ci.product_id
        WHERE c.user_id=:u AND c.status='open'
    """), {"u": user_id}).fetchall()
    total = sum(r[4] for r in rows)
    return {"items": [dict(r._mapping) for r in rows], "total": total}
