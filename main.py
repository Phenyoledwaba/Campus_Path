import flet as ft
from core.database import initialize_db
from ui.login_view import LoginView


def main(page: ft.Page):
    page.title = "CampusPath"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Dimensions tailored for mobile scaling
    page.window_width = 400
    page.window_height = 850

    initialize_db()
    page.add(LoginView(page))


if __name__ == "__main__":
    ft.run(main)
