import reflex as rx
from frontend.state.dashboard_state import DashboardState
from frontend.components.stat_card import stat_card
from frontend.components.layout import layout

@rx.page(route="/", title="Dashboard | Trazabilidad", on_load=DashboardState.load_dashboard)
def dashboard():
    return layout(
        rx.vstack(
            rx.heading("Dashboard", size="8", font_weight="bold"),
            rx.text("Resumen general del sistema", color="gray"),

            rx.cond(
                DashboardState.loading,
                rx.center(rx.spinner()),
                rx.grid(
                    stat_card("Productos", DashboardState.total_productos, "package"),
                    stat_card("Lotes", DashboardState.total_lotes, "layers"),
                    stat_card("Stock Total (kg)", DashboardState.stock_total, "scale"),
                    columns="3",
                    spacing="4",
                ),
            ),
            spacing="6",
            width="100%",
        )
    )



