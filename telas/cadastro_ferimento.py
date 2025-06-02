from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QDateEdit, QTextEdit)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDate
import sys
from banco import criar_ferimento
from logger import Logger


class CadastroFerimento(QMainWindow):
    def __init__(self, paciente_data):
        super().__init__()

        self.paciente_data = paciente_data

        # Configurações da Janela
        self.setWindowTitle(f"Cadastro de Ferimento - {paciente_data['nome']} - BIO-CV")
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
        self.voltar_button.clicked.connect(self.voltar_lista)
        header_layout.addWidget(self.voltar_button)

        # Espaçador para empurrar o botão para a esquerda
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Formulário de Cadastro
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Título
        self.title_label = QLabel(f"Cadastrar Novo Ferimento")
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setContentsMargins(0, 0, 0, 20)
        form_layout.addWidget(self.title_label)

        # Subtítulo com nome do paciente
        self.subtitle_label = QLabel(f"Paciente: {paciente_data['nome']}")
        self.subtitle_label.setFont(QFont("Arial", 12))
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #666; margin-bottom: 20px;")
        form_layout.addWidget(self.subtitle_label)

        # Campo de Descrição
        self.descricao_label = QLabel("Descrição do ferimento:")
        self.descricao_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.descricao_label)

        self.descricao_input = QTextEdit()
        self.descricao_input.setPlaceholderText("Descreva detalhadamente o ferimento (tipo, características, causa, etc.)")
        self.descricao_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.descricao_input.setFixedHeight(80)
        form_layout.addWidget(self.descricao_input)

        # Layout horizontal para Data e Localização
        data_local_layout = QHBoxLayout()
        data_local_layout.setSpacing(20)

        # Coluna da Data
        data_column = QVBoxLayout()

        self.data_label = QLabel("Data do ferimento:")
        self.data_label.setFont(QFont("Arial", 10))
        data_column.addWidget(self.data_label)

        self.data_input = QDateEdit()
        self.data_input.setCalendarPopup(True)
        self.data_input.setDate(QDate.currentDate())  # Data padrão: hoje
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
        data_column.addWidget(self.data_input)

        # Coluna da Localização
        localizacao_column = QVBoxLayout()

        self.localizacao_label = QLabel("Localização no corpo:")
        self.localizacao_label.setFont(QFont("Arial", 10))
        localizacao_column.addWidget(self.localizacao_label)

        self.localizacao_input = QLineEdit()
        self.localizacao_input.setPlaceholderText("Ex: Braço direito, perna esquerda, tórax...")
        self.localizacao_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.localizacao_input.setFixedHeight(40)
        localizacao_column.addWidget(self.localizacao_input)

        # Adiciona as colunas ao layout horizontal
        data_local_layout.addLayout(data_column)
        data_local_layout.addLayout(localizacao_column)

        # Adiciona o layout horizontal ao formulário
        form_layout.addLayout(data_local_layout)

        # Botão de Cadastrar
        self.cadastrar_button = QPushButton("Cadastrar Ferimento")
        self.cadastrar_button.setStyleSheet(
            "background-color: darkgreen; color: white;margin-top:30px; border-radius:5px")
        self.cadastrar_button.setFixedHeight(70)
        self.cadastrar_button.setFixedWidth(300)
        self.cadastrar_button.clicked.connect(self.handle_cadastrar)
        form_layout.addWidget(self.cadastrar_button, alignment=Qt.AlignCenter)

        # Ajuste do formulário
        form_widget.setFixedHeight(500)
        form_widget.setFixedWidth(600)
        main_layout.addWidget(form_widget, alignment=Qt.AlignCenter)

    def handle_cadastrar(self):
        try:
            descricao = self.descricao_input.toPlainText().strip()
            data_ocorrencia = self.data_input.date().toString("yyyy-MM-dd")
            localizacao = self.localizacao_input.text().strip()

            # Validações
            if not descricao:
                QMessageBox.warning(self, "Erro", "Por favor, descreva o ferimento!")
                return

            if len(descricao) < 10:
                QMessageBox.warning(self, "Erro", "A descrição deve ter pelo menos 10 caracteres!")
                return

            if not localizacao:
                QMessageBox.warning(self, "Erro", "Por favor, informe a localização do ferimento!")
                return

            if len(localizacao) < 3:
                QMessageBox.warning(self, "Erro", "A localização deve ter pelo menos 3 caracteres!")
                return

            # Verifica se a data não é no futuro
            if self.data_input.date() > QDate.currentDate():
                QMessageBox.warning(self, "Erro", "A data do ferimento não pode ser no futuro!")
                return

            # Cria o ferimento
            ferimento = criar_ferimento(self.paciente_data['id'], descricao, data_ocorrencia, localizacao)
            QMessageBox.information(self, "Sucesso", "Ferimento cadastrado com sucesso!")

            # Registra o log
            try:
                from banco import db
                Logger.registrar_acao(db.usuario_logado['id'],
                                    f"Cadastrou ferimento para paciente: {self.paciente_data['nome']}")
            except Exception as log_error:
                print(f"Erro ao registrar log: {log_error}")

            # Volta para a lista de ferimentos
            self.voltar_lista()

        except Exception as e:
            print(f"Erro no cadastro: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao cadastrar ferimento: {str(e)}")

    def voltar_lista(self):
        try:
            # Pega a posição atual da janela
            current_pos = self.pos()

            from telas.lista_ferimentos import ListaFerimentos
            self.lista_window = ListaFerimentos(self.paciente_data)
            self.lista_window.move(current_pos)
            self.lista_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao voltar para lista: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Dados de exemplo para teste
    paciente_exemplo = {
        'id': 1,
        'nome': 'João Silva'
    }
    window = CadastroFerimento(paciente_exemplo)
    window.show()
    sys.exit(app.exec_())