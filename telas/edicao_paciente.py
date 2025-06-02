from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QComboBox, QDateEdit)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDate
import sys
from banco import conectar
from banco import db
from logger import Logger
import re


class EdicaoPaciente(QMainWindow):
    def __init__(self, paciente_data):
        super().__init__()

        self.paciente_data = paciente_data

        # Configurações da Janela
        self.setWindowTitle("Editar Paciente - BIO-CV")
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)

        # Tenta adicionar ícone
        try:
            self.setWindowIcon(QIcon("assets/Icon.png"))
        except:
            pass

        # Layout Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header com botão voltar
        header_layout = QHBoxLayout()

        # Botão "Voltar" no canto superior esquerdo
        self.voltar_button = QPushButton("← Voltar")
        self.voltar_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0; 
                color: #666; 
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.voltar_button.setFixedSize(100, 35)
        self.voltar_button.clicked.connect(self.voltar_home)
        header_layout.addWidget(self.voltar_button)

        # Espaçador para empurrar o botão para a esquerda
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Formulário de Edição
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Título
        self.title_label = QLabel(f"Editar Paciente: {paciente_data['nome']}")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setContentsMargins(0, 0, 0, 30)
        form_layout.addWidget(self.title_label)

        # Campo de Nome
        self.nome_label = QLabel("Nome completo:")
        self.nome_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.nome_label)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Digite o nome completo do paciente")
        self.nome_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.nome_input.setFixedHeight(40)
        self.nome_input.setText(paciente_data['nome'])
        form_layout.addWidget(self.nome_input)

        # Campo de Data de Nascimento
        self.data_label = QLabel("Data de nascimento:")
        self.data_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.data_label)

        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)

        # Converte a data do banco para QDate
        if isinstance(paciente_data['data_nascimento'], str):
            # Se for string no formato YYYY-MM-DD
            data_parts = paciente_data['data_nascimento'].split('-')
            if len(data_parts) == 3:
                ano, mes, dia = int(data_parts[0]), int(data_parts[1]), int(data_parts[2])
                self.data_input.setDate(QDate(ano, mes, dia))
        else:
            # Se for objeto date
            self.data_input.setDate(QDate(paciente_data['data_nascimento']))

        self.data_input.setDisplayFormat("dd/MM/yyyy")
        self.data_input.setStyleSheet("""
            QDateEdit {
                border: 2px solid darkgreen;
                border-radius: 5px;
                padding: 10px;
                color: black;
                background-color: white;
            }
            QDateEdit::drop-down {
                border: none;
                color: black;
            }
            QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid darkgreen;
                margin-right: 10px;
            }
        """)
        self.data_input.setFixedHeight(40)
        form_layout.addWidget(self.data_input)

        # Layout horizontal para Gênero e Telefone
        genero_telefone_layout = QHBoxLayout()
        genero_telefone_layout.setSpacing(20)

        # Coluna do Gênero
        genero_column = QVBoxLayout()

        self.genero_label = QLabel("Gênero:")
        self.genero_label.setFont(QFont("Arial", 10))
        genero_column.addWidget(self.genero_label)

        self.genero_input = QComboBox()
        self.genero_input.addItems(["Selecione...", "Masculino", "Feminino", "Outro"])

        # Define o gênero atual
        genero_atual = paciente_data.get('genero', '')
        if genero_atual in ["Masculino", "Feminino", "Outro"]:
            self.genero_input.setCurrentText(genero_atual)

        self.genero_input.setStyleSheet("""
            QComboBox {
                border: 2px solid darkgreen;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid darkgreen;
                margin-right: 10px;
            }
        """)
        self.genero_input.setFixedHeight(40)
        genero_column.addWidget(self.genero_input)

        # Coluna do Telefone
        telefone_column = QVBoxLayout()

        self.telefone_label = QLabel("Telefone:")
        self.telefone_label.setFont(QFont("Arial", 10))
        telefone_column.addWidget(self.telefone_label)

        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("(11) 99999-9999")
        self.telefone_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.telefone_input.setFixedHeight(40)
        self.telefone_input.setText(paciente_data.get('telefone', ''))
        telefone_column.addWidget(self.telefone_input)

        # Adiciona as colunas ao layout horizontal
        genero_telefone_layout.addLayout(genero_column)
        genero_telefone_layout.addLayout(telefone_column)

        # Adiciona o layout horizontal ao formulário
        form_layout.addLayout(genero_telefone_layout)

        # Layout para botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Botão de Salvar Alterações
        self.salvar_button = QPushButton("Salvar Alterações")
        self.salvar_button.setStyleSheet(
            "background-color: darkgreen; color: white;margin-top:30px; border-radius:5px")
        self.salvar_button.setFixedHeight(70)
        self.salvar_button.setFixedWidth(200)
        self.salvar_button.clicked.connect(self.handle_salvar)
        buttons_layout.addWidget(self.salvar_button)

        # Botão de Excluir Paciente
        self.excluir_button = QPushButton("Excluir Paciente")
        self.excluir_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545; 
                color: white;
                margin-top:30px; 
                border-radius:5px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.excluir_button.setFixedHeight(70)
        self.excluir_button.setFixedWidth(200)
        self.excluir_button.clicked.connect(self.handle_excluir)
        buttons_layout.addWidget(self.excluir_button)

        form_layout.addLayout(buttons_layout)

        # Ajuste do formulário
        form_widget.setFixedHeight(500)
        form_widget.setFixedWidth(500)
        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)

    def validar_telefone(self, telefone):
        """Valida formato básico do telefone"""
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'[^\d]', '', telefone)

        # Verifica se tem 10 ou 11 dígitos (celular ou fixo)
        if len(telefone_limpo) in [10, 11]:
            return telefone_limpo
        return None

    def atualizar_paciente(self, paciente_id, nome, data_nascimento, genero, telefone):
        """Atualiza um paciente no banco de dados"""
        conexao = None
        cursor = None

        try:
            if not db.usuario_logado:
                raise Exception("Usuário não está logado")

            conexao = conectar()
            cursor = conexao.cursor()

            query = """UPDATE pacientes 
                       SET nome = %s, data_nascimento = %s, genero = %s, telefone = %s 
                       WHERE id = %s AND usuario_id = %s"""

            cursor.execute(query, (nome, data_nascimento, genero, telefone, paciente_id, db.usuario_logado['id']))

            if cursor.rowcount == 0:
                raise Exception("Paciente não encontrado ou não pertence ao usuário")

            return True

        except Exception as e:
            print(f"Erro ao atualizar paciente: {e}")
            raise e

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def excluir_paciente(self, paciente_id):
        """Exclui um paciente do banco de dados"""
        conexao = None
        cursor = None

        try:
            if not db.usuario_logado:
                raise Exception("Usuário não está logado")

            conexao = conectar()
            cursor = conexao.cursor()

            query = "DELETE FROM pacientes WHERE id = %s AND usuario_id = %s"
            cursor.execute(query, (paciente_id, db.usuario_logado['id']))

            if cursor.rowcount == 0:
                raise Exception("Paciente não encontrado ou não pertence ao usuário")

            return True

        except Exception as e:
            print(f"Erro ao excluir paciente: {e}")
            raise e

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def handle_salvar(self):
        try:
            nome = self.nome_input.text().strip()
            data_nascimento = self.data_input.date().toString("yyyy-MM-dd")
            genero = self.genero_input.currentText()
            telefone = self.telefone_input.text().strip()

            # Validações
            if not nome:
                QMessageBox.warning(self, "Erro", "Por favor, digite o nome do paciente!")
                return

            if len(nome) < 2:
                QMessageBox.warning(self, "Erro", "Nome deve ter pelo menos 2 caracteres!")
                return

            if genero == "Selecione...":
                QMessageBox.warning(self, "Erro", "Por favor, selecione o gênero!")
                return

            if telefone:
                telefone_validado = self.validar_telefone(telefone)
                if not telefone_validado:
                    QMessageBox.warning(self, "Erro", "Formato de telefone inválido!\nUse: (11) 99999-9999")
                    return
                telefone = telefone_validado

            # Verifica se a data não é no futuro
            if self.data_input.date() > QDate.currentDate():
                QMessageBox.warning(self, "Erro", "Data de nascimento não pode ser no futuro!")
                return

            # Atualiza o paciente
            self.atualizar_paciente(self.paciente_data['id'], nome, data_nascimento, genero, telefone)
            QMessageBox.information(self, "Sucesso", f"Paciente '{nome}' atualizado com sucesso!")

            # Registra o log
            try:
                Logger.registrar_acao(db.usuario_logado['id'], f"Editou paciente: {nome}")
            except Exception as log_error:
                print(f"Erro ao registrar log: {log_error}")

            # Volta para a home
            self.voltar_home()

        except Exception as e:
            print(f"Erro na atualização: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar paciente: {str(e)}")

    def handle_excluir(self):
        try:
            # Confirmação de exclusão
            reply = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o paciente '{self.paciente_data['nome']}'?\n\nEsta ação não pode ser desfeita.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Exclui o paciente
                self.excluir_paciente(self.paciente_data['id'])
                QMessageBox.information(self, "Sucesso",
                                        f"Paciente '{self.paciente_data['nome']}' excluído com sucesso!")

                # Registra o log
                try:
                    Logger.registrar_acao(db.usuario_logado['id'], f"Excluiu paciente: {self.paciente_data['nome']}")
                except Exception as log_error:
                    print(f"Erro ao registrar log: {log_error}")

                # Volta para a home
                self.voltar_home()

        except Exception as e:
            print(f"Erro na exclusão: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao excluir paciente: {str(e)}")

    def voltar_home(self):
        try:
            # Pega a posição atual da janela
            current_pos = self.pos()

            from telas.home import Home
            self.home_window = Home()
            self.home_window.move(current_pos)
            self.home_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao voltar para home: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Dados de exemplo para teste
    paciente_exemplo = {
        'id': 1,
        'nome': 'João Silva',
        'data_nascimento': '1990-05-15',
        'genero': 'Masculino',
        'telefone': '11999999999'
    }
    window = EdicaoPaciente(paciente_exemplo)
    window.show()
    sys.exit(app.exec_())