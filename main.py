import flet as ft
from core.database import initialize_db
from ui.login_view import LoginView

def main(page: ft.Page):
    page.title = "CampusPath"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_100
    page.window_width = 450 
    page.window_height = 850
    page.padding = 0
    
    initialize_db()
    page.add(LoginView(page))

if __name__ == "__main__":
    ft.run(main)