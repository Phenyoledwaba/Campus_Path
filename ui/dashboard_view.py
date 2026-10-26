import flet as ft
from core.rules import calculate_aps, filter_eligible_courses, SA_SUBJECTS
from core.database import get_all_courses

class DashboardView(ft.Column):
    def __init__(self, page, username):
        super().__init__()
        self.my_page = page
        self.username = username
        
        self.results_list = ft.ListView(expand=True, spacing=10, padding=20)
        
        self.subject_rows = []
        for i in range(6):
            dropdown = ft.Dropdown(options=[ft.dropdown.Option(subj) for subj in SA_SUBJECTS], width=260, hint_text=f"Subject {i+1}", border_color=ft.Colors.GREY_300, focused_border_color=ft.Colors.BLUE_700)
            percent = ft.TextField(label="%", width=80, keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.GREY_300, focused_border_color=ft.Colors.BLUE_700)
            self.subject_rows.append(ft.Row([dropdown, percent], alignment=ft.MainAxisAlignment.CENTER, spacing=15))
            
        self.income_dropdown = ft.Dropdown(width=355, hint_text="Select Household Income", border_color=ft.Colors.GREY_300, focused_border_color=ft.Colors.BLUE_700, options=[ft.dropdown.Option("Under R350,000"), ft.dropdown.Option("Between R350,000 and R600,000"), ft.dropdown.Option("Above R600,000")])
        
        self.controls = [
            ft.AppBar(title=ft.Text("CampusPath Dashboard", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.BLUE_900, actions=[ft.IconButton(icon=ft.Icons.LOGOUT, icon_color=ft.Colors.WHITE, tooltip="Logout", on_click=self.logout)]),
            ft.Container(
                content=ft.ListView(expand=True, padding=30, spacing=20, controls=[
                    ft.Container(content=ft.Column([ft.Text(f"Welcome back, {self.username}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900), ft.Text("Complete your profile below to generate your pathway.", size=14, color=ft.Colors.GREY_600)]), padding=20, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK))),
                    ft.Container(content=ft.Column([
                        ft.Text("Academic Profile", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        ft.Divider(),
                        *self.subject_rows,
                        ft.Divider(),
                        ft.Text("Financial Profile", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                        self.income_dropdown,
                        ft.Container(content=ft.Button("Generate Pathway", on_click=self.calculate, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, width=300, height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))), alignment=ft.Alignment.CENTER, margin=ft.Margin(top=15))
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=30, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK))),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    self.results_list
                ]),
                expand=True, bgcolor=ft.Colors.GREY_100
            )
        ]
        self.expand = True

    def logout(self, e):
        self.my_page.controls.clear()
        from ui.login_view import LoginView
        self.my_page.add(LoginView(self.my_page))
        self.my_page.update()

    def make_card(self, title, subtitle, color, icon, url=None):
        card_content = ft.Container(bgcolor=color, padding=20, border_radius=10, content=ft.Column([ft.Icon(icon, color=ft.Colors.WHITE, size=30), ft.Text(title, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16), ft.Text(subtitle, color=ft.Colors.WHITE, size=12, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS)]))
        if url:
            return ft.Card(elevation=5, content=ft.Container(content=card_content, on_click=lambda e: e.page.run_task(ft.UrlLauncher().launch_url, url), ink=True))
        return ft.Card(elevation=5, content=card_content)

    def calculate(self, e):
        self.results_list.controls.clear()
        marks = {}
        selected_subjects = []
        
        for row in self.subject_rows:
            subject = row.controls[0].value
            percent = row.controls[1].value
            if not subject or not percent:
                self.results_list.controls.append(ft.Text("Please complete all 6 subject rows.", color=ft.Colors.RED))
                self.update()
                return
            if subject in selected_subjects:
                self.results_list.controls.append(ft.Text(f"Error: You selected '{subject}' more than once.", color=ft.Colors.RED))
                self.update()
                return
            selected_subjects.append(subject)
            try:
                marks[subject] = float(percent)
            except ValueError:
                self.results_list.controls.append(ft.Text("Ensure all percentages are valid numbers.", color=ft.Colors.RED))
                self.update()
                return

        home_langs = [s for s in selected_subjects if "Home Language" in s]
        first_add_langs = [s for s in selected_subjects if "First Additional Language" in s]
        if len(home_langs) == 0:
            self.results_list.controls.append(ft.Text("Error: You must select 1 Home Language.", color=ft.Colors.RED))
            self.update()
            return
        if len(first_add_langs) == 0:
            self.results_list.controls.append(ft.Text("Error: You must select 1 First Additional Language.", color=ft.Colors.RED))
            self.update()
            return

        has_maths = any("Mathematics" in s or "Mathematical Literacy" in s for s in selected_subjects)
        if not has_maths:
            self.results_list.controls.append(ft.Text("Error: You must select Mathematics or Mathematical Literacy.", color=ft.Colors.RED))
            self.update()
            return

        if not self.income_dropdown.value:
            self.results_list.controls.append(ft.Text("Please select your household income.", color=ft.Colors.RED))
            self.update()
            return

        student_aps = calculate_aps(marks)
        eligible = filter_eligible_courses(student_aps, get_all_courses())

        self.results_list.controls.append(ft.Text("Your APS Score", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900))
        self.results_list.controls.append(self.make_card("Your APS", str(student_aps), ft.Colors.GREEN_700, ft.Icons.STAR))
        
        self.results_list.controls.append(ft.Divider(height=20))
        self.results_list.controls.append(ft.Text("Funding Pathways", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900))
        
        if "Under" in self.income_dropdown.value:
            self.results_list.controls.append(self.make_card("NSFAS", "Full Bursary", ft.Colors.BLUE_700, ft.Icons.MONEY, url="https://www.nsfas.org.za/content/"))
            self.results_list.controls.append(self.make_card("ISFAP", "Missing Middle", ft.Colors.INDIGO_400, ft.Icons.SCHOOL, url="https://www.isfap.org.za/"))
        elif "Between" in self.income_dropdown.value:
            self.results_list.controls.append(self.make_card("ISFAP", "Missing Middle", ft.Colors.INDIGO_400, ft.Icons.SCHOOL, url="https://applyonline.isfap.org.za/"))
            self.results_list.controls.append(self.make_card("Feenix", "Crowdfunding", ft.Colors.PURPLE_500, ft.Icons.PEOPLE, url="https://feenix.org/for-students"))
        else:
            self.results_list.controls.append(self.make_card("FNB Fund", "Merit Bursary", ft.Colors.ORANGE_700, ft.Icons.ACCOUNT_BALANCE, url="https://www.studytrust.org.za"))
            self.results_list.controls.append(self.make_card("Feenix", "Crowdfunding", ft.Colors.PURPLE_500, ft.Icons.PEOPLE, url="https://feenix.org/for-students"))
            self.results_list.controls.append(self.make_card("Study Loan", "Bank Loan", ft.Colors.GREY_700, ft.Icons.CREDIT_CARD, url="https://www.nsfas.org.za/"))

        self.results_list.controls.append(ft.Divider(height=20))
        self.results_list.controls.append(ft.Text("Qualifying Courses", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900))
        
        for c in eligible:
            course_url = ""
            if "Johannesburg" in c.institution: course_url = "https://www.uj.ac.za/apply/"
            elif "Wits" in c.institution: course_url = "https://www.wits.ac.za/undergraduate/apply-to-wits/"
            elif "Tshwane" in c.institution: course_url = "https://www.tut.ac.za/apply"
            
            self.results_list.controls.append(self.make_card(c.course_name, f"{c.institution}\nReq APS: {c.min_aps}", ft.Colors.CYAN_700, ft.Icons.BOOK, url=course_url))
            
        self.update()