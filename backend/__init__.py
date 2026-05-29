# backend/__init__.py
# Carga variables de entorno del .env al iniciar el backend
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # en producción (Railway) las variables se inyectan directamente
