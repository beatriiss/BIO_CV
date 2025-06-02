from banco import conectar

class Logger:
    @staticmethod
    def registrar_acao(usuario_id, acao):
        print('ta dentro do logger.py', usuario_id, acao)
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO logs (usuario_id, acao) VALUES (%s, %s)", (usuario_id, acao))
        conexao.commit()
        cursor.close()
        conexao.close()
