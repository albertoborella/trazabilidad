import reflex as rx   
import httpx

API_URL = "http://127.0.0.1:8001"

class DashboardState(rx.State):
    total_productos: int = 0
    total_lotes: int = 0
    stock_total: float = 0.0
    loading: bool = False

    async def load_dashboard(self):
        self.loading = True

        try:
            async with httpx.AsyncClient() as client:
                productos = await client.get(f"{API_URL}/productos")
                lotes = await client.get(f"{API_URL}/lotes")
                stock = await client.get(f"{API_URL}/lotes/stock-total")

            self.total_productos = len(productos.json())
            self.total_lotes = len(lotes.json())
            self.stock_total = stock.json().get("stock_total", 0.0)

        except httpx.HTTPError as e:
             print("Error cargando dashboard:", e)

        self.loading = False