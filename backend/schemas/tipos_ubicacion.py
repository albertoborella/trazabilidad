from sqlmodel import SQLModel


class TipoUbicacionCreate(SQLModel):
    codigo: str
    nombre: str
    descripcion: str


class TipoUbicacionRead(TipoUbicacionCreate):
    id: int
