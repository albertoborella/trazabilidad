import reflex as rx
from frontend.components.sidebar import sidebar

def layout(content: rx.Component) -> rx.Component:
    return rx.box(
            rx.hstack(
                sidebar(),
                rx.box(
                    content,
                    padding="24px",
                    width="100%",
                ),
                width="100%",
                min_height="100vh",
            ),
            width="100%",
            font_family="Inter",
            background_color="gray.1",
        )

