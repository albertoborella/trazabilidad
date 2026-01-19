import reflex as rx
from frontend.state.UbicacionesState import UbicacionesState
from frontend.components.layout import layout


def action_icon(icon: str, color: str, on_click) -> rx.Component:
    return rx.icon_button(
        rx.icon(icon, size=16),
        variant="ghost",
        size="1",
        color_scheme=color,
        on_click=on_click,
    )


def fila_ubicacion(u: dict):
    return rx.table.row(
        rx.table.cell(
            u["codigo"],
            font_size="0.8rem",
            padding="0.35em 0.5em",
        ),
        rx.table.cell(
            u["nombre"],
            font_size="0.8rem",
            padding="0.35em 0.5em",
        ),
        rx.table.cell(
            u.get("provincia", ""),
            font_size="0.8rem",
            padding="0.35em 0.5em",
        ),
        rx.table.cell(
            u.get("ciudad", ""),
            font_size="0.8rem",
            padding="0.35em 0.5em",
        ),
        rx.table.cell(
            rx.hstack(
                action_icon(
                    "pencil",
                    "gray",
                    UbicacionesState.open_edit(u["id"]),
                ),
                action_icon(
                    "trash-2",
                    "red",
                    UbicacionesState.open_delete_confirm(u["id"]),
                ),
                spacing="1",
            ),
            padding="0.25em",
        ),
        rx.cond(
    UbicacionesState.show_delete_modal,
    rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Eliminar ubicación"),
            rx.dialog.description(
                "¿Estás seguro que querés eliminar esta ubicación?"
            ),
            rx.hstack(
                rx.button(
                    "Cancelar",
                    variant="soft",
                    on_click=UbicacionesState.close_delete_confirm,
                ),
                rx.button(
                    "Eliminar",
                    color_scheme="red",
                    on_click=UbicacionesState.delete_ubicacion,
                ),
                justify="end",
                spacing="3",
            ),
        ),
        open=True,
    ),
),

    ),



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
                            rx.table.column_header_cell(
                                "Código",
                                font_size="0.75rem",
                                padding="0.4em",
                            ),
                            rx.table.column_header_cell(
                                "Nombre",
                                font_size="0.75rem",
                                padding="0.4em",
                            ),
                            rx.table.column_header_cell(
                                "Provincia",
                                font_size="0.75rem",
                                padding="0.4em",
                            ),
                            rx.table.column_header_cell(
                                "Ciudad",
                                font_size="0.75rem",
                                padding="0.4em",
                            ),
                            rx.table.column_header_cell(
                                "Acciones",
                                font_size="0.75rem",
                                padding="0.4em",
                                width="90px",
                            ),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            UbicacionesState.ubicaciones,
                            fila_ubicacion,
                        )
                    ),
                    width="100%",
                    variant="surface",
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



    