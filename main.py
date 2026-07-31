import flet as ft
from src.views.cliente_view import ClienteView


def main(page: ft.Page):
    page.title = "TechService - Sistema de Gestão de Assistência Técnica"
    page.window_width = 850
    page.window_height = 700
    page.padding = 20

    # Instancia a vista sem passar 'page'
    cliente_view = ClienteView()
    page.add(cliente_view)


if __name__ == "__main__":
    ft.app(target=main)

