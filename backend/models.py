from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import List
from datetime import datetime, date


class TipoEvento(str, Enum):
    PRODUCCION = "produccion"
    INGRESO = "ingreso"
    EGRESO = "egreso"
    EXPORTACION = "exportacion"


class TipoUbicacion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: str = Field(unique=True, index=True)
    nombre:str
    descripcion: str | None = None
    ubicaciones: list["Ubicacion"] = Relationship(back_populates="tipo")


class Ubicacion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: str = Field(unique=True, index=True)
    nombre: str
    tipo_id: int = Field(foreign_key="tipoubicacion.id")
    pais: str
    provincia: str | None = None
    ciudad: str | None = None
    tipo: TipoUbicacion | None = Relationship(back_populates="ubicaciones")
    eventos: list["EventoTrazabilidad"] = Relationship(back_populates="ubicacion")


class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo_producto: str = Field(unique=True, index=True)
    nombre: str
    lotes: list["LoteProduccion"] = Relationship(back_populates="producto")


class LoteProduccion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id", index=True)
    lote: str = Field(index=True)
    fecha_produccion: date
    producto: Producto | None = Relationship(back_populates="lotes")
    eventos: list["EventoTrazabilidad"] = Relationship(back_populates="lote")


class EventoTrazabilidad(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    lote_id: int = Field(foreign_key="loteproduccion.id", index=True)
    ubicacion_id: int = Field(foreign_key="ubicacion.id", index=True)
    tipo_evento: TipoEvento = Field(index=True)
    fecha_hora: datetime = Field(index=True)
    # Transporte (INGRESO / EGRESO)
    patente_1: str | None = Field(default=None, index=True)
    patente_2: str | None = Field(default=None, index=True)
    # Exportación
    documento_exportacion: str | None = Field(default=None, index=True)
    observaciones: str | None = None
    lote: LoteProduccion | None = Relationship(back_populates="eventos")
    ubicacion: Ubicacion | None = Relationship(back_populates="eventos")



