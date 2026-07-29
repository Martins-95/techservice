class Equipamento:
    def __init__(self, id_cliente, tipo, marca, modelo, numero_serie, data_compra=None, id_equipamento=None, status=1):
        self.id_equipamento = id_equipamento
        self.id_cliente = id_cliente
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.data_compra = data_compra
        self.status = status