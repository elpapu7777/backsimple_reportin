# app/schemas/users.py
from pydantic import BaseModel, EmailStr, ConfigDict  # <-- 1. IMPORTA ConfigDict
from datetime import datetime
from typing import Optional


class UsuarioCrear(BaseModel):
    nombre: str
    correo: EmailStr
    contrasena: str


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: str
    avatar_url: Optional[str]
    creado_en: datetime

    # --- ¡CORREGIDO! ---
    # Esta es la nueva sintaxis
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str