"""Endpoints de Profile (Perfil do Desenvolvedor)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.post("", response_model=schemas.ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(payload: schemas.ProfileCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(models.Profile)
        .filter(models.Profile.email.ilike(payload.email))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um perfil com o e-mail {payload.email}",
        )

    profile = models.Profile(
        name=payload.name,
        email=payload.email,
        bio=payload.bio,
        githubUrl=str(payload.githubUrl) if payload.githubUrl else None,
        linkedinUrl=str(payload.linkedinUrl) if payload.linkedinUrl else None,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=schemas.ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil não encontrado: {profile_id}",
        )
    return profile
