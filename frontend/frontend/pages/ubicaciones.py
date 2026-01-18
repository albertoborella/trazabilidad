import reflex as rx  
from frontend.state.UbicacionesState import UbicacionesState
from frontend.components.layout import layout


def fila_ubicacion(u: dict):
    return rx.table.row(
        rx.table.cell(u["codigo"]),
        rx.table.cell(u["nombre"]),
        rx.table.cell(u["pais"]),
        rx.table.cell(u.get("provincia", "")),
        rx.table.cell(u.get("ciudad", "")),
    )


@rx.page(
    route="/ubicaciones",
    title="Ubicaciones",
    on_load=UbicacionesState.cargar_ubicaciones,
)
def ubicaciones() -> rx.Component:
    return layout(
        rx.vstack(
            rx.hstack(
                rx.heading("Ubicaciones", size="5"),
                rx.link(
                    rx.button("Nueva ubicación"),
                    href="/ubicaciones/nueva",
                ),
                justify="between",
                width="100%",
            ),

            rx.cond(
                UbicacionesState.loading,
                rx.spinner(),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Código"),
                            rx.table.column_header_cell("Nombre"),
                            rx.table.column_header_cell("País"),
                            rx.table.column_header_cell("Provincia"),
                            rx.table.column_header_cell("Ciudad"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            UbicacionesState.ubicaciones,
                            fila_ubicacion,
                        )
                    ),
                    width="100%",
                ),
            ),

            rx.cond(
                UbicacionesState.error,
                rx.text(
                    UbicacionesState.error,
                    color="red",
                    font_size="0.85rem",
                ),
            ),

            spacing="4",
            width="100%",
        )
    )

    