# app/schemas/reports.py
from pydantic import BaseModel, ConfigDict  # <-- 1. IMPORTA ConfigDict
from datetime import datetime
from typing import Optional


class ReporteCrear(BaseModel):
    titulo: Optional[str]
    descripcion: str
    latitud: Optional[float]
    longitud: Optional[float]


class ReporteRespuesta(BaseModel):
    id: int
    titulo: Optional[str]
    descripcion: str
    imagen_url: Optional[str]
    latitud: Optional[float]
    longitud: Optional[float]
    estado: str
    usuario_id: int
    creado_en: datetime

    # --- ¡CORREGIDO! ---
    # Esta es la nueva sintaxis
    model_config = ConfigDict(from_attributes=True)


class ComentarioCrear(BaseModel):
    contenido: str


class ComentarioRespuesta(BaseModel):
    id: int
    contenido: str
    usuario_id: int
    reporte_id: int
    creado_en: datetime

    # --- ¡CORREGIDO! ---
    # Esta es la nueva sintaxis
    model_config = ConfigDict(from_attributes=True)