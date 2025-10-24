# app/routers/reportes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database.database import get_db
# --- ¡CORREGIDO! ---
from app.models.reportes import Reporte # No 'Report'
from app.schemas.reportes import ReporteCrear, ReporteRespuesta # No 'ReportCreate', 'ReportOut'
from app.routes.usuarios import obtener_usuario_actual
from app.core.config import config
import os

router = APIRouter(prefix="/reportes", tags=["Reportes"])
os.makedirs(config.UPLOAD_DIR, exist_ok=True)


@router.get("/", response_model=list[ReporteRespuesta]) # <-- CORREGIDO
def listar_reportes(db: Session = Depends(get_db)):
    """Lista todos los reportes existentes."""
    # --- ¡CORREGIDO! ---
    return db.query(Reporte).order_by(Reporte.creado_en.desc()).all()


@router.post("/", response_model=ReporteRespuesta) # <-- CORREGIDO
def crear_reporte(
    reporte_in: ReporteCrear, # <-- CORREGIDO
    imagen: UploadFile | None = None,
    db: Session = Depends(get_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    """Crea un nuevo reporte con descripción e imagen opcional."""
    imagen_url = None
    if imagen:
        # ... (lógica de archivos) ...
        pass

    # --- ¡CORREGIDO! ---
    nuevo_reporte = Reporte(
        titulo=reporte_in.titulo,
        descripcion=reporte_in.descripcion,
        imagen_url=imagen_url,
        latitud=reporte_in.latitud,
        longitud=reporte_in.longitud,
        usuario_id=usuario_actual.id,
    )
    db.add(nuevo_reporte)
    db.commit()
    db.refresh(nuevo_reporte)
    return nuevo_reporte


@router.get("/{reporte_id}", response_model=ReporteRespuesta) # <-- CORREGIDO
def ver_reporte(reporte_id: int, db: Session = Depends(get_db)):
    """Devuelve los detalles de un reporte específico."""
    # --- ¡CORREGIDO! ---
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return reporte


@router.put("/{reporte_id}", response_model=ReporteRespuesta) # <-- CORREGIDO
def editar_reporte(
    reporte_id: int,
    reporte_in: ReporteCrear, # <-- CORREGIDO
    db: Session = Depends(get_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    """Permite modificar un reporte existente."""
    # --- ¡CORREGIDO! ---
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # --- ¡CORREGIDO! --- (usa .rol, no .role)
    if reporte.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este reporte")

    for clave, valor in reporte_in.dict(exclude_unset=True).items():
        setattr(reporte, clave, valor)
    db.commit()
    db.refresh(reporte)
    return reporte


@router.delete("/{reporte_id}")
def eliminar_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    """Elimina un reporte (solo el autor o el admin puede hacerlo)."""
    # --- ¡CORREGIDO! ---
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # --- ¡CORREGIDO! --- (usa .rol, no .role)
    if reporte.usuario_id != usuario_actual.id and usuario_actual.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este reporte")

    db.delete(reporte)
    db.commit()
    return {"mensaje": "Reporte eliminado correctamente"}