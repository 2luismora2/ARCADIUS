from sqlalchemy import Column, Integer, String
from database import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    autor = Column(String(100))
    titulo = Column(String(255))
    estado = Column(Integer)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    documento = Column(String(12))

class LibroUsuario(Base):
    __tablename__ = "libros_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer)
    libro_id = Column(Integer)
    tiempo_prestamo = Column(Integer)
