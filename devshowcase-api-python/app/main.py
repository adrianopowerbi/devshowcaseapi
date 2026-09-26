"""Ponto de entrada da aplicação DevShowcase API."""
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import Base, engine
from .routers import profiles, projects, technologies

app = FastAPI(
    title="DevShowcase API",
    description="Backend da plataforma DevShowcase - vitrine de portfólios de desenvolvedores.",
    version="0.1.0",
)

# Cria as tabelas no banco (se ainda não existirem)
Base.metadata.create_all(bind=engine)

app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Converte os erros de validação do Pydantic em um formato mais simples de ler."""
    errors: dict[str, str] = {}
    for err in exc.errors():
        loc = [str(part) for part in err.get("loc", []) if part != "body"]
        field = loc[-1] if loc else "body"
        if field not in errors:
            errors[field] = err.get("msg", "Valor inválido")

    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "message": "Erro de validação",
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "devshowcase-api"}
