import uvicorn

from app.config import settings

uvicorn.run("app.main:app", host=settings.backend_host, port=settings.backend_port)
