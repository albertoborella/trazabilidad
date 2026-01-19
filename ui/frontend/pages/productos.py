import reflex as rx
from frontend.components.layout import layout
from frontend.components.productos_table import productos_table
from frontend.components.producto_modal import producto_modal
from frontend.components.delete_confirm_modal import delete_confirm_modal
from frontend.state.productos_state import ProductosState

@rx.page(
    route="/productos",
    title="Productos",
    on_load=ProductosState.load_productos,
)
def productos():
    return layout(
        rx.vstack(
            # Header: título + botón
            rx.hstack(
                rx.vstack(
                    rx.heading("Productos", size="6", font_weight="medium"),
                    rx.text(
                        "Gestión de productos del sistema",
                        color="gray",
                        font_size="0.9em",
                    ),
                    spacing="1",
                ),
                rx.button(
                    "+ Nuevo",
                    size="2",
                    variant="soft",
                    on_click=ProductosState.open_create,
                ),
                justify="between",
                align="center",
                width="100%",
            ),

            # Tabla / loader
            rx.cond(
                ProductosState.loading,
                rx.center(rx.spinner(size="3")),
                productos_table(),
            ),

            # Modales
            producto_modal(),
            delete_confirm_modal(),

            spacing="4",
            width="100%",
        )
    )

    

