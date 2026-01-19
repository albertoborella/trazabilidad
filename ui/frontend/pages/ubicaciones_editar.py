import reflex as rx
from frontend.state.UbicacionesState import UbicacionesState
from frontend.components.layout import layout  


@rx.page(route="/ubicaciones/editar/[id]", on_load=UbicacionesState.cargar_ubicacion)
def ubicaciones_editar():
    return layout(
        rx.vstack(
            rx.heading("Editar ubicación", size="4"),

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
                placeholder="Pais",
                value=UbicacionesState.pais,
                on_change=UbicacionesState.set_pais,
            ),

            rx.input(
                placeholder="Provincia",
                value=UbicacionesState.provincia,
                on_change=UbicacionesState.set_provincia,
            ),

            rx.input(
                placeholder="Ciudad",
                value=UbicacionesState.ciudad,
                on_change=UbicacionesState.set_ciudad,
            ),

            rx.cond(
                UbicacionesState.error,
                rx.text(UbicacionesState.error, color="red"),
            ),

            rx.hstack(
                rx.button(
                    "Actualizar",
                    on_click=UbicacionesState.actualizar_ubicacion,
                    color_scheme="blue",
                ),
                rx.button(
                    "Cancelar",
                    on_click=rx.redirect("/ubicaciones"),
                    variant="soft",
                ),
            ),

            spacing='4',
            max_w="500px",
            mx="auto",
        )
    )







