import csv

from fastapi import FastAPI
from pydantic import BaseModel, constr, field_validator
from typing import List, Any

from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"hello": "world"}


libros = []
usuarios = []
libros_usuarios = []


class Usuario(BaseModel):
    nombre: str
    id: int
    documento: str

    def crear(self):
        if self.id is None:
            self.id = len(usuarios) + 1
            usuarios.append(self)
        return self

    def actualizar(self):
        for i in range(len(usuarios) - 1):
            if self.id == usuarios[i].id:
                usuarios[i].documento = self.documento
                usuarios[i].nombre = self.nombre
                return self

    @classmethod
    def tomar_libro(cls, libro_id, usuario_id, tiempo_prestamo):
        for usuario in usuarios:
            if usuario.id == usuario_id:
                for libro in libros:
                    if libro.id == libro_id:
                        libro_user = LibroUsuario(
                            tiempo_prestamo=tiempo_prestamo,
                            usuario_id=usuario_id,
                            libro_id=libro_id
                        )
                        libros_usuarios.append(libro_user)
                        libro.estado = 1
                        return libro_user

    @classmethod
    def entregar_libro(cls, libro_id, usuario_id):
        for usuario in usuarios:
            if usuario.id == usuario_id:
                for libro in libros:
                    if libro.id == libro_id:
                        for libro_usuario in libros_usuarios:
                            if libro_usuario.usuario_id == usuario_id and libro_usuario.libro_id == libro_id:
                                libros_usuarios.remove(libro_usuario)
                                libro.estado = 0
                                return True
        return False

    @classmethod
    def entregar_libro2(cls, libro_id, usuario_id):
        for libro_usuario in libros_usuarios:
            if libro_usuario.usuario_id == usuario_id and libro_usuario.libro_id == libro_id:
                libros_usuarios.remove(libro_usuario)
                for libro in libros:
                    if libro.id == libro_id:
                        libro.estado = 0
                return True
        return False




class Libro(BaseModel):
    titulo: constr(min_length=3, max_length=100)
    autor: str
    estado: int = 0
    id: int = None

    @field_validator("autor")
    def check_autor(cls, v: str):
        if len(v) < 3 or len(v) > 20:
            raise ValueError("El autor debe tener"
                             " minimo 3 caracters "
                             "y maximo 20 caracteres")
        return v

    def guardar(self):
        if self.id is None:
            self.id = len(libros) + 1
            libros.append(self)
        else:
            for libro in libros:
                if libro.id == self.id:
                    libro.autor = self.autor
                    libro.titulo = self.titulo
                    libro.estado = self.estado
        return self

    def editar(self):
        return self.guardar()

    @classmethod
    def eliminar(cls, libro_id):
        for libro in libros:
            if libro.id == libro_id:
                libros.remove(libro)
                return True
        return False

    @classmethod
    def eliminar2(cls, libro_id):
        for i in range(len(libros) - 1):
            if libros[i].id == libro_id:
                libros.pop(i)
                return True
        return False

    @classmethod
    def consultar(cls, libro_id):
        for libro in libros:
            if libro.id == libro_id:
                return libro
        return None

    @classmethod
    def consultar_todos(cls):
        return libros


class LibroUsuario():
    usuario_id: int
    libro_id: int
    tiempo_prestamo: int

    def _init_(self,
                 usuario_id: int,
                 libro_id: int,
                 tiempo_prestamo: int):
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.tiempo_prestamo = tiempo_prestamo


@app.post("/libro")
async def crear_libro(libro: Libro):
    return libro.guardar()


@app.put("/libro")
async def editar_libro(libro: Libro):
    return libro.editar()


@app.get("/libros")
async def consultar_libro():
    return Libro.consultar_todos()


@app.get("/libro/{libro_id}")
async def consultar_libro(libro_id: int):
    return Libro.consultar(libro_id)


@app.delete("/libro/{libro_id}")
async def eliminar_libro(libro_id: int):
    return Libro.eliminar(libro_id)

@app.get("/ejemplo")
async def redirect():
    return RedirectResponse(url="https://www.google.com/")

def cargar_libros_desde_csv(filename: str) -> List[Libro]:
    global  libros
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            libro = Libro(
                id=int(row['id']),
                titulo=row['titulo'],
                autor=row.get('autor', 'Desconocido'),  # Autor desconocido si no está en el CSV
                estado=int(row['estado'])
            )
            libros.append(libro)
    return libros

def cargar_usuarios_desde_csv(filename: str) -> List[Libro]:
    global  usuarios
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            usuario = Usuario(
                id=int(row['id']),
                nombre=row['nombre'],
                documento=row.get('documento', 'Desconocido'),  # Autor desconocido si no está en el CSV
            )
            usuarios.append(usuario)
    return usuarios



if __name__ == "_main_":
    import uvicorn

    cargar_libros_desde_csv("libros.csv")
    cargar_usuarios_desde_csv("usuarios.csv")
    uvicorn.run(app, host="127.0.0.1", port=8000)