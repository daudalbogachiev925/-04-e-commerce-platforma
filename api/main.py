from fastapi import FastAPI
from routes import products, cart, orders, auth, search

app = FastAPI(title="E-commerce API", version="1.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/health")
def health(): return {"status": "ok"}
