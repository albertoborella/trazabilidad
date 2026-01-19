import reflex as rx
import httpx


class UbicacionesState(rx.State):
    print("UbicacionesState CARGADO DESDE:", __file__)

    # =====================
    # Estado general
    # =====================
    ubicaciones: list[dict] = []
    loading: bool = False
    error: str = ""

    # ID activo
    ubicacion_id: int | None = None

    # Modal delete
    show_delete_modal: bool = False

    # =====================
    # Formulario
    # =====================
    codigo: str = ""
    nombre: str = ""
    pais: str = ""
    provincia: str = ""
    ciudad: str = ""

    # =====================
    # Setters
    # =====================
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

    # =====================
    # LISTADO
    # =====================
    async def cargar_ubicaciones(self):
        self.loading = True
        self.error = ""

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get("http://127.0.0.1:8001/ubicaciones/")
                resp.raise_for_status()
                self.ubicaciones = resp.json()
            except Exception as e:
                self.error = str(e)
            finally:
                self.loading = False

    # =====================
    # CREAR
    # =====================
    async def crear_ubicacion(self):
        data = {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "pais": self.pais or None,
            "provincia": self.provincia or None,
            "ciudad": self.ciudad or None,
            "tipo_id": 1,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "http://127.0.0.1:8001/ubicaciones",
                json=data,
            )

        if resp.status_code == 201:
            self.reset_form()
            await self.cargar_ubicaciones()
            return rx.redirect("/ubicaciones")

        self.error = "Error al crear ubicación"

    # =====================
    # EDITAR – LOAD
    # =====================
    async def cargar_ubicacion(self):
        # Obtener ID desde la URL
        path = self.router.url.path
        ubicacion_id = path.split("/")[-1]

        if not ubicacion_id.isdigit():
            self.error = "ID de ubicación no informado"
            return

        self.ubicacion_id = int(ubicacion_id)

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"http://127.0.0.1:8001/ubicaciones/{self.ubicacion_id}"
            )

        if resp.status_code != 200:
            self.error = "No se pudo cargar la ubicación"
            return

        data = resp.json()

        self.codigo = data.get("codigo", "")
        self.nombre = data.get("nombre", "")
        self.pais = data.get("pais", "")
        self.provincia = data.get("provincia", "")
        self.ciudad = data.get("ciudad", "")

    # =====================
    # EDITAR – SAVE
    # =====================
    async def actualizar_ubicacion(self):
        if not self.ubicacion_id:
            self.error = "Ubicación inválida"
            return

        data = {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "pais": self.pais or None,
            "provincia": self.provincia or None,
            "ciudad": self.ciudad or None,
            "tipo_id": 1,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"http://127.0.0.1:8001/ubicaciones/{self.ubicacion_id}",
                json=data,
            )

        if resp.status_code == 200:
            self.reset_form()
            await self.cargar_ubicaciones()
            return rx.redirect("/ubicaciones")

        self.error = "Error al actualizar ubicación"

    # =====================
    # ELIMINAR
    # =====================
    def open_delete_confirm(self, ubicacion_id: int):
        self.ubicacion_id = ubicacion_id
        self.show_delete_modal = True

    def close_delete_confirm(self):
        self.show_delete_modal = False
        self.ubicacion_id = None

    async def delete_ubicacion(self):
        async with httpx.AsyncClient() as client:
            await client.delete(
                f"http://127.0.0.1:8001/ubicaciones/{self.ubicacion_id}"
            )

        self.show_delete_modal = False
        await self.cargar_ubicaciones()

    # =====================
    # Utils
    # =====================
    def reset_form(self):
        self.codigo = ""
        self.nombre = ""
        self.pais = ""
        self.provincia = ""
        self.ciudad = ""
        self.error = ""

    def open_edit(self, ubicacion_id: int):
        return rx.redirect(f"/ubicaciones/editar/{ubicacion_id}")





        






