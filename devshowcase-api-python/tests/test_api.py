"""Testes de integração dos endpoints da DevShowcase API."""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Banco em memória, isolado, só para os testes
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_creates_profile_and_finds_it_by_id():
    response = client.post(
        "/api/profiles",
        json={
            "name": "Ana Souza",
            "email": "ana@example.com",
            "bio": "Dev backend",
            "githubUrl": "https://github.com/ana",
        },
    )
    assert response.status_code == 201
    profile_id = response.json()["id"]

    get_response = client.get(f"/api/profiles/{profile_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Ana Souza"


def test_rejects_invalid_profile():
    response = client.post("/api/profiles", json={"name": "", "email": "nao-e-email"})
    assert response.status_code == 400
    errors = response.json()["errors"]
    assert "name" in errors
    assert "email" in errors


def test_returns_404_for_unknown_profile():
    response = client.get("/api/profiles/999999")
    assert response.status_code == 404


def test_creates_technology_and_lists_it():
    client.post("/api/technologies", json={"name": "Kotlin"})

    response = client.get("/api/technologies")
    assert response.status_code == 200
    names = [t["name"] for t in response.json()]
    assert "Kotlin" in names


def test_creates_project_linked_to_profile_and_technology():
    profile_resp = client.post(
        "/api/profiles", json={"name": "Bruno Lima", "email": "bruno@example.com"}
    )
    profile_id = profile_resp.json()["id"]

    tech_resp = client.post("/api/technologies", json={"name": "FastAPI"})
    tech_id = tech_resp.json()["id"]

    response = client.post(
        "/api/projects",
        json={
            "title": "Portfólio",
            "description": "Meu site",
            "repositoryUrl": "https://github.com/bruno/portfolio",
            "profileId": profile_id,
            "technologyIds": [tech_id],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["profileId"] == profile_id
    assert body["technologies"][0]["name"] == "FastAPI"

    list_response = client.get("/api/projects")
    assert list_response.status_code == 200
    titles = [p["title"] for p in list_response.json()]
    assert "Portfólio" in titles


def test_rejects_project_with_blank_title_and_invalid_url():
    response = client.post(
        "/api/projects",
        json={"title": "  ", "repositoryUrl": "isso-nao-e-url", "profileId": 1},
    )
    assert response.status_code == 400
    errors = response.json()["errors"]
    assert "title" in errors
    assert "repositoryUrl" in errors
