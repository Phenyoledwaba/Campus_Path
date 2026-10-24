import flet as ft
from core.rules import calculate_aps, filter_eligible_courses, SA_SUBJECTS
from core.database import get_all_courses


class DashboardView(ft.Column):
    def __init__(self, page, username):
        super().__init__()
        self.my_page = page
        self.username = username

        self.results = ft.Column()

        # Create 6 rows of Subject Dropdown + Percentage Input
        self.subject_rows = []
        for i in range(6):
            dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(subj) for subj in SA_SUBJECTS],
                width=250,
                hint_text=f"Select Subject {i+1}"
            )
            percent = ft.TextField(
                label="%",
                width=100,
                keyboard_type=ft.KeyboardType.NUMBER
            )
            self.subject_rows.append(
                ft.Row([dropdown, percent], alignment=ft.MainAxisAlignment.CENTER))

        self.controls = [
            ft.Container(
                content=ft.ListView(
                    expand=True,
                    padding=20,
                    spacing=15,
                    controls=[
                        ft.Text(f"Welcome, {self.username}!",
                                size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Select your 6 subjects and enter your percentages:",
                                size=16, color=ft.Colors.GREY_700),
                        ft.Divider(),
                        # Unpack all the subject rows into the ListView
                        *self.subject_rows,
                        ft.Container(
                            content=ft.Button("Calculate APS", on_click=self.calculate,
                                              bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, width=300),
                            alignment=ft.Alignment.CENTER,
                            margin=ft.Margin(top=20)
                        ),
                        ft.Divider(),
                        self.results
                    ]
                ),
                expand=True
            )
        ]
        self.expand = True

    def calculate(self, e):
        self.results.controls.clear()
        marks = {}

        # 1. Extract marks from the dynamic rows
        for row in self.subject_rows:
            dropdown = row.controls[0]
            percent_input = row.controls[1]

            if not dropdown.value or not percent_input.value:
                self.results.controls.append(ft.Text(
                    "Please select a subject and enter a mark for all 6 rows.", color=ft.Colors.RED))
                self.update()
                return

            try:
                marks[dropdown.value] = float(percent_input.value)
            except ValueError:
                self.results.controls.append(ft.Text(
                    "Please ensure all percentages are valid numbers.", color=ft.Colors.RED))
                self.update()
                return

        # 2. Calculate APS
        student_aps = calculate_aps(marks)
        eligible = filter_eligible_courses(student_aps, get_all_courses())

        self.results.controls.append(
            ft.Text(f"Your APS is: {student_aps}", size=22,
                    weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
        )

        # 3. Display Results
        if not eligible:
            self.results.controls.append(
                ft.Text(
                    "You do not currently qualify for the listed courses at UJ, Wits, or TUT. Keep pushing!", color=ft.Colors.RED)
            )
        else:
            for c in eligible:
                self.results.controls.append(
                    ft.Card(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.SCHOOL,
                                            color=ft.Colors.BLUE_700),
                            title=ft.Text(
                                c.course_name, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(
                                f"{c.institution} | Requires APS: {c.min_aps}"),
                        )
                    )
                )

        self.update()
