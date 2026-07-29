from src.database.conexao import conectar

def inserir(cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO clientes (nome, email, telefone, nif, morada)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (cliente.nome, cliente.email, cliente.telefone, cliente.nif, cliente.morada)
    cursor.execute(sql, valores)
    conexao.commit()
    cliente.id_cliente = cursor.lastrowid
    cursor.close()
    conexao.close()
    return cliente

def listar():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM clientes WHERE status = 1 ORDER BY id_cliente"
    cursor.execute(sql)
    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clientes

def atualizar(cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE clientes
        SET nome = %s,
            email = %s,
            telefone = %s,
            updated_at = NOW()
        WHERE id_cliente = %s
          AND status = 1
    """
    valores = (cliente.nome, cliente.email, cliente.telefone, cliente.id_cliente)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def excluir(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE clientes
        SET status = 0,
            deleted_at = NOW()
        WHERE id_cliente = %s
          AND status = 1
    """

    cursor.execute(sql, (id_cliente,))
    conexao.commit()

    cursor.close()
    conexao.close()

def buscar_por_id(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM clientes WHERE id_cliente = %s AND status = 1"
    cursor.execute(sql, (id_cliente,))
    cliente = cursor.fetchone()
    cursor.close()
    conexao.close()
    return cliente

def pesquisar_por_nome(nome):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = "SELECT * FROM clientes WHERE nome LIKE %s AND status = 1"
    cursor.execute(sql, (f"%{nome}%",))
    clientes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return clientes

