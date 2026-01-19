import reflex as rx
from frontend.state.productos_state import ProductosState

def action_icon(icon: str, color: str, on_click) -> rx.Component:
    return rx.icon_button(
        rx.icon(icon, size=16),
        variant="ghost",
        size="1",
        color_scheme=color,
        on_click=on_click,
    )


def productos_table() -> rx.Component:
    return rx.table.root(
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
                    "Acciones",
                    font_size="0.75rem",
                    padding="0.4em",
                    width="90px",
                ),
            )
        ),
        rx.table.body(
            rx.foreach(
                ProductosState.productos,
                lambda p: rx.table.row(
                    rx.table.cell(
                        p["codigo_producto"],
                        font_size="0.8rem",
                        padding="0.35em 0.5em",
                    ),
                    rx.table.cell(
                        p["nombre"],
                        font_size="0.8rem",
                        padding="0.35em 0.5em",
                    ),
                    rx.table.cell(
                        rx.hstack(
                            action_icon(
                                "pencil",
                                "gray",
                                ProductosState.open_edit(p["id"]),
                            ),
                            action_icon(
                                "trash-2",
                                "red",
                                ProductosState.open_delete_confirm(p["id"]),
                            ),
                            spacing="1",
                        ),
                        padding="0.25em",
                    ),
                ),
            )
        ),
        width="100%",
        variant="surface",
    )





        
        
    

