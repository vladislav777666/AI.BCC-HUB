from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.uploads import router as uploads_router
from app.api.recommendations import router as rec_router
from app.api.push import router as push_router
from app.db.models import Base
from app.utils.logging import setup_logging
from app.utils.metrics import setup_metrics
from celery import Celery
import os

app = FastAPI(title="Bank API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/bank")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

celery = Celery(__name__, broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"))

app.include_router(uploads_router, prefix="/api/upload")
app.include_router(rec_router, prefix="/api/recommendations")
app.include_router(push_router, prefix="/api/push")

setup_logging()
setup_metrics(app)

@app.get("/health")
def health():
    return {"status": "ok"}