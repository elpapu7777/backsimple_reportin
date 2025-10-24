# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.database import get_db
from app.models.usuarios import Usuario
# --- ¡CORREGIDO! ---
from app.schemas.usuarios import UsuarioCrear, UsuarioRespuesta, Token
from app.core.seguridad import (
    encriptar_contraseña,
    verificar_contraseña,
    crear_token_acceso,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/registrar", response_model=UsuarioRespuesta) # <-- CORREGIDO
def registrar_usuario(datos_usuario: UsuarioCrear, db: Session = Depends(get_db)): # <-- CORREGIDO
    """Registrar un nuevo usuario en el sistema."""
    
    # --- ¡CORREGIDO! ---
    existente = db.query(Usuario).filter(Usuario.correo == datos_usuario.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # --- ¡CORREGIDO! ---
    usuario = Usuario(
        nombre=datos_usuario.nombre,
        correo=datos_usuario.correo,
        contrasena_hash=encriptar_contraseña(datos_usuario.contrasena),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def iniciar_sesion(datos_usuario: UsuarioCrear, db: Session = Depends(get_db)): # <-- CORREGIDO
    """Verifica las credenciales y devuelve un token de acceso."""

    # --- ¡CORREGIDO! ---
    usuario = db.query(Usuario).filter(Usuario.correo == datos_usuario.correo).first()

    # --- ¡CORREGIDO! ---
    if not usuario or not verificar_contraseña(datos_usuario.contrasena, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    # --- ¡CORREGIDO! ---
    token = crear_token_acceso(
        {"user_id": usuario.id, "role": usuario.rol},
        expiracion=timedelta(minutes=1440),
    )
    return {"access_token": token, "token_type": "bearer"}