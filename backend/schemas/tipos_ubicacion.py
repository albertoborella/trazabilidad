from sqlmodel import SQLModel


class TipoUbicacionCreate(SQLModel):
    codigo: str
    descripcion: str


class TipoUbicacionRead(TipoUbicacionCreate):
    id: int
