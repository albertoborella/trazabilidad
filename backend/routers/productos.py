from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Producto, LoteProduccion
from schemas.productos import ProductoCreate, ProductoRead
from schemas.lotes import LoteRead

router = APIRouter(prefix="/productos", tags=["Productos"])


# ======================
# CREAR
# ======================
@router.post("", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(
    producto: ProductoCreate,
    session: Session = Depends(get_session),
):
    existe = session.exec(
        select(Producto).where(Producto.codigo_producto == producto.codigo_producto)
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un producto con ese código",
        )

    nuevo = Producto.model_validate(producto)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)

    return nuevo


# ======================
# LISTAR
# ======================
@router.get("", response_model=list[ProductoRead])
def listar_productos(session: Session = Depends(get_session)):
    return session.exec(select(Producto)).all()


# ======================
# OBTENER POR ID
# ======================
@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return producto


# ======================
# OBTENER POR CÓDIGO
# ======================
@router.get("/codigo/{codigo_producto}", response_model=ProductoRead)
def obtener_por_codigo(codigo_producto: str, session: Session = Depends(get_session)):
    producto = session.exec(
        select(Producto).where(Producto.codigo_producto == codigo_producto)
    ).first()

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    return producto


# ======================
# EDITAR (PUT)
# ======================
@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(
    producto_id: int,
    datos: ProductoCreate,
    session: Session = Depends(get_session),
):
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    producto.codigo_producto = datos.codigo_producto
    producto.nombre = datos.nombre

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return producto


# ======================
# ELIMINAR (DELETE)
# ======================
@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    session: Session = Depends(get_session),
):
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    session.delete(producto)
    session.commit()

    return None


# ======================
# LOTES POR PRODUCTO
# ======================
@router.get("/{producto_id}/lotes", response_model=list[LoteRead])
def listar_lotes_por_producto(
    producto_id: int,
    session: Session = Depends(get_session),
):
    return session.exec(
        select(LoteProduccion).where(LoteProduccion.producto_id == producto_id)
    ).all()



