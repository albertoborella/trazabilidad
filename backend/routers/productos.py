from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Producto, EventoTrazabilidad
from schemas.productos import ProductoCreate, ProductoRead
from schemas.trazabilidad import (
    TrazabilidadResponse,
    ProductoTimeline,
    EventoTimeline,
    UbicacionTimeline
)

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post(
    "",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED
)
def crear_producto(
    producto: ProductoCreate,
    session: Session = Depends(get_session)
):
    existe = session.exec(
        select(Producto).where(
            Producto.codigo_producto == producto.codigo_producto
        )
    ).first()

    if existe:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un producto con ese código"
        )

    nuevo = Producto.model_validate(producto)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    return nuevo


@router.get(
    "/codigo/{codigo_producto}",
    response_model=ProductoRead
)
def obtener_producto_por_codigo(
    codigo_producto: str,
    session: Session = Depends(get_session)
):
    producto = session.exec(
        select(Producto).where(
            Producto.codigo_producto == codigo_producto
        )
    ).first()

    if not producto:
        raise HTTPException(404, "Producto no encontrado")

    return producto


@router.get(
    "",
    response_model=list[ProductoRead]
)
def listar_productos(
    session: Session = Depends(get_session)
):
    return session.exec(select(Producto)).all()


@router.get(
    "/{producto_id}/trazabilidad",
    response_model=TrazabilidadResponse
)
def obtener_trazabilidad(
    producto_id: int,
    session: Session = Depends(get_session)
):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    eventos = session.exec(
        select(EventoTrazabilidad)
        .where(EventoTrazabilidad.producto_id == producto_id)
        .order_by(EventoTrazabilidad.fecha_hora)
    ).all()

    timeline = [
        EventoTimeline(
            fecha_hora=e.fecha_hora,
            tipo_evento=e.tipo_evento,
            ubicacion=UbicacionTimeline(
                codigo=e.ubicacion.codigo,
                nombre=e.ubicacion.nombre
            ),
            observaciones=e.observaciones
        )
        for e in eventos
    ]

    return TrazabilidadResponse(
        producto=ProductoTimeline.model_validate(producto),
        trazabilidad=timeline
    )


