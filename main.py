def rodar_terminal():
    from src.views.menu import exibir_menu
    exibir_menu()

def rodar_flet():
    import flet as ft
    from src.views.cliente_view import ClienteView

    def main_gui(page: ft.Page):
        page.title = "TechService - Sistema de Gestão"
        page.window_width = 850
        page.window_height = 700
        page.padding = 20

        cliente_view = ClienteView()
        page.add(cliente_view)

    ft.app(target=main_gui)

if __name__ == "__main__":
    print("\n=== TECHSERVICE - MODO DE EXECUÇÃO ===")
    print("1. Modo Terminal (Consola / CLI)")
    print("2. Modo Interface Gráfica (Flet)")
    
    opcao = input("Como deseja iniciar o programa? (1 ou 2): ").strip()

    if opcao == "2":
        rodar_flet()
    else:
        rodar_terminal()