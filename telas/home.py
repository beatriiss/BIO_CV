from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
                             QApplication, QLineEdit, QScrollArea, QHBoxLayout, QFrame, QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
import sys
from banco import db


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.setWindowTitle('BIO-CV - Análise de Ferimentos')
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
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Header com título e logout
        header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Análise Automatizada de Ferimentos Cutâneos por Imagem")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(self.title_label)

        # Botão de Logout (discreto no canto)
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("""
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
        self.logout_button.setFixedSize(80, 35)
        self.logout_button.clicked.connect(self.handle_logout)
        header_layout.addWidget(self.logout_button)

        layout.addLayout(header_layout)

        # Subtítulo
        self.subtitle_label = QLabel("Esses são os seus pacientes:")
        self.subtitle_label.setFont(QFont("Arial", 14))
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.subtitle_label)

        # Campo de busca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar paciente...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid darkgreen;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.search_input.setFixedHeight(45)

        # Busca local simples
        self.search_input.textChanged.connect(self.filtrar_pacientes)
        layout.addWidget(self.search_input)

        # Lista de todos os pacientes (carregada uma vez)
        self.todos_pacientes = []

        # Área de scroll para lista de pacientes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        self.pacientes_widget = QWidget()
        self.pacientes_layout = QVBoxLayout(self.pacientes_widget)
        self.pacientes_layout.setSpacing(10)

        self.scroll_area.setWidget(self.pacientes_widget)
        layout.addWidget(self.scroll_area)

        # Botão de cadastrar novo paciente
        self.new_patient_button = QPushButton("Cadastrar novo paciente")
        self.new_patient_button.setStyleSheet("""
            QPushButton {
                background-color: darkgreen; 
                color: white;
                border-radius: 5px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006400;
            }
        """)
        self.new_patient_button.setFixedHeight(50)
        self.new_patient_button.clicked.connect(self.open_cadastro_paciente)
        layout.addWidget(self.new_patient_button)

        # Carrega a lista inicial de pacientes
        self.carregar_pacientes()

    def atualizar_lista(self):
        """Atualiza a lista de pacientes (útil quando volta do cadastro)"""
        try:
            self.search_input.clear()  # Limpa a busca
            self.carregar_pacientes()  # Recarrega do banco
        except Exception as e:
            print(f"Erro ao atualizar lista: {e}")

    def criar_item_paciente(self, paciente):
        """Cria um item visual para cada paciente"""
        # Frame para o paciente
        paciente_frame = QFrame()
        paciente_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        paciente_frame.setFixedHeight(60)

        # Layout horizontal para o item
        item_layout = QHBoxLayout(paciente_frame)
        item_layout.setContentsMargins(15, 10, 15, 10)

        # Nome do paciente
        nome_label = QLabel(paciente['nome'])
        nome_label.setFont(QFont("Arial", 12))
        nome_label.setStyleSheet("color: #333; border: none;")
        item_layout.addWidget(nome_label)

        # Espaçador
        item_layout.addStretch()

        # Botão de editar
        editar_button = QPushButton("✏️ Editar")
        editar_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        editar_button.clicked.connect(lambda: self.abrir_edicao(paciente))
        item_layout.addWidget(editar_button)

        # Botão de análises
        analises_button = QPushButton("Ferimentos")
        analises_button.setStyleSheet("""
            QPushButton {
                background-color: darkgreen;
                color: white;
                border-radius: 5px;
                padding: 8px 20px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #006400;
            }
        """)
        analises_button.clicked.connect(lambda: self.abrir_analises(paciente))
        item_layout.addWidget(analises_button)

        return paciente_frame

    def carregar_pacientes(self):
        """Carrega todos os pacientes do banco UMA VEZ"""
        try:
            self.todos_pacientes = db.listar_pacientes()
            self.exibir_pacientes(self.todos_pacientes)
        except Exception as e:
            print(f"Erro ao carregar pacientes: {e}")
            self.todos_pacientes = []
            self.exibir_pacientes([])

    def exibir_pacientes(self, pacientes):
        """Exibe a lista de pacientes na tela"""
        try:
            # Limpa a lista atual de forma mais segura
            while self.pacientes_layout.count():
                child = self.pacientes_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Se não há pacientes, mostra mensagem
            if not pacientes:
                mensagem = "Nenhum paciente cadastrado ainda." if not self.todos_pacientes else "Nenhum paciente encontrado."
                no_patients_label = QLabel(mensagem)
                no_patients_label.setFont(QFont("Arial", 12))
                no_patients_label.setAlignment(Qt.AlignCenter)
                no_patients_label.setStyleSheet("color: #666; padding: 20px;")
                self.pacientes_layout.addWidget(no_patients_label)
            else:
                # Adiciona cada paciente à lista
                for paciente in pacientes:
                    try:
                        item = self.criar_item_paciente(paciente)
                        self.pacientes_layout.addWidget(item)
                    except Exception as e:
                        print(f"Erro ao criar item do paciente {paciente.get('nome', 'desconhecido')}: {e}")

            # Adiciona espaçador no final
            self.pacientes_layout.addStretch()

        except Exception as e:
            print(f"Erro ao exibir pacientes: {e}")

    def filtrar_pacientes(self):
        """Filtra os pacientes que já estão carregados"""
        try:
            termo = self.search_input.text().strip().lower()

            if not termo:
                # Se campo vazio, mostra todos
                pacientes_para_exibir = self.todos_pacientes[:]  # Cria cópia da lista
            else:
                # Filtra na lista que já está na memória
                pacientes_para_exibir = []
                for paciente in self.todos_pacientes:
                    try:
                        if termo in paciente['nome'].lower():
                            pacientes_para_exibir.append(paciente)
                    except (KeyError, AttributeError, TypeError):
                        continue  # Ignora pacientes com dados inválidos

            self.exibir_pacientes(pacientes_para_exibir)

        except Exception as e:
            print(f"Erro na filtragem: {e}")

    def abrir_edicao(self, paciente):
        """Abre a tela de edição do paciente"""
        try:
            current_pos = self.pos()

            from telas.edicao_paciente import EdicaoPaciente
            self.edicao_window = EdicaoPaciente(paciente)
            self.edicao_window.move(current_pos)
            self.edicao_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir edição de paciente: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir edição: {str(e)}")

    # Substituir o método abrir_analises na telas/home.py (linha 183)

    def abrir_analises(self, paciente):
        """Abre a lista de ferimentos do paciente"""
        try:
            current_pos = self.pos()

            from telas.lista_ferimentos import ListaFerimentos
            self.ferimentos_window = ListaFerimentos(paciente)
            self.ferimentos_window.move(current_pos)
            self.ferimentos_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir ferimentos: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir ferimentos: {str(e)}")

    def open_cadastro_paciente(self):
        """Abre a tela de cadastro de paciente"""
        try:
            current_pos = self.pos()

            from telas.cadastro_paciente import CadastroPaciente
            self.cadastro_window = CadastroPaciente()
            self.cadastro_window.move(current_pos)
            self.cadastro_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir cadastro de paciente: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir cadastro: {str(e)}")

    def handle_logout(self):
        try:
            # Limpa o usuário logado
            db.usuario_logado = None

            # Pega a posição atual da janela
            current_pos = self.pos()

            # Volta para a tela de login
            self.close()
            from telas.login import Login
            self.login_window = Login()
            self.login_window.move(current_pos)
            self.login_window.show()
        except Exception as e:
            print(f"Erro no logout: {e}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())