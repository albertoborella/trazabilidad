from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from services.trazabilidad import stock_disponible
from database import get_session
from models import LoteProduccion, Producto
from schemas.lotes import LoteCreate, LoteRead

router = APIRouter(prefix="/lotes", tags=["Lotes"])


@router.post("", response_model=LoteRead, status_code=status.HTTP_201_CREATED)
def crear_lote(lote: LoteCreate, session: Session = Depends(get_session)):
    if not session.get(Producto, lote.producto_id):
        raise HTTPException(404, "Producto inexistente")

    existe = session.exec(
        select(LoteProduccion)
        .where(LoteProduccion.producto_id == lote.producto_id)
        .where(LoteProduccion.lote == lote.lote)
    ).first()

    if existe:
        raise HTTPException(409, "Ya existe ese lote para el producto")

    nuevo = LoteProduccion.model_validate(lote)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    return nuevo


@router.get("", response_model=list[LoteRead])
def listar_lotes(session: Session = Depends(get_session)):
    return session.exec(select(LoteProduccion)).all()


@router.get("/{lote_id}", response_model=LoteRead)
def obtener_lote(lote_id: int, session: Session = Depends(get_session)):
    lote = session.get(LoteProduccion, lote_id)
    if not lote:
        raise HTTPException(404, "Lote no encontrado")
    return lote



@router.get("/{lote_id}/stock")
def obtener_stock_lote(
    lote_id: int,
    session: Session = Depends(get_session),
):
    lote = session.get(LoteProduccion, lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    stock = stock_disponible(session, lote_id)

    return {
        "lote_id": lote_id,
        "lote": lote.lote,
        "stock_disponible": stock,
    }
