# app/routers/comentarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
# --- ¡CORREGIDO! ---
from app.models.reportes import Comentario, Reporte # No 'Comment', 'Report'
from app.schemas.reportes import ComentarioCrear, ComentarioRespuesta # No 'CommentCreate', 'CommentOut'
from app.routes.usuarios import obtener_usuario_actual

router = APIRouter(prefix="/reportes/{reporte_id}/comentarios", tags=["Comentarios"])


@router.get("/", response_model=list[ComentarioRespuesta]) # <-- CORREGIDO
def listar_comentarios(reporte_id: int, db: Session = Depends(get_db)):
    """Devuelve todos los comentarios de un reporte."""
    # --- ¡CORREGIDO! ---
    comentarios = (
        db.query(Comentario)
        .filter(Comentario.reporte_id == reporte_id)
        .order_by(Comentario.creado_en.asc())
        .all()
    )
    return comentarios


@router.post("/", response_model=ComentarioRespuesta) # <-- CORREGIDO
def agregar_comentario(
    reporte_id: int,
    comentario_in: ComentarioCrear, # <-- CORREGIDO
    db: Session = Depends(get_db),
    usuario_actual=Depends(obtener_usuario_actual),
):
    """Agrega un nuevo comentario a un reporte existente."""
    # --- ¡CORREGIDO! ---
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    # --- ¡CORREGIDO! ---
    comentario = Comentario(
        contenido=comentario_in.contenido,
        reporte_id=reporte_id,
        usuario_id=usuario_actual.id,
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario