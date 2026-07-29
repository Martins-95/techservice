from src.repositories import ordem_servico_repository, historico_ordem_repository

def alterar_status_ordem(id_ordem, novo_status_id, observacao="", usuario="Técnico"):
    ordem = ordem_servico_repository.buscar_por_id(id_ordem)
    if not ordem:
        return False, "Ordem de serviço não encontrada."
    
    status_anterior = ordem['id_status']
    
    # 1. Atualizar o estado da OS
    ordem_servico_repository.atualizar_status(id_ordem, novo_status_id)
    
    # 2. Registar a alteração no histórico
    historico_ordem_repository.registrar_historico(
        id_ordem=id_ordem,
        id_status_anterior=status_anterior,
        id_status_novo=novo_status_id,
        observacao=observacao,
        usuario=usuario
    )
    return True, "Estado da Ordem alterado com sucesso!"