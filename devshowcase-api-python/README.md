# DevShowcase API (Python / FastAPI)

Backend da plataforma **DevShowcase** — vitrine de portfólios de desenvolvedores.
Etapa 1: fundação arquitetural com persistência relacional.

**Stack:** Python 3.10+ · FastAPI · SQLAlchemy (ORM) · Pydantic (validação) · SQLite · pytest

## Como executar

**Windows (mais fácil):** dê dois cliques em `iniciar-api.bat`. Ele cria o ambiente virtual, instala tudo e liga a API.

**Mac/Linux:** no terminal, rode `./iniciar-api.sh`.

**Manual (qualquer sistema):**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

A API sobe em **http://localhost:8000**. O banco (`devshowcase.db`, SQLite) é criado automaticamente na primeira execução, na mesma pasta.

### Testando sem o Postman

O FastAPI já vem com uma página para testar os endpoints direto no navegador:
**http://localhost:8000/docs**

### Rodando os testes automáticos

```bash
pytest
```

## Modelo de dados

```
Profile 1 ──── N Project N ──── N Technology
                   │
                   1
                   │
                   N
               Feedback
```

## Estrutura

```
app/
├── database.py   # conexão com o SQLite
├── models.py     # entidades SQLAlchemy (Profile, Project, Feedback, Technology)
├── schemas.py    # DTOs de entrada (com validação) e de saída (Pydantic)
├── routers/      # endpoints REST, um arquivo por recurso
└── main.py       # cria a aplicação, registra rotas e trata erros de validação
tests/
└── test_api.py   # testes de integração com pytest
```

## Endpoints

| Método | Rota                  | Descrição                    | Sucesso |
|--------|-----------------------|------------------------------|---------|
| POST   | `/api/profiles`       | Cadastra perfil              | 201     |
| GET    | `/api/profiles/{id}`  | Busca perfil por id          | 200     |
| POST   | `/api/technologies`   | Cadastra tecnologia          | 201     |
| GET    | `/api/technologies`   | Lista todas as tecnologias   | 200     |
| POST   | `/api/projects`       | Cadastra projeto             | 201     |
| GET    | `/api/projects`       | Lista projetos               | 200     |

Erros: `400` (validação), `404` (perfil ou tecnologia inexistente), `409` (e-mail ou tecnologia duplicados).

### Exemplos de corpo (JSON)

**POST /api/profiles**
```json
{
  "name": "Ana Souza",
  "email": "ana@example.com",
  "bio": "Desenvolvedora backend",
  "githubUrl": "https://github.com/anasouza",
  "linkedinUrl": "https://www.linkedin.com/in/anasouza"
}
```

**POST /api/technologies**
```json
{ "name": "FastAPI" }
```

**POST /api/projects**
```json
{
  "title": "Meu Portfólio",
  "description": "Site pessoal com meus projetos",
  "repositoryUrl": "https://github.com/anasouza/portfolio",
  "demoUrl": "https://anasouza.dev",
  "profileId": 1,
  "technologyIds": [1]
}
```

**Exemplo de erro de validação (400)**
```json
{
  "status": 400,
  "message": "Erro de validação",
  "errors": { "title": "O título é obrigatório" },
  "timestamp": "2026-09-24T10:00:00+00:00"
}
```

## Roteiro sugerido para o vídeo (5 a 8 min)

1. Apresentação de cada integrante na webcam (nome completo).
2. Tela inteira: mostrar rapidamente a estrutura do projeto e o repositório no GitHub.
3. Subir a API (dois cliques em `iniciar-api.bat`, ou `uvicorn app.main:app --reload`).
4. No Postman (ou em `http://localhost:8000/docs`), nesta ordem: `POST /api/profiles` → `GET /api/profiles/1` → `POST /api/technologies` → `GET /api/technologies` → `POST /api/projects` → `GET /api/projects`.
5. Mostrar também casos de erro: perfil com e-mail inválido, projeto com título vazio e URL inválida (400), `GET /api/profiles/999` (404).
