# app/core/seguridad.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

# Cargar variables del entorno (.env)
load_dotenv()

# Variables desde el archivo .env
CLAVE_SECRETA = os.getenv("SECRET_KEY", "clave_por_defecto")
ALGORITMO = os.getenv("ALGORITHM", "HS256")
TIEMPO_EXPIRACION_MINUTOS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Contexto de encriptación
contexto_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =====================================================
# 🔐 FUNCIONES DE SEGURIDAD
# =====================================================

def encriptar_contraseña(contrasena: str) -> str:
    """Devuelve la contraseña encriptada (máx. 72 caracteres para evitar error de bcrypt)."""
    if len(contrasena) > 72:
        contrasena = contrasena[:72]
    return contexto_pwd.hash(contrasena)


def verificar_contraseña(contrasena_plana: str, contrasena_encriptada: str) -> bool:
    """Compara una contraseña escrita con su versión encriptada."""
    try:
        return contexto_pwd.verify(contrasena_plana, contrasena_encriptada)
    except ValueError:
        # En caso de error de verificación o contraseña corrupta
        return False


def crear_token_acceso(datos: dict, expiracion: timedelta = None) -> str:
    """Genera un token JWT que expira después de cierto tiempo."""
    datos_a_codificar = datos.copy()
    expiracion_token = datetime.utcnow() + (expiracion or timedelta(minutes=TIEMPO_EXPIRACION_MINUTOS))
    datos_a_codificar.update({"exp": expiracion_token})
    token = jwt.encode(datos_a_codificar, CLAVE_SECRETA, algorithm=ALGORITMO)
    return token


def decodificar_token(token: str):
    """Decodifica y valida el token JWT. Si es válido, devuelve los datos; si no, devuelve None."""
    try:
        carga = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        return carga
    except JWTError:
        return None
