import pymysql
from datetime import datetime

# Variável global para armazenar o usuário logado
usuario_logado = None


def conectar():
    """Cria uma conexão com o banco MySQL usando PyMySQL"""
    try:
        conexao = pymysql.connect(
            host="localhost",
            user="root",
            password="@2368921",
            database="bio_cv",
            charset='utf8mb4',
            autocommit=True
        )
        return conexao
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        raise e


def criar_usuario(name, password, email):
    """Cria um novo usuário no banco de dados"""
    global usuario_logado
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Usa prepared statement para evitar SQL injection
        query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))

        usuario_id = cursor.lastrowid

        usuario_logado = {
            "id": usuario_id,
            "name": name,
            "email": email
        }

        return usuario_logado

    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        usuario_logado = None
        raise e

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def verificar_usuario(email, password):
    """Verifica se o usuário existe no banco de dados"""
    global usuario_logado
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Usa prepared statement
        query = "SELECT id, nome, email FROM usuarios WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, password))

        usuario = cursor.fetchone()

        if usuario:
            usuario_logado = {
                "id": usuario[0],
                "name": usuario[1],
                "email": usuario[2]
            }
        else:
            usuario_logado = None

        return usuario_logado

    except Exception as e:
        print(f"Erro ao verificar usuário: {e}")
        usuario_logado = None
        return None

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def criar_paciente(nome, data_nascimento, genero, telefone):
    """Cria um novo paciente no banco de dados"""
    conexao = None
    cursor = None

    try:
        if not usuario_logado:
            raise Exception("Usuário não está logado")

        conexao = conectar()
        cursor = conexao.cursor()

        query = """INSERT INTO pacientes (nome, data_nascimento, genero, telefone, usuario_id, created_at) 
                   VALUES (%s, %s, %s, %s, %s, NOW())"""

        cursor.execute(query, (nome, data_nascimento, genero, telefone, usuario_logado['id']))

        paciente_id = cursor.lastrowid

        return {
            "id": paciente_id,
            "nome": nome,
            "data_nascimento": data_nascimento,
            "genero": genero,
            "telefone": telefone,
            "usuario_id": usuario_logado['id']
        }

    except Exception as e:
        print(f"Erro ao criar paciente: {e}")
        raise e

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def listar_pacientes():
    """Lista todos os pacientes do usuário logado"""
    conexao = None
    cursor = None

    try:
        if not usuario_logado:
            return []

        conexao = conectar()
        cursor = conexao.cursor()

        query = """SELECT id, nome, data_nascimento, genero, telefone, created_at 
                   FROM pacientes 
                   WHERE usuario_id = %s 
                   ORDER BY nome"""

        cursor.execute(query, (usuario_logado['id'],))
        pacientes = cursor.fetchall()

        # Converte para lista de dicionários
        resultado = []
        for paciente in pacientes:
            resultado.append({
                "id": paciente[0],
                "nome": paciente[1],
                "data_nascimento": paciente[2],
                "genero": paciente[3],
                "telefone": paciente[4],
                "created_at": paciente[5]
            })

        return resultado

    except Exception as e:
        print(f"Erro ao listar pacientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()


def buscar_pacientes(termo_busca):
    """Busca pacientes por nome"""
    conexao = None
    cursor = None

    try:
        if not usuario_logado:
            return []

        conexao = conectar()
        cursor = conexao.cursor()

        query = """SELECT id, nome, data_nascimento, genero, telefone, created_at 
                   FROM pacientes 
                   WHERE usuario_id = %s AND nome LIKE %s 
                   ORDER BY nome"""

        termo_like = f"%{termo_busca}%"
        cursor.execute(query, (usuario_logado['id'], termo_like))
        pacientes = cursor.fetchall()

        # Converte para lista de dicionários
        resultado = []
        for paciente in pacientes:
            resultado.append({
                "id": paciente[0],
                "nome": paciente[1],
                "data_nascimento": paciente[2],
                "genero": paciente[3],
                "telefone": paciente[4],
                "created_at": paciente[5]
            })

        return resultado

    except Exception as e:
        print(f"Erro ao buscar pacientes: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()