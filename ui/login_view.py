import flet as ft
from core.database import check_login
from ui.dashboard_view import DashboardView

class LoginView(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.my_page = page
        self.username_field = ft.TextField(label="Username", width=300, prefix_icon=ft.Icons.PERSON, border_color=ft.Colors.GREY_400, focused_border_color=ft.Colors.BLUE_700)
        self.password_field = ft.TextField(label="Password", password=True, width=300, prefix_icon=ft.Icons.LOCK, border_color=ft.Colors.GREY_400, focused_border_color=ft.Colors.BLUE_700)
        self.error_text = ft.Text("", color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD)
        
        self.login_card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.ACCOUNT_BALANCE, size=60, color=ft.Colors.BLUE_700),
                ft.Text("CampusPath", size=32, weight=ft.FontWeight.W_900, color=ft.Colors.BLUE_900),
                ft.Text("Higher Education Pathway", size=14, color=ft.Colors.GREY_600),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                self.username_field,
                self.password_field,
                self.error_text,
                ft.Button("Login to Dashboard", on_click=self.handle_login, width=300, height=45, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                ft.TextButton("No Data? Try USSD Mode (*123*4#)", icon=ft.Icons.PHONE_ANDROID, on_click=self.show_ussd_mockup, style=ft.ButtonStyle(color=ft.Colors.GREY_700)),
                ft.Text("Demo: student / demo123", size=12, color=ft.Colors.GREY_500)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40, bgcolor=ft.Colors.WHITE, border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
        )
        
        self.controls = [self.login_card]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True

    def handle_login(self, e):
        if check_login(self.username_field.value, self.password_field.value):
            self.my_page.controls.clear()
            self.my_page.add(DashboardView(self.my_page, self.username_field.value))
            self.my_page.update()
        else:
            self.error_text.value = "Invalid username or password."
            self.my_page.update()

    def show_ussd_mockup(self, e):
        self.my_page.controls.clear()
        self.ussd_input = ft.TextField(hint_text="Type 1, 2, 3 or 4 and press Enter", width=300, color=ft.Colors.GREEN_400, border_color=ft.Colors.GREEN_400, on_submit=self.handle_ussd_response)
        self.ussd_screen = ft.Text("Welcome to CampusPath.\nReply with your APS to see courses and funding:\n\n1. APS 20-25\n2. APS 26-30\n3. APS 31-35\n4. APS 36+", color=ft.Colors.WHITE, size=16)
        
        self.my_page.add(ft.Container(bgcolor=ft.Colors.BLACK, padding=30, expand=True, content=ft.Column([
            ft.Text("USSD SIMULATION", color=ft.Colors.GREEN_400, size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Dial: *123*4#", color=ft.Colors.GREEN_400, size=16),
            ft.Divider(color=ft.Colors.GREEN_700),
            self.ussd_screen,
            ft.Divider(color=ft.Colors.GREEN_700),
            self.ussd_input,
            ft.TextButton("Exit USSD", on_click=lambda _: self.return_to_login(), style=ft.ButtonStyle(color=ft.Colors.RED_400))
        ])))
        self.my_page.update()

    def handle_ussd_response(self, e):
        user_input = self.ussd_input.value.strip()
        if user_input == "1":
            response = "APS 20-25:\n- Diploma in Business IT (UJ)\n- Diploma in Accounting (TUT)\n\nFUNDING:\n- NSFAS\n- ISFAP"
        elif user_input == "2":
            response = "APS 26-30:\n- Diploma in IT (TUT)\n- Diploma in Sport Management (UJ)\n- BA in Performing Arts (Wits)\n\nFUNDING:\n- NSFAS\n- ISFAP"
        elif user_input == "3":
            response = "APS 31-35:\n- BCom Accounting (UJ)\n- BEng Tech Electrical (TUT)\n- BSc Biological Sciences (Wits)\n\nFUNDING:\n- ISFAP\n- Feenix"
        elif user_input == "4":
            response = "APS 36+:\n- BSc Computer Science (UJ)\n- BCom Finance (Wits)\n- BA Law (Wits)\n- BSc Engineering (Wits)\n\nFUNDING:\n- FNB Fund\n- Feenix"
        else:
            response = "Invalid selection. Please reply with 1, 2, 3, or 4."
            
        self.ussd_screen.value = f"Welcome to CampusPath.\nReply with your APS to see courses and funding:\n\n1. APS 20-25\n2. APS 26-30\n3. APS 31-35\n4. APS 36+\n\n>> You selected: {user_input}\n\n{response}"
        self.ussd_input.value = ""
        self.my_page.update()
        
    def return_to_login(self):
        self.my_page.controls.clear()
        self.my_page.add(LoginView(self.my_page))
        self.my_page.update()