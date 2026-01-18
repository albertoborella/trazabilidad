import reflex as rx
import httpx


class UbicacionesState(rx.State):
    ubicaciones: list[dict] = []
    loading: bool = False
    error: str | None = None

    # Formulario
    codigo: str = ""
    nombre: str = ""
    pais: str = ""
    provincia: str = ""
    ciudad: str = ""

    #SETTERS
    def set_codigo(self, value: str):
        self.codigo = value

    def set_nombre(self, value: str):
        self.nombre = value

    def set_pais(self, value: str):
        self.pais = value

    def set_provincia(self, value: str):
        self.provincia = value

    def set_ciudad(self, value: str):
        self.ciudad = value

    async def cargar_ubicaciones(self):
        self.loading = True
        self.error = None
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get("http://127.0.0.1:8001/ubicaciones/")
                response.raise_for_status()
                self.ubicaciones = response.json()
            except httpx.HTTPError as e:
                self.error = str(e)
            finally:
                self.loading = False

    async def crear_ubicacion(self):
        self.loading = True
        self.error = None
        nueva_ubicacion = {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "pais": self.pais,
            "provincia": self.provincia,
            "ciudad": self.ciudad,
            "tipo_id": 1,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://127.0.0.1:8001/ubicaciones",
                json=nueva_ubicacion,
            )
            if response.status_code == 201:
                await self.cargar_ubicaciones()
                return rx.redirect("/ubicaciones")
                
            self.error = response.json().get("detail", "Error al crear ubicación")

    def reset_form(self):
        self.codigo = ""
        self.nombre = ""
        self.pais = ""
        self.provincia = ""
        self.ciudad = ""

