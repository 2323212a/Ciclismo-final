from pydantic import BaseModel


class Usuario(BaseModel):
    nombre: str
    email: str
    password: str

    categoria_id: int
    evento_id: int

    rol: str = "usuario"