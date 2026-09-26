"""Endpoints de Project (Projeto)."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == payload.profileId).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil não encontrado: {payload.profileId}",
        )

    technology_ids = payload.technologyIds or []
    technologies = []
    if technology_ids:
        technologies = (
            db.query(models.Technology)
            .filter(models.Technology.id.in_(technology_ids))
            .all()
        )
        if len(technologies) != len(set(technology_ids)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Uma ou mais tecnologias informadas não existem",
            )

    project = models.Project(
        title=payload.title,
        description=payload.description,
        repositoryUrl=str(payload.repositoryUrl),
        demoUrl=str(payload.demoUrl) if payload.demoUrl else None,
        profileId=profile.id,
    )
    project.technologies = technologies

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()
