from src.database.conexao import conectar

def abrir_ordem(ordem):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO ordens_servico 
        (id_equipamento, id_status, defeito_relatado, prioridade, valor_servico, valor_pecas, desconto, valor_total, observacoes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        ordem.id_equipamento,
        ordem.id_status,
        ordem.defeito_relatado,
        ordem.prioridade,
        ordem.valor_servico,
        ordem.valor_pecas,
        ordem.desconto,
        ordem.valor_total,
        ordem.observacoes
    )
    cursor.execute(sql, valores)
    conexao.commit()
    ordem.id_ordem = cursor.lastrowid
    cursor.close()
    conexao.close()
    return ordem

def atualizar_status(id_ordem, novo_status_id):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE ordens_servico SET id_status = %s, updated_at = NOW() WHERE id_ordem = %s"
    cursor.execute(sql, (novo_status_id, id_ordem))
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_por_id(id_ordem):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT os.*, s.nome as status_nome 
        FROM ordens_servico os
        JOIN status_ordem s ON os.id_status = s.id_status
        WHERE os.id_ordem = %s
    """
    cursor.execute(sql, (id_ordem,))
    ordem = cursor.fetchone()
    cursor.close()
    conexao.close()
    return ordem

def listar():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT os.id_ordem, c.nome AS cliente_nome, eq.modelo AS equipamento_modelo, 
               so.nome AS status_nome, os.valor_total, os.created_at
        FROM ordens_servico os
        JOIN equipamentos eq ON os.id_equipamento = eq.id_equipamento
        JOIN clientes c ON eq.id_cliente = c.id_cliente
        JOIN status_ordem so ON os.id_status = so.id_status
        ORDER BY os.id_ordem DESC
    """
    cursor.execute(sql)
    ordens = cursor.fetchall()
    cursor.close()
    conexao.close()
    return ordens