import flet as ft
from src.models.cliente import Cliente
from src.repositories import cliente_repository


class ClienteView(ft.Column):

    def __init__(self):
        super().__init__(scroll=ft.ScrollMode.AUTO, expand=True)

        # Campos do Formulário
        self.txt_nome = ft.TextField(label="Nome", width=350)
        self.txt_nif = ft.TextField(
            label="NIF", width=350, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.txt_telefone = ft.TextField(
            label="Telefone", width=350, keyboard_type=ft.KeyboardType.PHONE
        )
        self.txt_email = ft.TextField(
            label="Email", width=350, keyboard_type=ft.KeyboardType.EMAIL
        )

        # Tabela de Clientes
        self.tabela_clientes = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("NIF")),
                ft.DataColumn(ft.Text("Telefone")),
                ft.DataColumn(ft.Text("Email")),
            ],
            rows=[],
        )

        # Montagem do Layout
        self.controls = [
            ft.Text("Cadastro de Cliente", size=24, weight=ft.FontWeight.BOLD),
            self.txt_nome,
            self.txt_nif,
            self.txt_telefone,
            self.txt_email,
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Guardar", icon="save", on_click=self.guardar_cliente
                    ),
                    ft.OutlinedButton(
                        "Limpar", icon="clear", on_click=self.limpar_campos
                    ),
                ],
                spacing=10,
            ),
            ft.Divider(height=20, thickness=2),
            ft.Text("Lista de Clientes", size=20, weight=ft.FontWeight.BOLD),
            self.tabela_clientes,
        ]

    def did_mount(self):
        """Executado automaticamente pelo Flet assim que o componente é inserido na página"""
        self.atualizar_tabela()

    def guardar_cliente(self, e):
        """Coleta dados da UI, valida e chama o repository"""
        nome = self.txt_nome.value.strip() if self.txt_nome.value else ""
        nif = self.txt_nif.value.strip() if self.txt_nif.value else ""
        telefone = (
            self.txt_telefone.value.strip() if self.txt_telefone.value else ""
        )
        email = self.txt_email.value.strip() if self.txt_email.value else ""

        if not nome or not email:
            self.mostrar_mensagem(
                "Nome e Email são campos obrigatórios!", erro=True
            )
            return

        try:
            novo_cliente = Cliente(
                nome=nome, nif=nif, telefone=telefone, email=email
            )
            cliente_repository.inserir(novo_cliente)

            self.mostrar_mensagem("Cliente registrado com sucesso!")
            self.limpar_campos(None)
            self.atualizar_tabela()
        except Exception as ex:
            self.mostrar_mensagem(f"Erro ao guardar cliente: {ex}", erro=True)

    def limpar_campos(self, e):
        """Limpa o formulário"""
        self.txt_nome.value = ""
        self.txt_nif.value = ""
        self.txt_telefone.value = ""
        self.txt_email.value = ""
        self.update()

    def atualizar_tabela(self):
        """Atualiza a tabela consumindo o método do cliente_repository"""
        clientes = cliente_repository.listar()
        self.tabela_clientes.rows.clear()

        for c in clientes:
            self.tabela_clientes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(c["id_cliente"]))),
                        ft.DataCell(ft.Text(c["nome"])),
                        ft.DataCell(ft.Text(c["nif"] or "N/A")),
                        ft.DataCell(ft.Text(c["telefone"] or "N/A")),
                        ft.DataCell(ft.Text(c["email"])),
                    ]
                )
            )
        self.update()

    def mostrar_mensagem(self, texto, erro=False):
        """Exibe SnackBar com feedback visual"""
        cor = "red" if erro else "green"
        snack_bar = ft.SnackBar(
            content=ft.Text(texto, color="white"),
            bgcolor=cor,  # <--- Corrigido de bg_color para bgcolor
            open=True,
        )
        if self.page:
            self.page.overlay.append(snack_bar)
            self.page.update()