from src.repositories import ordem_servico_repository, historico_ordem_repository

def alterar_status_ordem(id_ordem, id_status_anterior, id_status_novo, observacao="", usuario="Sistema"):
    # 1. Atualiza o status na ordem de serviço
    ordem_servico_repository.atualizar_status(id_ordem, id_status_novo)
    
    # 2. Regista o movimento no histórico
    historico_ordem_repository.registrar_historico(
        id_ordem=id_ordem,
        id_status_anterior=id_status_anterior,
        id_status_novo=id_status_novo,
        observacao=observacao,
        usuario=usuario
    )