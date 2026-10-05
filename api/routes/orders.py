from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_session

router = APIRouter()

class CheckoutIn(BaseModel):
    user_id: int
    address: str

@router.post("/checkout")
def checkout(data: CheckoutIn, db: Session = Depends(get_session)):
    # 1. Находим открытую корзину
    cart = db.execute(text("SELECT id FROM carts WHERE user_id=:u AND status='open'"),
                      {"u": data.user_id}).fetchone()
    if not cart: raise HTTPException(400, "Корзина пуста")
    cart_id = cart[0]

    # 2. Считаем сумму
    items = db.execute(text("""
        SELECT ci.product_id, ci.qty, p.price, p.stock
        FROM cart_items ci JOIN products p ON p.id=ci.product_id
        WHERE ci.cart_id=:c
    """), {"c": cart_id}).fetchall()
    if not items: raise HTTPException(400, "Корзина пуста")

    # 3. Проверяем остатки
    for pid, qty, price, stock in items:
        if stock < qty:
            raise HTTPException(400, f"Товар {pid}: осталось {stock}")

    # 4. Создаём заказ
    total = sum(qty * price for _, qty, price, _ in items)
    order = db.execute(text("""
        INSERT INTO orders (user_id, total, status, address)
        VALUES (:u, :t, 'pending', :a) RETURNING id
    """), {"u": data.user_id, "t": total, "a": data.address}).fetchone()
    order_id = order[0]

    # 5. Переносим позиции и списываем остатки
    for pid, qty, price, _ in items:
        db.execute(text("INSERT INTO order_items (order_id, product_id, qty, price) VALUES (:o,:p,:q,:pr)"),
                   {"o": order_id, "p": pid, "q": qty, "pr": price})
        db.execute(text("UPDATE products SET stock = stock - :q WHERE id=:p"),
                   {"q": qty, "p": pid})

    db.execute(text("UPDATE carts SET status='done' WHERE id=:c"), {"c": cart_id})
    db.commit()
    return {"order_id": order_id, "total": float(total), "status": "pending"}

@router.get("/{user_id}")
def my_orders(user_id: int, db: Session = Depends(get_session)):
    rows = db.execute(text("""
        SELECT o.id, o.total, o.status, o.created,
               (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id=o.id) AS items
        FROM orders o WHERE o.user_id=:u ORDER BY o.created DESC
    """), {"u": user_id}).fetchall()
    return [dict(r._mapping) for r in rows]
