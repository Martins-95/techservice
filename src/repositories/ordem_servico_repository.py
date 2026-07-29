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