from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import Ubicacion, TipoUbicacion
from schemas.ubicaciones import UbicacionCreate, UbicacionRead

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

@router.post(
    "",
    response_model=UbicacionRead,
    status_code=status.HTTP_201_CREATED
)
def crear_ubicacion(
    ubicacion: UbicacionCreate,
    session: Session = Depends(get_session)
):
    if not session.get(TipoUbicacion, ubicacion.tipo_id):
        raise HTTPException(404, "Tipo de ubicación inexistente")

    existe = session.exec(
        select(Ubicacion).where(
            Ubicacion.codigo == ubicacion.codigo
        )
    ).first()

    if existe:
        raise HTTPException(409, "Ya existe una ubicación con ese código")

    nueva = Ubicacion.model_validate(ubicacion)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)

    return nueva


@router.get("/")
def listar_ubicaciones(
    tipo_id: int | None = None,
    session: Session = Depends(get_session),
):
    query = select(Ubicacion)

    if tipo_id:
        query = query.where(Ubicacion.tipo_id == tipo_id)

    return session.exec(query).all()


@router.get("/{ubicacion_id}")
def obtener_ubicacion(
    ubicacion_id: int,
    session: Session = Depends(get_session),
):
    ubicacion = session.get(Ubicacion, ubicacion_id)
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion

# ======================
# EDITAR (PUT)
# ======================
@router.put("/{ubicacion_id}", response_model=UbicacionRead)
def actualizar_producto(
    ubicacion_id: int,
    datos: UbicacionCreate,
    session: Session = Depends(get_session),
):
    ubicacion = session.get(Ubicacion, ubicacion_id)

    if not ubicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ubicacion no registrada",
        )

    ubicacion.codigo = datos.codigo
    ubicacion.nombre = datos.nombre
    ubicacion.pais = datos.pais
    ubicacion.provincia = datos.provincia
    ubicacion.ciudad = datos.ciudad
    ubicacion.tipo_id = datos.tipo_id

    session.add(ubicacion)
    session.commit()
    session.refresh(ubicacion)

    return ubicacion


# ======================
# ELIMINAR (DELETE)
# ======================
@router.delete("/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ubicacion(
    ubicacion_id: int,
    session: Session = Depends(get_session),
):
    ubicacion = session.get(Ubicacion, ubicacion_id)

    if not ubicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ubicacion no registrada",
        )

    session.delete(ubicacion)
    session.commit()

    return None
