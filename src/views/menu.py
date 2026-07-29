from src.models.cliente import Cliente
from src.repositories import cliente_repository

def exibir_menu():
    while True:
        print("\n=== TechService - Gestão de Assistência Técnica ===")
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            c = Cliente(nome=nome, email=email, telefone=telefone)
            cliente_repository.inserir(c)
            print(f"Cliente inserido com sucesso! ID: {c.id_cliente}")
        elif opcao == "2":
            print("\n--- Lista de Clientes ---")
            for item in cliente_repository.listar():
                print(f"ID: {item['id_cliente']} | Nome: {item['nome']} | Email: {item['email']}")
        elif opcao == "0":
            break