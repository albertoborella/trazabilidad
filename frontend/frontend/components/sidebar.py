import reflex as rx

def sidebar_item(label: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(label),
            spacing="3",
            padding="0.75em",
            border_radius="medium",
            _hover={
                "background_color": rx.color("accent", 3),
            },
            width="100%",
        ),
        href=href,
        width="100%",
        text_decoration="none",
        color="inherit",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Trazabilidad", size="6", margin_bottom="1em"),

            sidebar_item("Dashboard", "layout-dashboard", "/"),
            sidebar_item("Productos", "package", "/productos"),
            sidebar_item("Lotes", "layers", "/lotes"),
            sidebar_item("Eventos", "repeat", "/eventos"),
            sidebar_item("Ubicaciones", "map-pin", "/ubicaciones"),

            rx.spacer(),

            rx.divider(),
            rx.color_mode.button(),
            spacing="2",
            width="100%",
        ),
        width="220px",
        min_width="220px",
        height="100vh",
        padding="1 em",
        border_right="1px solid",
        border_color=rx.color("gray", 4),
        background_color="white",
    )
