from fastapi import FastAPI 
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import productos, ubicaciones, eventos, tipos_ubicacion, lotes, trazabilidad


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title="API de Trazabilidad de Productos")

app.include_router(eventos.router)
app.include_router(productos.router)
app.include_router(tipos_ubicacion.router)
app.include_router(ubicaciones.router) 
app.include_router(lotes.router)
app.include_router(trazabilidad.router) 


