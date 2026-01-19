import reflex as rx
import httpx

API_URL = "http://127.0.0.1:8001"


class ProductosState(rx.State):
    productos: list[dict] = []
    loading: bool = False

    # form state
    codigo_producto: str = ""
    nombre: str = ""
    producto_id: int | None = None
    modal_open: bool = False

    # ===== SETTERS EXPLÍCITOS (evitan el warning) =====
    def set_codigo_producto(self, value: str):
        self.codigo_producto = value

    def set_nombre(self, value: str):
        self.nombre = value

    async def load_productos(self):
        self.loading = True
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/productos")
                self.productos = response.json()
        except Exception as e:
            print("Error cargando productos:", e)
        self.loading = False

    # ======================
    # MODAL
    # ======================
    def open_create(self):
        self.producto_id = None
        self.codigo_producto = ""
        self.nombre = ""
        self.modal_open = True

    def open_edit(self, producto_id: int):
        producto = next(
            (p for p in self.productos if p["id"] == producto_id),
            None,
        )
        if not producto:
            return

        self.producto_id = producto["id"]
        self.codigo_producto = producto["codigo_producto"]
        self.nombre = producto["nombre"]
        self.modal_open = True

    def close_modal(self):
        self.modal_open = False

    # ======================
    # GUARDAR
    # ======================
    async def save_producto(self):
        data = {
            "codigo_producto": self.codigo_producto,
            "nombre": self.nombre,
        }

        async with httpx.AsyncClient() as client:
            if self.producto_id is None:
                await client.post(f"{API_URL}/productos", json=data)
            else:
                await client.put(
                    f"{API_URL}/productos/{self.producto_id}",
                    json=data,
                )

        self.modal_open = False
        await self.load_productos()

    # ======================
    # ELIMINAR
    # ======================
    async def delete_producto(self, producto_id: int):
        async with httpx.AsyncClient() as client:
            await client.delete(f"{API_URL}/productos/{producto_id}")

        await self.load_productos()

    # ======================
    # CONFIRMAR ELIMINACIÓN
    # ======================
    delete_id: int | None = None
    confirm_delete_open: bool = False

    def open_delete_confirm(self, producto_id: int):
        self.delete_id = producto_id
        self.confirm_delete_open = True

    def close_delete_confirm(self):
        self.delete_id = None
        self.confirm_delete_open = False

    async def confirm_delete(self):
        if self.delete_id is None:
            return

        async with httpx.AsyncClient() as client:
            await client.delete(f"{API_URL}/productos/{self.delete_id}")

        self.close_delete_confirm()
        await self.load_productos()


