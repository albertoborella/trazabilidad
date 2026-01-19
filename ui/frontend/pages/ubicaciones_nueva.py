import reflex as rx
from frontend.state.UbicacionesState import UbicacionesState
from frontend.components.layout import layout


@rx.page(route="/ubicaciones/nueva", title="Nueva ubicación")
def ubicaciones_nueva():
    return layout(
        rx.vstack(
            rx.heading("Nueva ubicación", size="5"),

            rx.input(
                placeholder="Código",
                value=UbicacionesState.codigo,
                on_change=UbicacionesState.set_codigo,
            ),

            rx.input(
                placeholder="Nombre",
                value=UbicacionesState.nombre,
                on_change=UbicacionesState.set_nombre,
            ),

            rx.input(
                placeholder="País",
                value=UbicacionesState.pais,
                on_change=UbicacionesState.set_pais,
            ),

            rx.input(
                placeholder="Provincia (opcional)",
                value=UbicacionesState.provincia,
                on_change=UbicacionesState.set_provincia,
            ),

            rx.input(
                placeholder="Ciudad (opcional)",
                value=UbicacionesState.ciudad,
                on_change=UbicacionesState.set_ciudad,
            ),

            rx.hstack(
                rx.button(
                    "Crear",
                    on_click=UbicacionesState.crear_ubicacion,
                ),
                rx.link(
                    rx.button("Cancelar", variant="outline"),
                    href="/ubicaciones",
                ),
                spacing="3",
            ),

            rx.cond(
                UbicacionesState.error,
                rx.text(
                    UbicacionesState.error,
                    color="red",
                    font_size="0.85rem",
                ),
            ),

            spacing="3",
            max_width="420px",
        )
    )

