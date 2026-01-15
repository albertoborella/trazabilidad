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

    patente_1: str | None = None
    patente_2: str | None = None
    documento_exportacion: str | None = None

    observaciones: str | None = None



class ProductoTimeline(SQLModel):
    codigo_producto: str
    nombre: str
    

class LoteTimeline(SQLModel):
    id: int
    lote: str
    fecha_produccion: date


class TrazabilidadResponse(SQLModel):
    producto: ProductoTimeline
    lote: LoteTimeline
    trazabilidad: list[EventoTimeline]

