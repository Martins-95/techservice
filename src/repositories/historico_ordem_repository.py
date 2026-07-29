from src.database.conexao import conectar

def registrar_historico(id_ordem, id_status_anterior, id_status_novo, observacao="", usuario="Sistema"):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO historico_ordem_servico 
        (id_ordem, id_status_anterior, id_status_novo, observacao, usuario)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (id_ordem, id_status_anterior, id_status_novo, observacao, usuario))
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_por_ordem(id_ordem):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT h.id_historico, h.data_alteracao, h.usuario, h.observacao,
               sa.nome AS status_anterior, sn.nome AS status_novo
        FROM historico_ordem_servico h
        LEFT JOIN status_ordem sa ON h.id_status_anterior = sa.id_status
        JOIN status_ordem sn ON h.id_status_novo = sn.id_status
        WHERE h.id_ordem = %s
        ORDER BY h.data_alteracao ASC
    """
    cursor.execute(sql, (id_ordem,))
    historicos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return historicos