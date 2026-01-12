from datetime import date
from sqlmodel import SQLModel

class ProductoCreate(SQLModel):
    codigo_producto: str
    descripcion: str
    fecha_produccion: date
    lote_produccion: str

class ProductoRead(ProductoCreate):
    id: int