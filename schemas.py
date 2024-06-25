from pydantic import BaseModel

class LibroBase(BaseModel):
    autor: str
    titulo: str
    estado: int

class LibroCreate(LibroBase):
    pass

class Libro(LibroBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nombre: str
    documento: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class LibroUsuarioBase(BaseModel):
    usuario_id: int
    libro_id: int
    tiempo_prestamo: int

class LibroUsuarioCreate(LibroUsuarioBase):
    pass

class LibroUsuario(LibroUsuarioBase):
    id: int

    class Config:
        from_attributes = True
