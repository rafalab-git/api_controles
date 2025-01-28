# src/models.py

from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Controle(Base):
    __tablename__ = "controles"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    code = Column(String, index=True)
    name = Column(String, default="")
    
    # Novo campo booleano, default = False
    controle_status = Column(Boolean, default=False)

    # Exemplo de unicidade (opcional)
    __table_args__ = (
        UniqueConstraint('client_id', 'code', name='uix_client_code'),
    )

# ---- MODELOS PYDANTIC ----
from pydantic import BaseModel

class ControleBase(BaseModel):
    code: str
    name: str = ""
    # Por padrão, é False. Se o usuário não enviar nada, fica False.
    controle_status: bool = False

class ControleCreate(ControleBase):
    pass

class ControleRead(ControleBase):
    id: int
    client_id: str

    class Config:
        orm_mode = True
