"""DTOs de entrada (com validação) e de saída da API."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


# ---------- Profile ----------

class ProfileCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    bio: Optional[str] = Field(default=None, max_length=500)
    githubUrl: Optional[HttpUrl] = None
    linkedinUrl: Optional[HttpUrl] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O nome é obrigatório")
        return v.strip()


class ProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    bio: Optional[str] = None
    githubUrl: Optional[str] = None
    linkedinUrl: Optional[str] = None
    createdAt: datetime


# ---------- Technology ----------

class TechnologyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O nome da tecnologia é obrigatório")
        return v.strip()


class TechnologyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


# ---------- Project ----------

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = Field(default=None, max_length=1000)
    repositoryUrl: HttpUrl
    demoUrl: Optional[HttpUrl] = None
    profileId: int
    technologyIds: Optional[List[int]] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O título é obrigatório")
        return v.strip()


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    repositoryUrl: str
    demoUrl: Optional[str] = None
    profileId: int
    profileName: str
    technologies: List[TechnologyOut] = []
    createdAt: datetime
