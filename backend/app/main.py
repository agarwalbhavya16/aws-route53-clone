import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import SessionLocal, engine
from .models import Base
from .routers import auth, hosted_zones, records
from .services.seed import seed_demo_data

Base.metadata.create_all(engine)
with SessionLocal() as db:
    seed_demo_data(db)

app = FastAPI(title="Route 53 Clone API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", os.getenv("FRONTEND_URL", "")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["System"])
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(hosted_zones.router)
app.include_router(records.router)
