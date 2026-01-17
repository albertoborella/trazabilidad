import reflex as rx
from frontend.pages.dashboard import dashboard
from frontend.pages.productos import productos

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="gray",
        radius="medium",
        font_family="Inter",
    ),
     stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap"
    ],
)




