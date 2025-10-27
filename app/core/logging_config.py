from app.core.config import get_settings
import logging

def setup_logging():
    settings = get_settings()
    logging.basicConfig(level=settings.LOG_LEVEL.upper())
