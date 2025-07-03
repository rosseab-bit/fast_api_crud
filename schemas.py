from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    precio: int
    stock: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True


class UsuarioCreate(BaseModel):
    email: str
    password: str

class UsuarioOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True