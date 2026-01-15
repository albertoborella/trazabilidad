from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from database import get_session
from models import EventoTrazabilidad
from schemas.eventos import EventoCreate, EventoRead
from services.trazabilidad import validar_evento

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("", response_model=EventoRead, status_code=status.HTTP_201_CREATED)
def crear_evento(
    evento: EventoCreate,
    session: Session = Depends(get_session),
):
    validar_evento(session, evento)

    nuevo = EventoTrazabilidad.model_validate(evento)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    return nuevo


@router.get("/lote/{lote_id}", response_model=list[EventoRead])
def listar_eventos_por_lote(
    lote_id: int,
    session: Session = Depends(get_session),
):
    return session.exec(
        select(EventoTrazabilidad)
        .where(EventoTrazabilidad.lote_id == lote_id)
        .order_by(EventoTrazabilidad.fecha_hora)
    ).all()

