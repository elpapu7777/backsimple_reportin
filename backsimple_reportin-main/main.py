# main.py
from fastapi import FastAPI
from app.database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

# --- ¡ESTA ES LA PARTE MÁS IMPORTANTE! ---
# Importa tus MÓDULOS de modelos explícitamente aquí.
# Esto le "avisa" a SQLAlchemy que estas clases existen
# y las añade al registro de 'Base.metadata'.
from app.models import usuarios, reportes
# -----------------------------------------

# Importa todos tus routers
from app.routes import auth, reportes, comentarios, usuarios

app = FastAPI(title="Reportín API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ahora que los modelos están 100% importados, 
# esta línea SÍ sabrá qué tablas crear.
Base.metadata.create_all(bind=engine)

# Incluye todos tus routers para que los endpoints funcionen
app.include_router(auth.router)
app.include_router(reportes.router)
app.include_router(comentarios.router)
app.include_router(usuarios.router)


@app.get("/")
def root():
    return {"message": "Reportín API funcionando 🚀"}