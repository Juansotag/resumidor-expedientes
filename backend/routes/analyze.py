import os
import asyncio
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from backend.services import document_processor, claude_service, html_generator

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
MAX_FILE_SIZE_MB = int(os.environ.get("MAX_FILE_SIZE_MB", "20"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@router.post("/analyze")
async def analyze(file: UploadFile = File(...), api_key: str = Form(None), use_search: str = Form("false")):
    """
    Recibe un documento, lo procesa y devuelve un resumen ejecutivo en HTML.
    """
    # Validar extensión
    filename = file.filename or ""
    ext = "." + filename.lower().split(".")[-1] if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"Formato no soportado. Usa solo PDF o Word. Recibido: '{ext}'",
            },
        )

    # Leer contenido
    file_bytes = await file.read()

    # Validar tamaño
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"El archivo es muy grande. Máximo {MAX_FILE_SIZE_MB}MB.",
            },
        )

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "El archivo está vacío."},
        )

    # Pipeline de procesamiento
    try:
        # 1. Extraer texto e imágenes (síncrono, corre en thread)
        extracted = await asyncio.to_thread(
            document_processor.extract, file_bytes, filename
        )
        text = extracted.get("text", "")
        images = extracted.get("images", [])

        if not text and not images:
            raise HTTPException(
                status_code=422,
                detail={
                    "status": "error",
                    "message": "No se pudo extraer contenido del documento.",
                },
            )

        # 2. Llamar a Claude (síncrono, corre en thread para no bloquear el event loop)
        do_search = use_search.lower() == "true"
        raw_html, sources = await asyncio.to_thread(
            claude_service.analyze, text, images, api_key, do_search
        )

        if not raw_html:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "message": "Claude no devolvió un resultado válido.",
                },
            )

        # 3. Envolver con estilos GovLab
        final_html = html_generator.wrap(raw_html)

        return JSONResponse(
            content={
                "status": "ok",
                "html": final_html,
                "tokens_used": 0,
                "sources": sources,
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Ocurrió un error al procesar el expediente: {str(e)}",
            },
        )
