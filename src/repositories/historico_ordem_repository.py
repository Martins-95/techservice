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