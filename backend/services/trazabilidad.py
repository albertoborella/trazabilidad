from datetime import timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select

from models import (
    EventoTrazabilidad,
    LoteProduccion,
    Ubicacion,
    TipoEvento,
)


# ============================
# STOCK DISPONIBLE POR LOTE
# ============================
def stock_disponible(session: Session, lote_id: int) -> float:
    eventos = session.exec(
        select(EventoTrazabilidad)
        .where(EventoTrazabilidad.lote_id == lote_id)
        .order_by(EventoTrazabilidad.fecha_hora)
    ).all()

    stock = 0.0

    for e in eventos:
        if e.tipo_evento == TipoEvento.PRODUCCION:
            stock += e.cantidad
        elif e.tipo_evento in (TipoEvento.EGRESO, TipoEvento.EXPORTACION):
            stock -= e.cantidad
        # INGRESO no modifica stock del lote

    return stock


# ============================
# VALIDACIÓN DE EVENTO
# ============================
def validar_evento(session: Session, evento):
    # ============================
    # Validar que exista el lote
    # ============================
    lote = session.get(LoteProduccion, evento.lote_id)
    if not lote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lote no encontrado",
        )

    # ============================
    # Validar que exista la ubicación
    # ============================
    ubicacion = session.get(Ubicacion, evento.ubicacion_id)
    if not ubicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ubicación no encontrada",
        )

    # ============================
    # Validar fecha >= producción
    # ============================
    if evento.fecha_hora.date() < lote.fecha_produccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha del evento no puede ser anterior a la fecha de producción del lote",
        )

    # ============================
    # Validar cantidad
    # ============================
    if evento.cantidad is None or evento.cantidad <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cantidad es obligatoria y debe ser mayor a cero",
        )

    # ============================
    # Validar stock disponible
    # ============================
    if evento.tipo_evento in (TipoEvento.EGRESO, TipoEvento.EXPORTACION):
        disponible = stock_disponible(session, evento.lote_id)
        if evento.cantidad > disponible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente. Disponible: {disponible} kg",
            )

    # ============================
    # Validaciones por tipo de evento
    # ============================
    if evento.tipo_evento in (TipoEvento.INGRESO, TipoEvento.EGRESO):
        if not evento.patente_1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los eventos de ingreso o egreso requieren al menos una patente",
            )

    if evento.tipo_evento == TipoEvento.EXPORTACION:
        if not evento.documento_exportacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El evento de exportación requiere un documento de exportación",
            )

    if evento.tipo_evento == TipoEvento.PRODUCCION:
        if evento.patente_1 or evento.patente_2 or evento.documento_exportacion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El evento de producción no debe tener patentes ni documentos",
            )

    # ============================
    # Evitar duplicados técnicos
    # ============================
    ventana = timedelta(seconds=5)

    evento_similar = session.exec(
        select(EventoTrazabilidad).where(
            EventoTrazabilidad.lote_id == evento.lote_id,
            EventoTrazabilidad.ubicacion_id == evento.ubicacion_id,
            EventoTrazabilidad.tipo_evento == evento.tipo_evento,
            EventoTrazabilidad.fecha_hora >= evento.fecha_hora - ventana,
            EventoTrazabilidad.fecha_hora <= evento.fecha_hora + ventana,
        )
    ).first()

    if evento_similar:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Evento duplicado detectado (posible doble registro)",
        )

    # ============================
    # Validar secuencia de eventos
    # ============================
    ultimo_evento = session.exec(
        select(EventoTrazabilidad)
        .where(EventoTrazabilidad.lote_id == evento.lote_id)
        .order_by(EventoTrazabilidad.fecha_hora.desc())
    ).first()

    # Primer evento
    if not ultimo_evento:
        if evento.tipo_evento != TipoEvento.PRODUCCION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El primer evento del lote debe ser PRODUCCION",
            )
        return

    # No permitir mismo tipo consecutivo
    if ultimo_evento.tipo_evento == evento.tipo_evento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede registrar dos eventos consecutivos de tipo {evento.tipo_evento}",
        )

    # Exportación solo luego de egreso
    if (
        evento.tipo_evento == TipoEvento.EXPORTACION
        and ultimo_evento.tipo_evento != TipoEvento.EGRESO
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La exportación solo puede registrarse después de un egreso",
        )



    

        