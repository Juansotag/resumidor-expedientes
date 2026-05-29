import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.analyze import router as analyze_router

# Raíz del proyecto (un nivel arriba de este archivo: backend/main.py → raíz/)
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="resume-expedientes — GovLab",
    description="Generador de resúmenes ejecutivos institucionales para la Universidad de La Sabana",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(analyze_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


# Servir assets de marca (logos, fuentes, styles.css) desde /assets
# La carpeta assets/ está en la raíz del proyecto, fuera de frontend/
app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="assets")

# Servir el frontend como archivos estáticos — debe ir último
app.mount("/", StaticFiles(directory=str(BASE_DIR / "frontend"), html=True), name="frontend")
