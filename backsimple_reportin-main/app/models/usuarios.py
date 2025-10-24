# app/models/users.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    contrasena_hash = Column(String, nullable=False)
    rol = Column(String, default="usuario")  # 'usuario' o 'admin'
    avatar_url = Column(String, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
