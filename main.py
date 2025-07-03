from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from auth import crear_token
from passlib.context import CryptContext
from security import get_current_user
from models import Usuario

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependency para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register", response_model=schemas.UsuarioOut)
def register(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Usuario).filter_by(email=usuario.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    hashed_password = pwd_context.hash(usuario.password)
    nuevo = models.Usuario(email=usuario.email, password=hashed_password)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@app.post("/login")
def login(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter_by(email=usuario.email).first()
    if not user or not pwd_context.verify(usuario.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud.get_productos(db)

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    producto = crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud.crear_producto(db, producto)

@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
def borrar_producto(producto_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    producto = crud.borrar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto