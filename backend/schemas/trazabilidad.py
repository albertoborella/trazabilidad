from datetime import datetime, date
from sqlmodel import SQLModel
from models import TipoEvento


class UbicacionTimeline(SQLModel):
    codigo: str
    nombre: str


class EventoTimeline(SQLModel):
    fecha_hora: datetime
    tipo_evento: TipoEvento
    ubicacion: UbicacionTimeline
    observaciones: str | None = None


class ProductoTimeline(SQLModel):
    id: int
    codigo_producto: str
    nombre: str
    fecha_produccion: date
    lote_produccion: str


class TrazabilidadResponse(SQLModel):
    producto: ProductoTimeline
    trazabilidad: list[EventoTimeline]
