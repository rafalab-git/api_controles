# src/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Se preferir, defina via variável de ambiente (ou configure no docker-compose)
DB_NAME = os.getenv("DB_NAME", "controles.db")
DB_PATH = f"sqlite:///{DB_NAME}"

engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Cria as tabelas no banco de dados, se não existirem
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


