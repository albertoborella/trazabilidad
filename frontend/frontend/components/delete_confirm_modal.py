import reflex as rx
from frontend.state.productos_state import ProductosState


def delete_confirm_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.dialog.title("Confirmar eliminación"),

                rx.text(
                    "¿Está seguro que desea eliminar este producto? "
                    "Esta acción no se puede deshacer.",
                    color="red",
                ),

                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        on_click=ProductosState.close_delete_confirm,
                    ),
                    rx.button(
                        "Eliminar",
                        color_scheme="red",
                        on_click=ProductosState.confirm_delete,
                    ),
                    justify="end",
                    spacing="3",
                ),
                spacing="4",
            )
        ),
        open=ProductosState.confirm_delete_open,
    )
