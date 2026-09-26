# 🚀 DevShowcase API (Python / FastAPI)

O **DevShowcase API** é o backend da plataforma DevShowcase, funcionando como uma vitrine de portfólios para desenvolvedores. O projeto foi construído seguindo uma fundação arquitetural sólida com persistência relacional.

---

## 🛠️ Stack Utilizada

* **Linguagem:** Python 3.10+
* **Framework:** FastAPI
* **Banco de Dados:** SQLite
* **ORM:** SQLAlchemy
* **Validação de Dados:** Pydantic
* **Testes:** pytest

---

## ⚙️ Como Executar o Projeto

### 💻 No Windows (Forma Mais Fácil)
Basta navegar até a pasta raiz do projeto e dar **dois cliques no arquivo**:
`iniciar-api.bat`
> *Esse script criará o ambiente virtual automaticamente, instalará as dependências do `requirements.txt` e iniciará o servidor.*

### 🐧 No Mac / Linux
Abra o terminal na pasta raiz do projeto e execute:
```bash
chmod +x iniciar-api.sh
./iniciar-api.sh
```

### 🛠️ Inicialização Manual (Qualquer Sistema)
Se preferir rodar manualmente no terminal, execute a sequência abaixo:

1. **Criar o ambiente virtual:**
   ```bash
   python -m venv .venv
   ```
2. **Ativar o ambiente virtual:**
   * *Windows:* `.venv\Scripts\activate`
   * *Mac/Linux:* `source .venv/bin/activate`
3. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Iniciar o servidor:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

## 🔗 Endpoints Principais

A API roda localmente no endereço `http://localhost:8000`.

* `GET /` - Verifica o status da API.
* `GET /api/profiles/` - Lista os perfis de desenvolvedores cadastrados.

### 📝 Documentação Interativa
Com o servidor rodando, você pode acessar a documentação automática criada pelo FastAPI (Swagger UI) para testar os endpoints direto pelo navegador:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)
