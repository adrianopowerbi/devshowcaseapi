"""Entidades (tabelas) da aplicação, mapeadas com SQLAlchemy."""
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base

# Tabela de associação do relacionamento N:N entre Project e Technology
project_technologies = Table(
    "project_technologies",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
    Column("technology_id", Integer, ForeignKey("technologies.id"), primary_key=True),
)


class Profile(Base):
    """Perfil do desenvolvedor. Profile 1 : N Project."""

    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    bio = Column(String(500), nullable=True)
    githubUrl = Column(String(500), nullable=True)
    linkedinUrl = Column(String(500), nullable=True)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)

    projects = relationship(
        "Project", back_populates="profile", cascade="all, delete-orphan"
    )


class Technology(Base):
    """Tecnologia usada em projetos. Project N : N Technology."""

    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    projects = relationship(
        "Project", secondary=project_technologies, back_populates="technologies"
    )


class Project(Base):
    """Projeto de portfólio. N : 1 com Profile, N : N com Technology, 1 : N com Feedback."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(1000), nullable=True)
    repositoryUrl = Column(String(500), nullable=False)
    demoUrl = Column(String(500), nullable=True)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)

    profileId = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    profile = relationship("Profile", back_populates="projects")

    technologies = relationship(
        "Technology", secondary=project_technologies, back_populates="projects"
    )

    feedbacks = relationship(
        "Feedback", back_populates="project", cascade="all, delete-orphan"
    )

    @property
    def profileName(self) -> str:
        """Nome do dono do projeto, usado nas respostas da API."""
        return self.profile.name if self.profile else None


class Feedback(Base):
    """Opinião/avaliação recebida em um projeto. Feedback N : 1 Project."""

    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    authorName = Column(String(100), nullable=False)
    comment = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)

    projectId = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="feedbacks")
