import flet as ft
from core.rules import calculate_aps, filter_eligible_courses, SA_SUBJECTS
from core.database import get_all_courses

class DashboardView(ft.Column):
    def __init__(self, page, username):
        super().__init__()
        self.my_page = page
        self.username = username
        
        # Grid to display result cards
        self.results_grid = ft.GridView(expand=True, max_extent=350, child_aspect_ratio=1.5, spacing=10, run_spacing=10)
        
        # Dynamic Subject Inputs
        self.subject_rows = []
        for i in range(6):
            dropdown = ft.Dropdown(options=[ft.dropdown.Option(subj) for subj in SA_SUBJECTS], width=250, hint_text=f"Subject {i+1}")
            percent = ft.TextField(label="%", width=80, keyboard_type=ft.KeyboardType.NUMBER)
            self.subject_rows.append(ft.Row([dropdown, percent], alignment=ft.MainAxisAlignment.CENTER, spacing=10))
            
        # Income Input for Funding Logic
        self.income_dropdown = ft.Dropdown(
            width=350,
            hint_text="Select Household Income",
            options=[
                ft.dropdown.Option("Under R350,000"),
                ft.dropdown.Option("Between R350,000 and R600,000"),
                ft.dropdown.Option("Above R600,000")
            ]
        )
        
        # Main Layout
        self.controls = [
            ft.AppBar(title=ft.Text("CampusPath Dashboard"), bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
            ft.Container(
                content=ft.ListView(
                    expand=True, padding=20, spacing=15,
                    controls=[
                        ft.Text(f"Welcome, {self.username}!", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Enter your subjects and income to generate your pathway:", size=14, color=ft.Colors.GREY_700),
                        ft.Divider(),
                        *self.subject_rows,
                        ft.Divider(),
                        self.income_dropdown,
                        ft.Container(
                            content=ft.Button("Calculate APS & Find Funding", on_click=self.calculate, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, width=300, height=50),
                            alignment=ft.Alignment.CENTER, margin=ft.Margin(top=20)
                        ),
                        ft.Divider(),
                        ft.Text("Your Results:", size=18, weight=ft.FontWeight.BOLD),
                        self.results_grid
                    ]
                ),
                expand=True
            )
        ]
        self.expand = True

    def make_card(self, title, subtitle, color, icon):
        """Helper function to generate a uniform result card."""
        return ft.Card(
            elevation=5,
            content=ft.Container(
                bgcolor=color,
                padding=15,
                border_radius=10,
                content=ft.Column([
                    ft.Icon(icon, color=ft.Colors.WHITE, size=30),
                    ft.Text(title, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(subtitle, color=ft.Colors.WHITE, size=12, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS)
                ])
            )
        )

    def calculate(self, e):
        """Calculates APS and determines course/funding eligibility."""
        self.results_grid.controls.clear()
        marks = {}
        
        # Validate subject inputs
        for row in self.subject_rows:
            if not row.controls[0].value or not row.controls[1].value:
                self.results_grid.controls.append(ft.Text("Please complete all 6 rows.", color=ft.Colors.RED))
                self.update()
                return
            try:
                marks[row.controls[0].value] = float(row.controls[1].value)
            except ValueError:
                self.results_grid.controls.append(ft.Text("Invalid number.", color=ft.Colors.RED))
                self.update()
                return
                
        if not self.income_dropdown.value:
            self.results_grid.controls.append(ft.Text("Please select income.", color=ft.Colors.RED))
            self.update()
            return

        # Run logic
        student_aps = calculate_aps(marks)
        eligible = filter_eligible_courses(student_aps, get_all_courses())
        
        # Render APS Card
        self.results_grid.controls.append(self.make_card("Your APS", str(student_aps), ft.Colors.GREEN_700, ft.Icons.STAR))
        
        # Render Funding Cards based on income
        if "Under" in self.income_dropdown.value:
            self.results_grid.controls.append(self.make_card("NSFAS", "Full Bursary", ft.Colors.BLUE_700, ft.Icons.MONEY))
            self.results_grid.controls.append(self.make_card("ISFAP", "Missing Middle", ft.Colors.INDIGO_400, ft.Icons.SCHOOL))
        elif "Between" in self.income_dropdown.value:
            self.results_grid.controls.append(self.make_card("ISFAP", "Missing Middle", ft.Colors.INDIGO_400, ft.Icons.SCHOOL))
            self.results_grid.controls.append(self.make_card("Feenix", "Crowdfunding", ft.Colors.PURPLE_500, ft.Icons.PEOPLE))
        else:
            self.results_grid.controls.append(self.make_card("FNB Fund", "Merit Bursary", ft.Colors.ORANGE_700, ft.Icons.ACCOUNT_BALANCE))
            self.results_grid.controls.append(self.make_card("Feenix", "Crowdfunding", ft.Colors.PURPLE_500, ft.Icons.PEOPLE))
            self.results_grid.controls.append(self.make_card("Study Loan", "Bank Loan", ft.Colors.GREY_700, ft.Icons.CREDIT_CARD))

        # Render Course Cards
        for c in eligible:
            self.results_grid.controls.append(self.make_card(c.course_name, f"{c.institution}\nReq APS: {c.min_aps}", ft.Colors.CYAN_700, ft.Icons.BOOK))
            
        self.update()