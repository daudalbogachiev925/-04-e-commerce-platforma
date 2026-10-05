from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DSN = f"postgresql://{os.getenv('POSTGRES_USER','shop')}:{os.getenv('POSTGRES_PASSWORD','shop')}@{os.getenv('POSTGRES_HOST','localhost')}:{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('POSTGRES_DB','shop')}"
engine = create_engine(DSN, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_session():
    s = SessionLocal()
    try: yield s
    finally: s.close()
