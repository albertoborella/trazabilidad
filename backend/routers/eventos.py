from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from database import get_session
from models import EventoTrazabilidad
from schemas.eventos import EventoCreate, EventoRead
from services.trazabilidad import validar_evento

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post(
    "",
    response_model=EventoRead,
    status_code=status.HTTP_201_CREATED
)
def crear_evento(
    evento: EventoCreate,
    session: Session = Depends(get_session)
):
    validar_evento(session, evento)

    nuevo_evento = EventoTrazabilidad.model_validate(evento)

    session.add(nuevo_evento)
    session.commit()
    session.refresh(nuevo_evento)

    return nuevo_evento
