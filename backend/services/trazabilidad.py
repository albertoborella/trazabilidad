from datetime import timedelta
from fastapi import HTTPException, status
from sqlmodel import Session, select
from models import EventoTrazabilidad, Producto, Ubicacion, TipoEvento


def validar_evento(session: Session, evento):
    # Validar que exista el producto
    producto = session.get(Producto, evento.producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Producto no encontrado'
        )
    # Validar que exista la ubicacion
    ubicacion = session.get(Ubicacion, evento.ubicacion_id)
    if not ubicacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Ubicación no encontrada'
                            )
    # Validar que na fecha no sea anterior a la producion
    if evento.fecha_hora < producto.fecha_produccion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='La fecha del evento no puede ser anterior a la fecha de producción del producto'
        )
# Validar no duplicar tecnicamente eventos iguales
    ventana = timedelta(seconds=5)
    evento_similar = session.exec(
        select(EventoTrazabilidad).where(
            EventoTrazabilidad.producto_id == evento.producto_id,
            EventoTrazabilidad.ubicacion_id == evento.ubicacion_id,
            EventoTrazabilidad.tipo_evento == evento.tipo_evento,
            EventoTrazabilidad.fecha_hora >= evento.fecha_hora - ventana,
            EventoTrazabilidad.fecha_hora <= evento.fecha_hora + ventana,
        )
    ).first()

    if evento_similar:
        raise HTTPException(
            status_code=409,
            detail="Evento duplicado detectado (posible doble registro)"
        )
# Validad secuencias de eventos
    ultimo_evento = session.exec(
        select(EventoTrazabilidad)
        .where(EventoTrazabilidad.producto_id == evento.producto_id)
        .order_by(EventoTrazabilidad.fecha_hora.desc())
    ).first()

    if not ultimo_evento:
        if evento.tipo_evento != TipoEvento.PRODUCCION:
            raise HTTPException(
                status_code=400,
                detail="El primer evento del producto debe ser PRODUCCION"
            )
        return

    if ultimo_evento.tipo_evento == evento.tipo_evento:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede registrar dos eventos consecutivos de tipo {evento.tipo_evento}"
        )

    if evento.tipo_evento == TipoEvento.EXPORTACION and ultimo_evento.tipo_evento != TipoEvento.EGRESO:
        raise HTTPException(
            status_code=400,
            detail="La exportación solo puede registrarse después de un egreso"
        )
    

        