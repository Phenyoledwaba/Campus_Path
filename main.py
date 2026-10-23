import flet as ft
from database import initialize_db

def main(page: ft.Page):
    page.title = "CampusPath"
    page.add(ft.Text("Welcome to CampusPath - Skeleton Build", size=24))

if __name__ == "__main__":
    initialize_db()
    ft.app(target=main)