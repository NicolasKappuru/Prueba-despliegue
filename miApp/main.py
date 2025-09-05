from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# -------------------------
# Configuración de BD
# -------------------------
DATABASE_URL = "postgresql://postgres:frPVlEnQwyfiDsmvnVpmcjFhFeKbZgZl@hopper.proxy.rlwy.net:40246/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla
class Texto(Base):
    __tablename__ = "textos"
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(String, index=True)

# Crear tabla si no existe
Base.metadata.create_all(bind=engine)

# -------------------------
# App FastAPI
# -------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# -------------------------
# Dependencia DB
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Rutas
# -------------------------

# Página principal con formulario
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Guardar texto en la BD
@app.post("/guardar")
def guardar_texto(request: Request, texto: str = Form(...), db: Session = Depends(get_db)):
    nuevo = Texto(valor=texto)
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# Mostrar todos los datos
@app.get("/ver")
def ver_datos(request: Request, db: Session = Depends(get_db)):
    datos = db.query(Texto).all()
    return templates.TemplateResponse("view.html", {"request": request, "datos": datos})
