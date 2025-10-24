2# app/routers/usuarios.py
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
# --- ¡CORREGIDO! ---
from app.models.usuarios import Usuario # No 'User'
from app.core.seguridad import decodificar_token

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def obtener_usuario_actual(token: str = Header(None), db: Session = Depends(get_db)):
    """Devuelve el usuario actual según el token JWT."""
    if not token:
        raise HTTPException(status_code=401, detail="Falta el token en la cabecera")

    datos = decodificar_token(token)
    if not datos:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    # --- ¡CORREGIDO! ---
    usuario = db.query(Usuario).filter(Usuario.id == datos.get("user_id")).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario


@router.get("/perfil")
def ver_perfil(usuario_actual=Depends(obtener_usuario_actual)):
    """Muestra la información del usuario logueado."""
    # --- ¡CORREGIDO! ---
    return {
        "id": usuario_actual.id,
        "nombre": usuario_actual.nombre,
        "email": usuario_actual.correo,
        "rol": usuario_actual.rol,
    }