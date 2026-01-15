from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database import get_session
from models import LoteProduccion, EventoTrazabilidad
from schemas.trazabilidad import (
    TrazabilidadResponse,
    ProductoTimeline,
    LoteTimeline,
    EventoTimeline,
    UbicacionTimeline,
)

router = APIRouter(prefix="/trazabilidad", tags=["Trazabilidad"])


@router.get("/lotes/{lote_id}", response_model=TrazabilidadResponse)
def obtener_trazabilidad_lote(
    lote_id: int,
    session: Session = Depends(get_session),
):
    lote = session.get(LoteProduccion, lote_id)
    if not lote:
        raise HTTPException(404, "Lote no encontrado")

    eventos = session.exec(
        select(EventoTrazabilidad)
        .where(EventoTrazabilidad.lote_id == lote_id)
        .order_by(EventoTrazabilidad.fecha_hora)
    ).all()

    timeline = [
        EventoTimeline(
            fecha_hora=e.fecha_hora,
            tipo_evento=e.tipo_evento,
            ubicacion=UbicacionTimeline(
                codigo=e.ubicacion.codigo,
                nombre=e.ubicacion.nombre,
            ),
            patente_1=e.patente_1,
            patente_2=e.patente_2,
            documento_exportacion=e.documento_exportacion,
            observaciones=e.observaciones,
        )
        for e in eventos
    ]

    return TrazabilidadResponse(
        producto=ProductoTimeline(
            codigo_producto=lote.producto.codigo_producto,
            nombre=lote.producto.nombre,
        ),
        lote=LoteTimeline(
            id=lote.id,
            lote=lote.lote,
            fecha_produccion=lote.fecha_produccion,
        ),
        trazabilidad=timeline,
    )
