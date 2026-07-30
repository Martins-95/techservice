from datetime import datetime

class HistoricoOrdem:
    def __init__(self, id_ordem, status_novo, status_anterior=None, observacao="", usuario="Sistema",data=None, id_historico=None):
        self.id_ordem = id_ordem
        self.status_novo = status_novo
        self.status_anterior = status_anterior
        self.observacao = observacao
        self.usuario = usuario
        self.data_hora = data
        self.id_historico = id_historico

    def registrar(self, repo_historico):
        return repo_historico.registrar_historico(
            id_ordem=self.id_ordem,
            id_status_anterior=self.status_anterior,
            id_status_novo=self.status_novo,
            observacao=self.observacao,
            usuario=self.usuario
        )

    @staticmethod
    def listar(id_ordem, repo_historico):
        return repo_historico.listar_por_ordem(id_ordem)