from PyQt5.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
                             QApplication, QLineEdit, QScrollArea, QHBoxLayout, QFrame, QMessageBox)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
from banco import listar_ferimentos, buscar_ferimentos
from datetime import datetime


class ListaFerimentos(QMainWindow):
    def __init__(self, paciente_data):
        super().__init__()

        self.paciente_data = paciente_data

        # Configurações da Janela
        self.setWindowTitle(f'Ferimentos - {paciente_data["nome"]} - BIO-CV')
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

        layout.addLayout(header_layout)

        # Título
        self.title_label = QLabel(f"Ferimentos de {paciente_data['nome']}")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Campo de busca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar ferimento por descrição ou localização...")
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
        self.search_input.textChanged.connect(self.filtrar_ferimentos)
        layout.addWidget(self.search_input)

        # Lista de todos os ferimentos (carregada uma vez)
        self.todos_ferimentos = []

        # Área de scroll para lista de ferimentos
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        self.ferimentos_widget = QWidget()
        self.ferimentos_layout = QVBoxLayout(self.ferimentos_widget)
        self.ferimentos_layout.setSpacing(10)

        self.scroll_area.setWidget(self.ferimentos_widget)
        layout.addWidget(self.scroll_area)

        # Botão de cadastrar novo ferimento
        self.new_ferimento_button = QPushButton("Cadastrar novo ferimento")
        self.new_ferimento_button.setStyleSheet("""
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
        self.new_ferimento_button.setFixedHeight(50)
        self.new_ferimento_button.clicked.connect(self.open_cadastro_ferimento)
        layout.addWidget(self.new_ferimento_button)

        # Carrega a lista inicial de ferimentos
        self.carregar_ferimentos()

    def formatar_data(self, data):
        """Formata a data para exibição"""
        try:
            if isinstance(data, str):
                # Se for string no formato YYYY-MM-DD, converte para DD/MM/YYYY
                if len(data) == 10 and data.count('-') == 2:
                    ano, mes, dia = data.split('-')
                    return f"{dia}/{mes}/{ano}"
            elif hasattr(data, 'strftime'):
                # Se for objeto date/datetime
                return data.strftime("%d/%m/%Y")
            return str(data)
        except:
            return str(data)

    def atualizar_lista(self):
        """Atualiza a lista de ferimentos (útil quando volta do cadastro)"""
        try:
            self.search_input.clear()  # Limpa a busca
            self.carregar_ferimentos()  # Recarrega do banco
        except Exception as e:
            print(f"Erro ao atualizar lista: {e}")

    def criar_item_ferimento(self, ferimento):
        """Cria um item visual para cada ferimento"""
        # Frame para o ferimento
        ferimento_frame = QFrame()
        ferimento_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 2px;
            }
        """)
        ferimento_frame.setFixedHeight(100)  # Aumentei para 100px

        # Layout vertical para o item
        item_layout = QVBoxLayout(ferimento_frame)
        item_layout.setContentsMargins(15, 15, 15, 15)  # Margens maiores
        item_layout.setSpacing(10)  # Mais espaçamento entre elementos

        # Layout superior com descrição e botões
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignVCenter)  # Alinha verticalmente ao centro

        # Descrição do ferimento (limitada)
        descricao = ferimento['descricao'][:40] + "..." if len(ferimento['descricao']) > 40 else ferimento['descricao']
        descricao_label = QLabel(f"📋 {descricao}")
        descricao_label.setFont(QFont("Arial", 12, QFont.Bold))
        descricao_label.setStyleSheet("color: #333; border: none;")
        descricao_label.setWordWrap(False)
        top_layout.addWidget(descricao_label)

        # Espaçador
        top_layout.addStretch()

        # Botão de análises (NOVO)
        analises_button = QPushButton("🔬 Análises")
        analises_button.setStyleSheet("""
            QPushButton {
                background-color: darkgreen;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006400;
            }
        """)
        analises_button.setFixedSize(90, 30)
        analises_button.clicked.connect(lambda: self.abrir_analises(ferimento))
        top_layout.addWidget(analises_button)

        # Botão de editar
        editar_button = QPushButton("✏️ Editar")
        editar_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        editar_button.setFixedSize(80, 30)  # Tamanho fixo maior
        editar_button.clicked.connect(lambda: self.abrir_edicao(ferimento))
        top_layout.addWidget(editar_button)

        # Botão de excluir
        excluir_button = QPushButton("🗑️")
        excluir_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        excluir_button.setFixedSize(35, 30)  # Tamanho fixo maior
        excluir_button.clicked.connect(lambda: self.confirmar_exclusao(ferimento))
        top_layout.addWidget(excluir_button)

        item_layout.addLayout(top_layout)

        # Layout inferior com detalhes
        bottom_layout = QHBoxLayout()

        # Localização e data
        localizacao_data = f"📍 {ferimento['localizacao']} • 📅 {self.formatar_data(ferimento['data_ocorrencia'])}"
        detalhes_label = QLabel(localizacao_data)
        detalhes_label.setFont(QFont("Arial", 10))
        detalhes_label.setStyleSheet("color: #666; border: none;")
        bottom_layout.addWidget(detalhes_label)

        bottom_layout.addStretch()

        item_layout.addLayout(bottom_layout)

        return ferimento_frame

    def abrir_analises(self, ferimento):
        """Abre as análises do ferimento (por enquanto só mensagem)"""
        QMessageBox.information(
            self,
            "Análises de Ferimento",
            f"Funcionalidade em desenvolvimento!\n\nFerimento: {ferimento['descricao'][:30]}...\nLocalização: {ferimento['localizacao']}\nData: {self.formatar_data(ferimento['data_ocorrencia'])}"
        )

    def carregar_ferimentos(self):
        """Carrega todos os ferimentos do banco UMA VEZ"""
        try:
            self.todos_ferimentos = listar_ferimentos(self.paciente_data['id'])
            self.exibir_ferimentos(self.todos_ferimentos)
        except Exception as e:
            print(f"Erro ao carregar ferimentos: {e}")
            self.todos_ferimentos = []
            self.exibir_ferimentos([])

    def exibir_ferimentos(self, ferimentos):
        """Exibe a lista de ferimentos na tela"""
        try:
            # Limpa a lista atual de forma mais segura
            while self.ferimentos_layout.count():
                child = self.ferimentos_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Se não há ferimentos, mostra mensagem
            if not ferimentos:
                mensagem = "Nenhum ferimento cadastrado ainda." if not self.todos_ferimentos else "Nenhum ferimento encontrado."
                no_ferimentos_label = QLabel(mensagem)
                no_ferimentos_label.setFont(QFont("Arial", 12))
                no_ferimentos_label.setAlignment(Qt.AlignCenter)
                no_ferimentos_label.setStyleSheet("color: #666; padding: 20px;")
                self.ferimentos_layout.addWidget(no_ferimentos_label)
            else:
                # Adiciona cada ferimento à lista
                for ferimento in ferimentos:
                    try:
                        item = self.criar_item_ferimento(ferimento)
                        self.ferimentos_layout.addWidget(item)
                    except Exception as e:
                        print(f"Erro ao criar item do ferimento {ferimento.get('id', 'desconhecido')}: {e}")

            # Adiciona espaçador no final
            self.ferimentos_layout.addStretch()

        except Exception as e:
            print(f"Erro ao exibir ferimentos: {e}")

    def filtrar_ferimentos(self):
        """Filtra os ferimentos que já estão carregados"""
        try:
            termo = self.search_input.text().strip().lower()

            if not termo:
                # Se campo vazio, mostra todos
                ferimentos_para_exibir = self.todos_ferimentos[:]  # Cria cópia da lista
            else:
                # Filtra na lista que já está na memória
                ferimentos_para_exibir = []
                for ferimento in self.todos_ferimentos:
                    try:
                        descricao = ferimento.get('descricao', '').lower()
                        localizacao = ferimento.get('localizacao', '').lower()
                        if termo in descricao or termo in localizacao:
                            ferimentos_para_exibir.append(ferimento)
                    except (AttributeError, TypeError):
                        continue  # Ignora ferimentos com dados inválidos

            self.exibir_ferimentos(ferimentos_para_exibir)

        except Exception as e:
            print(f"Erro na filtragem: {e}")

    def abrir_edicao(self, ferimento):
        """Abre a tela de edição do ferimento"""
        try:
            current_pos = self.pos()

            from telas.edicao_ferimento import EdicaoFerimento
            self.edicao_window = EdicaoFerimento(ferimento, self.paciente_data)
            self.edicao_window.move(current_pos)
            self.edicao_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir edição de ferimento: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir edição: {str(e)}")

    def confirmar_exclusao(self, ferimento):
        """Confirma e exclui um ferimento"""
        try:
            from banco import excluir_ferimento
            from logger import Logger

            # Confirmação de exclusão
            descricao_curta = ferimento['descricao'][:30] + "..." if len(ferimento['descricao']) > 30 else ferimento['descricao']
            reply = QMessageBox.question(
                self,
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o ferimento:\n\n'{descricao_curta}'\n\nEsta ação não pode ser desfeita.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Exclui o ferimento
                excluir_ferimento(ferimento['id'])
                QMessageBox.information(self, "Sucesso", "Ferimento excluído com sucesso!")

                # Registra o log
                try:
                    from banco import db
                    Logger.registrar_acao(db.usuario_logado['id'], f"Excluiu ferimento: {descricao_curta}")
                except Exception as log_error:
                    print(f"Erro ao registrar log: {log_error}")

                # Recarrega a lista
                self.atualizar_lista()

        except Exception as e:
            print(f"Erro na exclusão: {e}")
            QMessageBox.warning(self, "Erro", f"Erro ao excluir ferimento: {str(e)}")

    def open_cadastro_ferimento(self):
        """Abre a tela de cadastro de ferimento"""
        try:
            current_pos = self.pos()

            from telas.cadastro_ferimento import CadastroFerimento
            self.cadastro_window = CadastroFerimento(self.paciente_data)
            self.cadastro_window.move(current_pos)
            self.cadastro_window.show()
            self.close()
        except Exception as e:
            print(f"Erro ao abrir cadastro de ferimento: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao abrir cadastro: {str(e)}")

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
        'nome': 'João Silva'
    }
    window = ListaFerimentos(paciente_exemplo)
    window.show()
    sys.exit(app.exec_())