import reflex as rx
from frontend.pages.dashboard import dashboard
from frontend.pages.productos import productos
from frontend.pages.ubicaciones import ubicaciones
from frontend.pages.ubicaciones_nueva import ubicaciones_nueva
from frontend.pages.ubicaciones_editar import ubicaciones_editar

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




