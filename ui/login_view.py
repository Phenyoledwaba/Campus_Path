import flet as ft
from core.database import check_login
from ui.dashboard_view import DashboardView

class LoginView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.my_page = page
        
        # UI Components
        self.username_field = ft.TextField(label="Username", width=300, prefix_icon=ft.Icons.PERSON)
        self.password_field = ft.TextField(label="Password", password=True, width=300, prefix_icon=ft.Icons.LOCK)
        self.error_text = ft.Text("", color=ft.Colors.RED)
        
        # Layout
        self.controls = [
            ft.Container(height=40),
            ft.Icon(ft.Icons.SCHOOL, size=80, color=ft.Colors.BLUE_700),
            ft.Text("CampusPath", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Text("Bridging the gap between Grade 12 and graduation.", size=14, color=ft.Colors.GREY_700),
            ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
            self.username_field,
            self.password_field,
            self.error_text,
            ft.Button("Login", on_click=self.handle_login, width=300, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            
            # USSD Mockup Button
            ft.TextButton(
                "No Data? Try USSD Mode (*123*4#)", 
                icon=ft.Icons.PHONE_ANDROID, 
                on_click=self.show_ussd_mockup
            ),
            
            ft.Text("Demo Login: student / demo123", size=12, color=ft.Colors.GREY)
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_login(self, e):
        """Validates credentials and loads the dashboard."""
        if check_login(self.username_field.value, self.password_field.value):
            self.my_page.controls.clear()
            self.my_page.add(DashboardView(self.my_page, self.username_field.value))
            self.my_page.update()
        else:
            self.error_text.value = "Invalid username or password."
            self.my_page.update()

    def show_ussd_mockup(self, e):
        """Simulates a USSD screen for low-data users."""
        self.my_page.controls.clear()
        self.my_page.add(
            ft.Container(
                bgcolor=ft.Colors.BLACK,
                padding=20,
                expand=True,
                content=ft.Column([
                    ft.Text("USSD SIMULATION", color=ft.Colors.GREEN, size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Dial: *123*4#", color=ft.Colors.GREEN),
                    ft.Divider(color=ft.Colors.GREEN),
                    ft.Text("Welcome to CampusPath.\nReply with your APS to see courses:\n\n1. APS 20-25\n2. APS 26-30\n3. APS 31-35\n4. APS 36+", color=ft.Colors.WHITE, size=16),
                    ft.Divider(color=ft.Colors.GREEN),
                    ft.TextButton("Exit USSD", on_click=lambda _: self.return_to_login(), style=ft.ButtonStyle(color=ft.Colors.RED))
                ])
            )
        )
        self.my_page.update()
        
    def return_to_login(self):
        """Returns the user to the main login screen."""
        self.my_page.controls.clear()
        self.my_page.add(LoginView(self.my_page))
        self.my_page.update()