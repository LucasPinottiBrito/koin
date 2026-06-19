from fastapi import FastAPI

from src.config.settings import get_settings
from src.controllers.health import router as health_router
from src.logging.config import configure_logging

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)
app.include_router(health_router)
