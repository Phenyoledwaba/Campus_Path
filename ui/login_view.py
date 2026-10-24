import flet as ft
from core.database import check_login
from ui.dashboard_view import DashboardView

class LoginView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.my_page = page
        self.username_field = ft.TextField(label="Username", width=300, prefix_icon=ft.Icons.PERSON)
        self.password_field = ft.TextField(label="Password", password=True, width=300, prefix_icon=ft.Icons.LOCK)
        self.error_text = ft.Text("", color=ft.Colors.RED)
        
        self.controls = [
            ft.Icon(ft.Icons.SCHOOL, size=80, color=ft.Colors.BLUE_700),
            ft.Text("CampusPath", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Text("Bridging the gap between Grade 12 and graduation.", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            self.username_field,
            self.password_field,
            self.error_text,
            ft.Button("Login", on_click=self.handle_login, width=300, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            ft.Text("Demo Login: student / demo123", size=12, color=ft.Colors.GREY)
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_login(self, e):
        if check_login(self.username_field.value, self.password_field.value):
            self.my_page.controls.clear()
            self.my_page.add(DashboardView(self.my_page, self.username_field.value))
            self.my_page.update()
        else:
            self.error_text.value = "Invalid username or password."
            self.my_page.update()