#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERRO] Python 3 não foi encontrado. Instale em https://www.python.org/downloads/"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Criando ambiente virtual em .venv ..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "Instalando dependências (na primeira vez pode demorar alguns minutos)..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

echo ""
echo "API disponível em:   http://localhost:8000"
echo "Documentação/testes: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --port 8000
