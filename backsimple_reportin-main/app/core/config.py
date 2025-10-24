# app/core/config.py
from pydantic_settings import BaseSettings

class Configuracion(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"

# Instancia global
config = Configuracion()
