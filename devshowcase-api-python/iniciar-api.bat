@echo off
setlocal
cd /d "%~dp0"
title DevShowcase API (Python)

echo ==========================================
echo   DevShowcase API - Python / FastAPI
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERRO] Python nao foi encontrado neste computador.
  echo Instale em https://www.python.org/downloads/
  echo IMPORTANTE: na instalacao, marque a caixinha "Add python.exe to PATH".
  echo.
  pause
  exit /b 1
)

if not exist ".venv" (
  echo Criando ambiente virtual em .venv ...
  python -m venv .venv
)

call ".venv\Scripts\activate.bat"

echo.
echo Instalando dependencias (na primeira vez pode demorar alguns minutos)...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo [ERRO] Falha ao instalar as dependencias. Confira sua conexao com a internet.
  pause
  exit /b 1
)

echo.
echo ==========================================
echo API disponivel em:   http://localhost:8000
echo Documentacao/testes: http://localhost:8000/docs
echo NAO FECHE ESTA JANELA enquanto estiver testando.
echo ==========================================
echo.

uvicorn app.main:app --reload --port 8000

echo.
echo A API foi encerrada (ou ocorreu um erro). Leia as mensagens acima.
pause
