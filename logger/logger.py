from banco import conectar


class Logger:
    @staticmethod
    def registrar_acao(usuario_id, acao):
        print('Registrando ação:', usuario_id, acao)
        conexao = None
        cursor = None

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO logs (usuario_id, acao) VALUES (%s, %s)", (usuario_id, acao))

        except Exception as e:
            print(f"Erro ao registrar log: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()