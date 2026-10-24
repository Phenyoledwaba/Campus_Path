import flet as ft
from core.database import initialize_db
from ui.login_view import LoginView


def main(page: ft.Page):
    page.title = "CampusPath"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 700
    page.window_height = 800

    initialize_db()

    # We add the view directly to the page
    page.add(LoginView(page))


if __name__ == "__main__":
    ft.run(main)
