from sqlmodel import SQLModel


class UbicacionCreate(SQLModel):
    codigo: str
    nombre: str
    tipo_id: int
    pais: str
    provincia: str | None = None
    ciudad: str | None = None


class UbicacionRead(UbicacionCreate):
    id: int
