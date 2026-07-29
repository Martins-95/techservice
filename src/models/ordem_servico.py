class OrdemServico:
    def __init__(
        self,
        id_equipamento,
        defeito_relatado,
        prioridade="MEDIA",
        valor_servico=0.0,
        valor_pecas=0.0,
        desconto=0.0,
        id_status=1,
        id_ordem=None,
        diagnostico="",
        solucao="",
        observacoes=""
    ):
        self.id_ordem = id_ordem
        self.id_equipamento = id_equipamento
        self.id_status = id_status
        self.defeito_relatado = defeito_relatado
        self.diagnostico = diagnostico
        self.solucao = solucao
        self.prioridade = prioridade
        self.valor_servico = valor_servico
        self.valor_pecas = valor_pecas
        self.desconto = desconto
        self.observacoes = observacoes
        
        # Chama o método de cálculo definido abaixo
        self.valor_total = self.calcular_total()

    def calcular_total(self):
        """Calcula o valor total da ordem de serviço."""
        return (self.valor_servico + self.valor_pecas) - self.desconto