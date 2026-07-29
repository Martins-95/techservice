from src.models.cliente import Cliente
from src.models.equipamento import Equipamento
from src.models.ordem_servico import OrdemServico
from src.repositories import (
    cliente_repository, 
    equipamento_repository, 
    ordem_servico_repository, 
    historico_ordem_repository
)
from src.services import ordem_servico_service

def exibir_menu():
    while True:
        print("\n" + "="*45)
        print("    TECHSERVICE - SISTEMA DE ASSISTÊNCIA")
        print("="*45)
        print(" 1. Criar Cliente")
        print(" 2. Listar Todos os Clientes")
        print(" 3. Editar Cliente")
        print(" 4. Remover Cliente")
        print(" 5. Pesquisar Cliente por Nome")
        print(" 6. Criar Equipamento")
        print(" 7. Editar Equipamento")
        print(" 8. Abrir Ordem de Serviço")
        print(" 9. Alterar Estado da Ordem")
        print("10. Listar Ordens de Serviço")
        print("11. Consultar Histórico da Ordem")
        print(" 0. Sair")
        print("="*45)
        
        opcao = input("Selecione uma opção (0-11): ").strip()
        
        # 1. Criar Cliente
        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            nif = input("NIF: ")
            morada = input("Morada: ")
            c = Cliente(nome=nome, email=email, telefone=telefone, nif=nif, morada=morada)
            cliente_repository.inserir(c)
            print(f"✅ Cliente inserido! ID: {c.id_cliente}")

        # 2. Listar Todos os Clientes
        elif opcao == "2":
            clientes = cliente_repository.listar()
            print("\n" + "-"*65)
            print("                LISTA DE CLIENTES ATIVOS")
            print("-"*65)
            if clientes:
                for c in clientes:
                    nif_str = c['nif'] if c['nif'] else 'N/A'
                    tel_str = c['telefone'] if c['telefone'] else 'N/A'
                    print(f"ID: {c['id_cliente']:<3} | Nome: {c['nome']:<20} | NIF: {nif_str:<10} | Tel: {tel_str:<10} | Email: {c['email']}")
            else:
                print("Nenhum cliente ativo encontrado.")
            print("-"*65)

        # 3. Editar Cliente
        elif opcao == "3":
            id_c = input("ID do Cliente a editar: ")
            c = cliente_repository.buscar_por_id(id_c)
            if c:
                nome = input(f"Novo Nome [{c['nome']}]: ") or c['nome']
                email = input(f"Novo Email [{c['email']}]: ") or c['email']
                telefone = input(f"Novo Telefone [{c['telefone']}]: ") or c['telefone']
                nif = input(f"Novo NIF [{c['nif']}]: ") or c['nif']
                morada = input(f"Nova Morada [{c['morada']}]: ") or c['morada']
                
                cliente_obj = Cliente(nome=nome, email=email, telefone=telefone, nif=nif, morada=morada, id_cliente=id_c)
                cliente_repository.atualizar(cliente_obj)
                print("✅ Cliente atualizado com sucesso!")
            else:
                print("❌ Cliente não encontrado.")

        # 4. Remover Cliente
        elif opcao == "4":
            id_c = input("ID do Cliente a remover: ")
            if cliente_repository.buscar_por_id(id_c):
                cliente_repository.excluir(id_c)
                print("✅ Cliente removido (exclusão lógica realizada)!")
            else:
                print("❌ Cliente não encontrado.")

        # 5. Pesquisar Cliente por Nome
        elif opcao == "5":
            termo = input("Digite o nome ou parte do nome: ")
            resultados = cliente_repository.pesquisar_por_nome(termo)
            print(f"\n--- Encontrados ({len(resultados)}) ---")
            for item in resultados:
                print(f"ID: {item['id_cliente']} | Nome: {item['nome']} | Tel: {item['telefone']} | Email: {item['email']}")

        # 6. Criar Equipamento
        elif opcao == "6":
            id_cliente = input("ID do Proprietário (Cliente): ")
            if cliente_repository.buscar_por_id(id_cliente):
                tipo = input("Tipo (ex: Laptop, Smartphone): ")
                marca = input("Marca: ")
                modelo = input("Modelo: ")
                sn = input("Número de Série: ")
                eq = Equipamento(id_cliente=id_cliente, tipo=tipo, marca=marca, modelo=modelo, numero_serie=sn)
                equipamento_repository.inserir(eq)
                print(f"✅ Equipamento registado! ID: {eq.id_equipamento}")
            else:
                print("❌ Cliente não existe.")

        # 7. Editar Equipamento
        elif opcao == "7":
            id_eq = input("ID do Equipamento a editar: ")
            eq = equipamento_repository.buscar_por_id(id_eq)
            if eq:
                tipo = input(f"Novo Tipo [{eq['tipo']}]: ") or eq['tipo']
                marca = input(f"Nova Marca [{eq['marca']}]: ") or eq['marca']
                modelo = input(f"Novo Modelo [{eq['modelo']}]: ") or eq['modelo']
                sn = input(f"Novo Nº Série [{eq['numero_serie']}]: ") or eq['numero_serie']
                
                eq_obj = Equipamento(id_cliente=eq['id_cliente'], tipo=tipo, marca=marca, modelo=modelo, numero_serie=sn, id_equipamento=id_eq)
                equipamento_repository.atualizar(eq_obj)
                print("✅ Equipamento atualizado com sucesso!")
            else:
                print("❌ Equipamento não encontrado.")

        # 8. Abrir Ordem de Serviço
        elif opcao == "8":
            id_eq = input("ID do Equipamento: ")
            if equipamento_repository.buscar_por_id(id_eq):
                defeito = input("Defeito Relatado: ")
                prioridade = input("Prioridade (BAIXA, MEDIA, ALTA) [MEDIA]: ").upper() or "MEDIA"
                v_servico = float(input("Valor Serviço (€) [0.0]: ") or 0.0)
                v_pecas = float(input("Valor Peças (€) [0.0]: ") or 0.0)
                desc = float(input("Desconto (€) [0.0]: ") or 0.0)
                
                os = OrdemServico(
                    id_equipamento=id_eq, defeito_relatado=defeito, prioridade=prioridade,
                    valor_servico=v_servico, valor_pecas=v_pecas, desconto=desc
                )
                ordem_servico_repository.abrir_ordem(os)
                historico_ordem_repository.registrar_historico(os.id_ordem, None, 1, "Abertura inicial da OS")
                print(f"✅ Ordem de Serviço #{os.id_ordem} aberta! Total: {os.valor_total:.2f}€")
            else:
                print("❌ Equipamento não encontrado.")

        # 9. Alterar Estado da Ordem
        elif opcao == "9":
            id_os = input("ID da Ordem de Serviço: ")
            print("Estados disponíveis: 1-Aberta | 2-Em Andamento | 3-Aguardando Peças | 4-Concluída | 5-Cancelada")
            novo_st = int(input("Novo ID do Estado: "))
            obs = input("Observação da mudança: ")
            tecnico = input("Técnico responsável [Técnico]: ") or "Técnico"
            
            sucesso, msg = ordem_servico_service.alterar_status_ordem(id_os, novo_st, obs, tecnico)
            print("✅ " + msg if sucesso else "❌ " + msg)

        # 10. Listar Ordens de Serviço
        elif opcao == "10":
            ordens = ordem_servico_repository.listar()
            print("\n" + "-"*60)
            print("LISTA DE ORDENS DE SERVIÇO")
            print("-"*60)
            for o in ordens:
                print(f"OS #{o['id_ordem']} | Cliente: {o['cliente_nome']} | Equip: {o['equipamento_modelo']} | Status: {o['status_nome']} | Total: {o['valor_total']:.2f}€")

        # 11. Consultar Histórico da Ordem
        elif opcao == "11":
            id_os = input("ID da Ordem de Serviço: ")
            historicos = historico_ordem_repository.listar_por_ordem(id_os)
            print(f"\n--- Histórico de Alterações da OS #{id_os} ---")
            if historicos:
                for h in historicos:
                    st_ant = h['status_anterior'] or 'Nenhum'
                    print(f"[{h['data_alteracao']}] ({h['usuario']}): {st_ant} ➔ {h['status_novo']} | Obs: {h['observacao']}")
            else:
                print("Sem histórico ou OS não encontrada.")

        elif opcao == "0":
            print("A encerrar o TechService...")
            break