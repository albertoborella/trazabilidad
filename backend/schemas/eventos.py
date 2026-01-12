from datetime import datetime
from sqlmodel import SQLModel
from models import TipoEvento

class EventoCreate(SQLModel):
    producto_id: int
    ubicacion_id: int
    tipo_evento: TipoEvento
    fecha_hora: datetime
    observaciones:str | None = None


class EventoRead(EventoCreate):
    id: int
