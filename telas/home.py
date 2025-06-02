from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
from banco import db


class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.setWindowTitle('Home')
        self.setGeometry(100, 100, 1000, 600)
        self.setFixedSize(1000, 600)

        # Adiciona ícone da janela
        self.setWindowIcon(QIcon("../assets/Icon.png"))

        # Layout Principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Título
        self.title_label = QLabel("Bem-vindo à Home!")
        self.title_label.setFont(QFont("Arial", 18))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.setContentsMargins(0, 20, 0, 20)  # Margens

        # Informações do Usuário
        self.user_info_label = QLabel(self.get_user_info())
        self.user_info_label.setFont(QFont("Arial", 14))
        self.user_info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.user_info_label)

        # Botão de Logout
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("background-color: darkgreen; color: white; border-radius: 5px;")
        self.logout_button.setFixedHeight(50)
        self.logout_button.setFixedWidth(200)
        self.logout_button.clicked.connect(self.handle_logout)
        layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)

    def get_user_info(self):
        # Obtém as informações do usuário logado do módulo db
        usuario = db.usuario_logado
        if usuario:
            return f"Usuário Logado: {usuario['name']} ({usuario['email']})"
        return "Nenhum usuário logado."

    def handle_logout(self):
        # Fecha a tela atual e retorna para a tela de login
        self.close()
        from login import Login
        self.login_window = Login()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())
