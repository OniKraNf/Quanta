import flet as ft
import time

def show_window(page: ft.Page, item_text: str):
    # Добавление строки с текстом
    page.add(
        ft.Row([
            ft.Text(value=item_text)
        ])
    )

ft.app(target=show_window)