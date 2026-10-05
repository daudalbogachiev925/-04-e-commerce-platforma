from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, Numeric, Boolean, TIMESTAMP, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True)
    sku = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    price = Column(Numeric(12,2))
    stock = Column(Integer, default=0)
    active = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    total = Column(Numeric(12,2))
    status = Column(String, default="pending")
    address = Column(String)
