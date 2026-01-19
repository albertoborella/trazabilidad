import reflex as rx

def stat_card(title: str, value, icon: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(icon),
                rx.text(title, font_weight="bold"),
                justify="between",
                width="100%",
            ),
            rx.heading(value, size="6"),
            spacing="2",
        ),
        padding="2em",
        width="100%",
        border_radius="large",
        box_shadow="md",
    )
