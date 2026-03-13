import os
import json
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Tu Caserito — Auth Service",
    description="Servicio de autenticación con Google Sign-In para la plataforma Tu Caserito.",
    version="1.0.0",
)

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", '[ "https://www.tucaserito.com"]')
try:
    origins = json.loads(allowed_origins_env)
except Exception:
    origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin"],
)

app.include_router(router, prefix="/api/v1/auth", tags=["Auth"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Tu Caserito Auth Service"}
