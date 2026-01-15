from datetime import date
from sqlmodel import SQLModel

class LoteCreate(SQLModel):
    producto_id: int
    lote: str
    fecha_produccion: date

class LoteRead(LoteCreate):
    id: int