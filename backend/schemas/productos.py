from datetime import date
from sqlmodel import SQLModel

class ProductoCreate(SQLModel):
    codigo_producto: str
    nombre: str

class ProductoRead(ProductoCreate):
    id: int
