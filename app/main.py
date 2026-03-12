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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://www.tucaserito.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1/auth", tags=["Auth"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Tu Caserito Auth Service"}
