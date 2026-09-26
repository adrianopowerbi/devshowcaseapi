"""Endpoints de Technology (Tecnologia)."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/technologies", tags=["technologies"])


@router.post("", response_model=schemas.TechnologyOut, status_code=status.HTTP_201_CREATED)
def create_technology(payload: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(models.Technology)
        .filter(models.Technology.name.ilike(payload.name))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tecnologia já cadastrada: {payload.name}",
        )

    technology = models.Technology(name=payload.name)
    db.add(technology)
    db.commit()
    db.refresh(technology)
    return technology


@router.get("", response_model=List[schemas.TechnologyOut])
def list_technologies(db: Session = Depends(get_db)):
    return db.query(models.Technology).order_by(models.Technology.name).all()
