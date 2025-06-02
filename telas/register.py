from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
from banco import criar_usuario
from decorators import log_action
import re

class Register(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.setWindowTitle("Registro de Usuário")
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)  # Define o tamanho fixo da janela

        # Adiciona ícone da janela
        self.setWindowIcon(QIcon("../assets/Icon.png"))

        # Layout Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)



        # Formulário de Cadastro
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(0, 0, 0, 0)  # Move o formulário para cima (margem superior negativa)

        # Título
        self.title_label = QLabel("Insira seus dados para se cadastrar no BIO-CV")
        self.title_label.setFont(QFont("Arial", 14))
        self.title_label.setAlignment(Qt.AlignCenter)  # Centraliza o texto
        self.title_label.setContentsMargins(0, 0, 0, 20)
        form_layout.addWidget(self.title_label)
        #setContentsMargins(0, 0, 0, 0)  # Remove margens externas

        # Campo de Nome de Usuário
        self.username_label = QLabel("Nome de Usuário:")
        self.username_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nome de Usuário")
        self.username_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.username_input.setFixedHeight(50)
        form_layout.addWidget(self.username_input)

        # Campo de Senha
        self.password_label = QLabel("Senha:")
        self.password_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.password_input.setFixedHeight(50)
        form_layout.addWidget(self.password_input)

        # Campo de E-mail
        self.email_label = QLabel("E-mail:")
        self.email_label.setFont(QFont("Arial", 10))
        form_layout.addWidget(self.email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        self.email_input.setStyleSheet("border: 2px solid darkgreen;border-radius:5px;padding:10;")
        self.email_input.setFixedHeight(50)
        form_layout.addWidget(self.email_input)

        # Layout para Botões e Label "ou"
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(10)

        # Botão de Registro (estilizado como o de login)
        self.register_button = QPushButton("Cadastro")
        self.register_button.setStyleSheet("background-color: darkgreen; color: white;margin-top:30px; border-radius:5px")
        self.register_button.setFixedHeight(80)
        self.register_button.setFixedWidth(450)
        self.register_button.clicked.connect(self.handle_register)
        button_layout.addWidget(self.register_button)

        # Texto de Ou
        self.or_label = QLabel("ou")
        self.or_label.setFont(QFont("Arial", 10))
        self.or_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.or_label)

        # Botão "Voltar para Login"
        self.back_button = QPushButton("Login")
        self.back_button.setStyleSheet("border: 2px solid darkgreen; color: darkgreen;border-radius:5px")
        self.back_button.setFixedHeight(50)
        self.back_button.setFixedWidth(450)
        self.back_button.clicked.connect(self.go_to_login)
        button_layout.addWidget(self.back_button)

        # Adiciona o layout de botões e label ao layout principal
        form_layout.addLayout(button_layout)

        # Ajuste da altura do form_widget para 70% da altura da janela
        form_widget.setFixedHeight(600)
        form_widget.setFixedWidth(500)
        layout.addWidget(form_widget, alignment=Qt.AlignCenter)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()

        # Regex para validação de e-mail
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if username and password and email:
            if not re.match(email_regex, email):
                QMessageBox.warning(self, "Erro", "Por favor, insira um e-mail válido!")
                return

            try:
                usuario = criar_usuario(username, password, email)
                QMessageBox.information(self, "Sucesso", "Usuário cadastrado com sucesso!")
                log_action(usuario['id'], "Usuario realizou cadastro")(lambda: None)()

                from telas.home import Home
                self.home = Home()
                self.home.show()

                self.close()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Ocorreu um erro ao cadastrar o usuário: {str(e)}")
        else:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos!")

    def go_to_login(self):
        from telas.login import Login
        self.login_window = Login()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Register()
    window.show()
    sys.exit(app.exec_())
