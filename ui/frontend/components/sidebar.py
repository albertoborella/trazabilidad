import reflex as rx

FONT_BASE = "Inter, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"


def sidebar_item(text: str, icon: str, href: str):
    return rx.link(
        rx.hstack(
            rx.icon(
                icon,
                size=14,
                color=rx.cond(
                    rx.color_mode == "dark",
                    "#d1d5db",
                    "#374151",
                ),
            ),
            rx.text(
                text,
                font_size="0.85rem",
                font_weight="400",
                font_family=FONT_BASE,
                color=rx.cond(
                    rx.color_mode == "dark",
                    "#e5e7eb",
                    "#374151",
                ),
            ),
            spacing="2",
            align="center",
        ),
        href=href,
        width="100%",
        padding_y="0.4em",
        padding_x="0.5em",
        border_radius="6px",
        _hover={
            "background_color": rx.cond(
                rx.color_mode == "dark",
                "#1f2937",
                "#f3f4f6",
            ),
            "text_decoration": "none",
        },
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            # TÍTULO
            rx.heading(
                "Trazabilidad",
                size="4",
                margin_bottom="1em",
                text_align="center",
                width="100%",
                font_weight="500",
                font_family=FONT_BASE,
                color=rx.cond(
                    rx.color_mode == "dark",
                    "#f9fafb",
                    "#111827",
                ),
            ),

            # MENÚ
            rx.vstack(
                sidebar_item("Dashboard", "layout-dashboard", "/"),
                sidebar_item("Productos", "package", "/productos"),
                sidebar_item("Ubicaciones", "map-pin", "/ubicaciones"),
                sidebar_item("Lotes", "layers", "/lotes"),
                sidebar_item("Eventos", "repeat", "/eventos"),
                spacing="2",
                width="100%",
            ),

            rx.divider(),

            # BOTÓN DARK / LIGHT (FORMA CORRECTA)
            rx.color_mode.button(
                width="100%",
                padding="0.5em",
                border_radius="6px",
                background_color=rx.cond(
                    rx.color_mode == "dark",
                    "#1f2937",
                    "#f3f4f6",
                ),
                color=rx.cond(
                    rx.color_mode == "dark",
                    "#f9fafb",
                    "#111827",
                ),
                _hover={
                    "background_color": rx.cond(
                        rx.color_mode == "dark",
                        "#374151",
                        "#e5e7eb",
                    )
                },
            ),

            spacing="2",
            width="100%",
            align_items="stretch",
        ),

        width="240px",
        height="100vh",
        padding_top="2.5em",
        padding_x="1.25em",
        background_color=rx.cond(
            rx.color_mode == "dark",
            "#111827",
            "#fafafa",
        ),
        border_right=rx.cond(
            rx.color_mode == "dark",
            "1px solid #1f2937",
            "1px solid #e5e7eb",
        ),
    )



    
