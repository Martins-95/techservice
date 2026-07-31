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
        print(" 7. Listar Equipamentos")
        print(" 8. Editar Equipamento")
        print(" 9. Abrir Ordem de Serviço")
        print("10. Alterar Estado da Ordem")
        print("11. Listar Ordens de Serviço")
        print("12. Consultar Histórico da Ordem")
        print(" 0. Sair")
        print("="*45)
        
        opcao = input("Selecione uma opção (0-12): ").strip()
        
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

        # 7. Listar Equipamentos
        elif opcao == "7":
            equipamentos = equipamento_repository.listar_equipamentos()
            print("\n" + "-"*65)
            print("                LISTA DE EQUIPAMENTOS ATIVOS")
            print("-"*65)
            if equipamentos:
                for eq in equipamentos:
                    print(f"ID: {eq['id_equipamento']:<3} | Tipo: {eq['tipo']:<15} | Marca: {eq['marca']:<15} | Modelo: {eq['modelo']:<20} | Nº Série: {eq['numero_serie']}")
            else:
                print("Nenhum equipamento ativo encontrado.")
            print("-"*65)

        # 8. Editar Equipamento
        elif opcao == "8":
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

        # 9. Abrir Ordem de Serviço
        elif opcao == "9":
            print("\n--- ABERTURA DE ORDEM DE SERVIÇO ---")
            id_eq = input("ID do Equipamento: ").strip()
            
            # Verificar se o equipamento existe
            eq = equipamento_repository.buscar_por_id(id_eq)
            if not eq:
                print("❌ Equipamento não encontrado.")
            else:
                cliente = cliente_repository.buscar_por_id(eq['id_cliente'])
                print(f"➜ Equipamento: {eq['marca']} {eq['modelo']} | Cliente: {cliente['nome']}")
                
                defeito = input("Defeito Relatado: ").strip()
                tecnico = input("Técnico Responsável: ").strip() or "Ana Pereira"
                prioridade = input("Prioridade (BAIXA, MEDIA, ALTA) [MEDIA]: ").strip().upper() or "MEDIA"
                
                v_servico = float(input("Valor Serviço (€) [0.0]: ").strip() or 0.0)
                v_pecas = float(input("Valor Peças (€) [0.0]: ").strip() or 0.0)
                desc = float(input("Desconto (€) [0.0]: ").strip() or 0.0)
                
                # 1. Instanciar e gravar a OS
                os_obj = OrdemServico(
                    id_equipamento=id_eq,
                    defeito_relatado=defeito,
                    prioridade=prioridade,
                    valor_servico=v_servico,
                    valor_pecas=v_pecas,
                    desconto=desc
                )
                ordem_servico_repository.abrir_ordem(os_obj)
                
                # 2. Registar o histórico inicial com o Técnico
                historico_ordem_repository.registrar_historico(
                    id_ordem=os_obj.id_ordem,
                    id_status_anterior=None,
                    id_status_novo=1,  # 1 = Aberta / Em Serviço
                    observacao="Abertura inicial da Ordem de Serviço",
                    usuario=tecnico
                )
                
                info = ordem_servico_repository.buscar_detalhes_exibicao(os_obj.id_ordem)
                data_formatada = info['created_at'].strftime("%d/%m/%Y %H:%M")
                
                print("\n" + "┌" + "─"*46 + "┐")
                print(f"│ {'ORDENS DE SERVIÇO':^44} │")
                print("├" + "─"*46 + "┤")
                print(f"│  ID: {info['id_ordem']:<39} │")
                print(f"│  Cliente: {info['cliente_nome']:<34} │")
                print(f"│  Equipamento: {info['equipamento_modelo']:<30} │")
                print(f"│  Defeito: {info['defeito_relatado']:<34} │")
                print(f"│  Estado: {info['status_nome']:<35} │")
                print(f"│  Técnico: {info['tecnico']:<34} │")
                print(f"│  Abertura: {data_formatada:<33} │")
                print("└" + "─"*46 + "┘")
                print("\033[92m>> Operação realizada com sucesso!\033[0m\n")

        # 10. Alterar Estado da Ordem
        elif opcao == "10":
            id_os = input("ID da Ordem de Serviço: ")
            print("Estados disponíveis: 1-Aberta | 2-Em Andamento | 3-Aguardando Peças | 4-Concluída | 5-Cancelada")
            novo_st = int(input("Novo ID do Estado: "))
            obs = input("Observação da mudança: ")
            tecnico = input("Técnico responsável [Técnico]: ") or "Técnico"
            
            sucesso, msg = ordem_servico_service.alterar_status_ordem(id_os, novo_st, obs, tecnico)
            print("✅ " + msg if sucesso else "❌ " + msg)

        # 11. Listar Ordens de Serviço
        elif opcao == "11":
            ordens = ordem_servico_repository.listar()
            print("\n" + "-"*60)
            print("LISTA DE ORDENS DE SERVIÇO")
            print("-"*60)
            for o in ordens:
                print(f"OS #{o['id_ordem']} | Cliente: {o['cliente_nome']} | Equip: {o['equipamento_modelo']} | Status: {o['status_nome']} | Total: {o['valor_total']:.2f}€")

        # 12. Consultar Histórico da Ordem
        elif opcao == "12":
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