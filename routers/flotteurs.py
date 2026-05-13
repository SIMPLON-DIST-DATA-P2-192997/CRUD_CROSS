from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Flotteur
from pydantic_schemas.flotteur import FlotteurCreate, FlotteurRead, FlotteurUpdate

router = APIRouter(prefix="/flotteurs", tags=["Flotteurs"])


@router.get("/", response_model=List[FlotteurRead])
def get_flotteurs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Flotteur).offset(skip).limit(limit).all()


@router.get("/{flotteur_id}", response_model=FlotteurRead)
def get_flotteur(flotteur_id: int, db: Session = Depends(get_db)):
    flotteur = db.query(Flotteur).filter(Flotteur.id == flotteur_id).first()
    if not flotteur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flotteur not found")
    return flotteur


@router.get("/by-operation/{operation_id}", response_model=List[FlotteurRead])
def get_flotteurs_by_operation(operation_id: int, db: Session = Depends(get_db)):
    return db.query(Flotteur).filter(Flotteur.operation_id == operation_id).all()


@router.post("/", response_model=FlotteurRead, status_code=status.HTTP_201_CREATED)
def create_flotteur(payload: FlotteurCreate, db: Session = Depends(get_db)):
    flotteur = Flotteur(**payload.model_dump())
    db.add(flotteur)
    db.commit()
    db.refresh(flotteur)
    return flotteur


@router.put("/{flotteur_id}", response_model=FlotteurRead)
def update_flotteur(flotteur_id: int, payload: FlotteurUpdate, db: Session = Depends(get_db)):
    flotteur = db.query(Flotteur).filter(Flotteur.id == flotteur_id).first()
    if not flotteur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flotteur not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(flotteur, field, value)
    db.commit()
    db.refresh(flotteur)
    return flotteur


@router.delete("/{flotteur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flotteur(flotteur_id: int, db: Session = Depends(get_db)):
    flotteur = db.query(Flotteur).filter(Flotteur.id == flotteur_id).first()
    if not flotteur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flotteur not found")
    db.delete(flotteur)
    db.commit()
