import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from banco import db
from telas.home import Home
from telas.register import Register
from logger import Logger


class Login(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.setWindowTitle("BIO-CV")
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)

        # Tenta carregar ícone (sem quebrar se não encontrar)
        try:
            pixmap = QPixmap("assets/Icon.png")  # Caminho corrigido
            if not pixmap.isNull():
                pixmap = pixmap.scaled(64, 64, aspectRatioMode=Qt.KeepAspectRatio,
                                       transformMode=Qt.SmoothTransformation)
                self.setWindowIcon(QIcon(pixmap))
        except:
            pass  # Ignora se não conseguir carregar o ícone

        # Layout Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Formulário de Login
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(0, -140, 0, 0)

        # Título
        self.title_label = QLabel("Insira seus dados para realizar login do BIO-CV")
        self.title_label.setFont(QFont("Arial", 14))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setContentsMargins(0, 0, 0, 20)
        form_layout.addWidget(self.title_label)

        # Campo de E-mail
        self.email_label = QLabel("Insira seu e-mail:")
        self.email_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.email_input.setFixedHeight(50)
        form_layout.addWidget(self.email_input)

        # Campo de Senha
        self.password_label = QLabel("Insira sua senha:")
        self.password_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.password_input.setFixedHeight(50)
        form_layout.addWidget(self.password_input)

        # Layout para Botões
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(10)

        # Botão de Login
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: darkgreen; color: white;margin-top:30px; border-radius:5px")
        self.login_button.setFixedHeight(80)
        self.login_button.setFixedWidth(450)
        self.login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_button)

        # Texto "ou"
        self.or_label = QLabel("ou")
        self.or_label.setFont(QFont("Arial", 10))
        self.or_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.or_label)

        # Botão de Cadastro
        self.register_button = QPushButton("Cadastro")
        self.register_button.setStyleSheet("border: 2px solid darkgreen; color: darkgreen;border-radius:5px")
        self.register_button.setFixedHeight(50)
        self.register_button.setFixedWidth(450)
        self.register_button.clicked.connect(self.open_register)
        button_layout.addWidget(self.register_button)

        form_layout.addLayout(button_layout)

        # Ajuste do formulário
        form_widget.setFixedHeight(500)
        form_widget.setFixedWidth(500)
        layout.addWidget(form_widget, alignment=Qt.AlignCenter)

    def handle_login(self):
        try:
            email = self.email_input.text()
            password = self.password_input.text()

            # Valida se os campos foram preenchidos
            if not email or not password:
                QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos!")
                return

            # Verifica se o usuário existe
            usuario = db.verificar_usuario(email, password)

            if usuario:
                QMessageBox.information(self, "Login bem-sucedido", "Você fez login com sucesso!")

                # Registra o log
                try:
                    Logger.registrar_acao(usuario['id'], "Usuário fez login")
                except Exception as log_error:
                    print(f"Erro ao registrar log: {log_error}")

                self.open_home()
            else:
                QMessageBox.warning(self, "Erro", "E-mail ou senha incorretos. Tente novamente.")

        except Exception as e:
            print(f"Erro no login: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao fazer login: {str(e)}")

    def open_home(self):
        try:
            # Pega a posição atual da janela
            current_pos = self.pos()

            self.home = Home()
            # Define a nova janela na mesma posição
            self.home.move(current_pos)
            self.home.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir home: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir tela principal: {str(e)}")

    def open_register(self):
        try:
            # Pega a posição atual da janela
            current_pos = self.pos()

            self.cadastro_window = Register()
            # Define a nova janela na mesma posição
            self.cadastro_window.move(current_pos)
            self.cadastro_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir register: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir tela de cadastro: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())