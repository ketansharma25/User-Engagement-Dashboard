import reflex as rx
from app.components.dashboard import dashboard_component
from app.states.dashboard_state import DashboardState


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            dashboard_component(),
            class_name="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8",
        ),
        class_name="font-['Inter'] bg-gray-100 min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=DashboardState.fetch_metrics)