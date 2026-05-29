# resume-expedientes — GovLab · Universidad de La Sabana

Aplicación web que convierte expedientes institucionales (PDF, Word, imagen) en resúmenes ejecutivos de dos páginas, optimizados para lectura desde celular, con análisis de riesgos y referencias externas.

---

## Cómo construir con Antigravity

1. Descomprime este `.zip`
2. Abre la carpeta en Antigravity
3. Pega este mensaje en el chat:

```
Por favor desarrolla esta aplicación siguiendo exactamente el APP_SPEC.md incluido en esta carpeta.

Stack: HTML/CSS/JS vanilla (frontend) + Python FastAPI (backend). Sin React, sin frameworks de frontend.

Orden de construcción:
1. backend/main.py
2. backend/services/document_processor.py
3. backend/services/claude_service.py
4. backend/services/html_generator.py
5. backend/routes/analyze.py
6. frontend/index.html
7. frontend/css/app.css
8. frontend/js/app.js
9. frontend/js/share.js
10. frontend/js/pdf-export.js

Los assets de marca ya están en assets/ — NO los regeneres.
El system prompt de Claude está en el APP_SPEC.md sección 6 — cópialo exactamente.
No cambies la paleta de colores ni las fuentes.
```

---

## Variables de entorno

Copia `.env.example` como `.env` y completa:

- `ANTHROPIC_API_KEY` — obligatoria, obtener en console.anthropic.com

---

## Deploy en Railway

1. Conectar repositorio GitHub a Railway
2. Configurar variables de entorno en el dashboard de Railway
3. Railway detectará automáticamente Python y usará el `Procfile`
4. Dominio: configurar CNAME en Cloudflare apuntando a `*.up.railway.app`

---

## Prueba local

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
# Abrir http://localhost:8000
```

---

Laboratorio de Gobierno · Universidad de La Sabana
