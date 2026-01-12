from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import TipoUbicacion
from schemas.tipos_ubicacion import TipoUbicacionCreate, TipoUbicacionRead

router = APIRouter(prefix="/tipos-ubicacion", tags=["Tipos de Ubicación"])

@router.post(
    "",
    response_model=TipoUbicacionRead,
    status_code=status.HTTP_201_CREATED
)
def crear_tipo_ubicacion(
    tipo: TipoUbicacionCreate,
    session: Session = Depends(get_session)
):
    existe = session.exec(
        select(TipoUbicacion).where(
            TipoUbicacion.codigo == tipo.codigo
        )
    ).first()

    if existe:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un tipo de ubicación con ese código"
        )

    nuevo = TipoUbicacion.model_validate(tipo)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    return nuevo

@router.get(
    "",
    response_model=list[TipoUbicacionRead]
)
def listar_tipos_ubicacion(
    session: Session = Depends(get_session)
):
    return session.exec(select(TipoUbicacion)).all()
