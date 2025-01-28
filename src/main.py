# src/main.py

from fastapi import FastAPI, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import init_db, get_db
from .models import Controle, ControleCreate, ControleRead
import os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")
app = FastAPI(title="API de Controles")

@app.on_event("startup")
def startup_event():
    init_db()

def verify_bearer_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token ausente ou inválido",
        )
    token = auth_header.replace("Bearer ", "")
    if token != token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido",
        )
    return True

@app.get("/api/{client_id}/controles", response_model=List[ControleRead])
def list_controles(
    client_id: str,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_bearer_token),
):
    """Lista todos os controles de um cliente específico."""
    return db.query(Controle).filter(Controle.client_id == client_id).all()


@app.post("/api/{client_id}/controles", response_model=ControleRead, status_code=status.HTTP_201_CREATED)
def create_controle(
    client_id: str,
    controle_in: ControleCreate,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_bearer_token),
):
    """
    Cria um novo registro de controle para um cliente específico (client_id).
    Se não for enviado controle_status, ficará false por padrão.
    """
    # Verifica se (client_id, code) já existe
    existing = db.query(Controle).filter_by(client_id=client_id, code=controle_in.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este code já está cadastrado para esse client_id."
        )

    # Cria o controle com status default = False (caso não seja enviado)
    controle = Controle(
        client_id=client_id,
        code=controle_in.code,
        name=controle_in.name,
        controle_status=controle_in.controle_status  # vem do Pydantic (default False)
    )
    db.add(controle)
    db.commit()
    db.refresh(controle)
    return controle


@app.delete("/api/{client_id}/controles/{controle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_controle(
    client_id: str,
    controle_id: int,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_bearer_token),
):
    """Deleta um controle pelo ID e client_id."""
    controle = db.query(Controle).filter_by(id=controle_id, client_id=client_id).first()
    if not controle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Controle não encontrado para este client_id."
        )
    db.delete(controle)
    db.commit()
    return None

@app.patch("/api/{client_id}/controles/{controle_id}/ativar", response_model=ControleRead)
def activate_controle(
    client_id: str,
    controle_id: int,
    db: Session = Depends(get_db),
    authorized: bool = Depends(verify_bearer_token),
):
    controle = db.query(Controle).filter_by(id=controle_id, client_id=client_id).first()
    if not controle:
        raise HTTPException(status_code=404, detail="Controle não encontrado.")
    controle.controle_status = True
    db.commit()
    db.refresh(controle)
    return controle
