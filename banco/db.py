import mysql.connector


# Variável global para armazenar o usuário logado
usuario_logado = None

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@2368921",
        database="bio_cv"
    )

def criar_usuario(name, password, email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (name, email, password))
    conexao.commit()
    usuario_id = cursor.lastrowid  # Obtém o ID do último registro inserido
    global usuario_logado
    usuario_logado = {
        "id": usuario_id,
        "name": name,
        "email": email
    }
    cursor.close()
    conexao.close()
    return usuario_logado

def verificar_usuario(email, password):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = %s AND senha = %s", (email, password))
    usuario = cursor.fetchone()
    if usuario:
        global usuario_logado
        usuario_logado = {
            "id": usuario[0],  # ID do usuário
            "name": usuario[1],  # Nome do usuário
            "email": usuario[2]  # Email do usuário
        }
    cursor.close()
    conexao.close()
    return usuario_logado
