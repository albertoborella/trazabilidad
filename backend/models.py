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
    fecha_produccion: date
    lote_produccion: str
    eventos: list["EventoTrazabilidad"] = Relationship(back_populates="producto")


class EventoTrazabilidad(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id", index=True)
    ubicacion_id: int = Field(foreign_key="ubicacion.id", index=True)
    tipo_evento: TipoEvento = Field(index=True)
    fecha_hora: datetime = Field(index=True)
    observaciones: str | None = None
    producto: Producto | None = Relationship(back_populates="eventos")
    ubicacion: Ubicacion | None = Relationship(back_populates="eventos")


