class Cliente:

    def __init__(
        self,
        nome,
        email,
        telefone="",
        nif="",
        morada="",
        id_cliente=None,
        status=1
    ):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.nif = nif
        self.morada = morada
        self.status = status