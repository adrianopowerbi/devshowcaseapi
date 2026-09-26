"""Configuração da conexão com o banco de dados (SQLite)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./devshowcase.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Fornece uma sessão de banco de dados por requisição (dependency injection)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
