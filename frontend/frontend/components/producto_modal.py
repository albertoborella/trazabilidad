import reflex as rx
from frontend.state.productos_state import ProductosState

def producto_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Título
                rx.dialog.title(
                    rx.cond(
                        ProductosState.producto_id is None,
                        "Nuevo producto",
                        "Editar producto",
                    )
                ),

                # Formulario
                rx.input(
                    placeholder="Código de producto",
                    value=ProductosState.codigo_producto,
                    on_change=ProductosState.set_codigo_producto,
                ),
                rx.input(
                    placeholder="Nombre",
                    value=ProductosState.nombre,
                    on_change=ProductosState.set_nombre,
                ),

                # Acciones
                rx.hstack(
                    rx.button(
                        "Cancelar",
                        variant="soft",
                        on_click=ProductosState.close_modal,
                    ),
                    rx.button(
                        "Guardar",
                        on_click=ProductosState.save_producto,
                    ),
                    justify="end",
                    spacing="3",
                ),

                spacing="4",
                width="100%",
            ),
        ),
        open=ProductosState.modal_open,
    )



