# Backend — AWS Route 53 Clone

FastAPI + SQLAlchemy + SQLite backend for the Route 53 clone assignment.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

## Structure

- `app/main.py` — application startup, CORS, health endpoint, router registration
- `app/database.py` — SQLite engine and sessions
- `app/models.py` — SQLAlchemy models
- `app/schemas.py` — Pydantic request/response models
- `app/routers/` — HTTP/API layer
- `app/services/` — business logic
- `app/utils/validation.py` — input normalization and validation
