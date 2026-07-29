from src.database.conexao import conectar

def inserir(equipamento):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO equipamentos (id_cliente, tipo, marca, modelo, numero_serie, data_compra)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        equipamento.id_cliente, equipamento.tipo, equipamento.marca, equipamento.modelo, equipamento.numero_serie, equipamento.data_compra
    )
    cursor.execute(sql, valores)
    conexao.commit()
    equipamento.id_equipamento = cursor.lastrowid
    cursor.close()
    conexao.close()
    return equipamento

def listar_por_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM equipamentos WHERE id_cliente = %s AND status = 1"
    cursor.execute(sql, (id_cliente,))
    equipamentos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return equipamentos

def atualizar(equipamento):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE equipamentos
        SET tipo = %s, marca = %s, modelo = %s, numero_serie = %s, data_compra = %s, updated_at = NOW()
        WHERE id_equipamento = %s AND status = 1
    """
    valores = (
        equipamento.tipo,
        equipamento.marca,
        equipamento.modelo,
        equipamento.numero_serie,
        equipamento.data_compra,
        equipamento.id_equipamento
    )
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_por_id(id_equipamento):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM equipamentos WHERE id_equipamento = %s AND status = 1"
    cursor.execute(sql, (id_equipamento,))
    equipamento = cursor.fetchone()
    cursor.close()
    conexao.close()
    return equipamento