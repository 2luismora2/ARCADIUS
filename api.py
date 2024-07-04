from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/libros/", response_model=schemas.Libro)
async def create_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = models.Libro(autor=libro.autor, titulo=libro.titulo, estado=libro.estado)
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro


@app.get("/libros/", response_model=List[schemas.Libro])
async def read_libros(db: Session = Depends(get_db)):
    return db.query(models.Libro).all()


@app.post("/usuarios/", response_model=schemas.Usuario)
async def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = models.Usuario(nombre=usuario.nombre, documento=usuario.documento)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@app.get("/usuarios/", response_model=List[schemas.Usuario])
async def read_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


@app.post("/libros_usuarios/", response_model=schemas.LibroUsuario)
async def create_libro_usuario(libro_usuario: schemas.LibroUsuarioCreate, db: Session = Depends(get_db)):
    db_libro_usuario = models.LibroUsuario(
        usuario_id=libro_usuario.usuario_id,
        libro_id=libro_usuario.usuario_id,
        tiempo_prestamo=libro_usuario.tiempo_prestamo
    )
    db.add(db_libro_usuario)
    db.commit()
    db.refresh(db_libro_usuario)
    return db_libro_usuario


@app.get("/libro/{libro_id}", response_model=schemas.Libro)
async def read_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    return db_libro


@app.get("/libros/search/", response_model=List[schemas.Libro])
async def search_libros(query: str, db: Session = Depends(get_db)):
    db_libro = db.query(models.Libro).filter(models.Libro.titulo.like(f"%{query}%")).first()
    return db_libro


@app.put("/libro/{libro_id}", response_model=schemas.Libro)
async def update_libro(libro_id: int, libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    db_libro.autor = libro.autor
    db_libro.titulo = libro.titulo
    db_libro.estado = libro.estado
    db.commit()
    db.refresh(db_libro)
    return db_libro


@app.delete("/libro/{libro_id}", response_model=dict)
async def delete_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    db.delete(db_libro)
    db.commit()
    return {"message": "Libro eliminado"}


