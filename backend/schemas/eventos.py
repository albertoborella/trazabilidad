from datetime import datetime
from sqlmodel import SQLModel
from models import TipoEvento

class EventoCreate(SQLModel):
    lote_id: int
    ubicacion_id: int
    tipo_evento: TipoEvento
    fecha_hora: datetime

    patente_1: str | None = None
    patente_2: str | None = None
    documento_exportacion: str | None = None

    observaciones: str | None = None


class EventoRead(EventoCreate):
    id: int
