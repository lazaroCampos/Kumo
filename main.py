import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QWidget, QMessageBox)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

# AQUI ESTÁ A MÁGICA: Importamos a função que criamos no outro arquivo!
from api_clima import obter_clima

class KumoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Configurações Básicas da Janela
        self.setWindowTitle("Kumo - Clima")
        self.setGeometry(100, 100, 400, 500) # Posição X, Y, Largura, Altura
        self.setStyleSheet("background-color: #2C3E50;") # Cor de fundo (Azul escuro)

        # 2. Configurar a Interface (Layout)
        self.inicializar_ui()

    def inicializar_ui(self):
        # Widget central (onde tudo fica)
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Layout Vertical (empilha um item embaixo do outro)
        layout = QVBoxLayout()
        widget_central.setLayout(layout)

        # --- Título ---
        titulo = QLabel("Kumo ☁️")
        titulo.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # --- Campo de Entrada (Input) ---
        self.input_cidade = QLineEdit()
        self.input_cidade.setPlaceholderText("Digite a cidade (ex: Cruz Alta)")
        self.input_cidade.setStyleSheet("padding: 10px; font-size: 16px; background-color: white;")
        layout.addWidget(self.input_cidade)

        # --- Botão de Busca ---
        botao = QPushButton("Ver Clima")
        botao.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; 
                color: white; 
                font-size: 16px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        botao.clicked.connect(self.buscar_clima) # Conecta o clique à função
        layout.addWidget(botao)

        # --- Imagem do Clima ---
        self.label_imagem = QLabel()
        self.label_imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_imagem.setMinimumHeight(150) # Reserva espaço para a imagem
        layout.addWidget(self.label_imagem)

        # --- Temperatura ---
        self.label_temp = QLabel("--°C")
        self.label_temp.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        self.label_temp.setStyleSheet("color: white;")
        self.label_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_temp)

        # --- Descrição (ex: Céu Limpo) ---
        self.label_desc = QLabel("Aguardando busca...")
        self.label_desc.setFont(QFont("Arial", 14))
        self.label_desc.setStyleSheet("color: #ECF0F1;")
        self.label_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_desc)

        # Espaço vazio para empurrar tudo para cima
        layout.addStretch()

    def buscar_clima(self):
        # 1. Pega o texto que o usuário digitou
        cidade = self.input_cidade.text()

        if not cidade:
            return # Se estiver vazio, não faz nada

        # 2. CHAMA O NOSSO MOTOR (api_clima.py)
        self.label_desc.setText("Buscando...")
        QApplication.processEvents() # Atualiza a tela para não travar
        
        dados = obter_clima(cidade)

        # 3. Atualiza a tela com a resposta
        if dados["sucesso"]:
            # Arredonda a temperatura (Dica de UX que falamos antes!)
            temp = int(dados['temperatura']) 
            
            self.label_temp.setText(f"{temp}°C")
            self.label_desc.setText(dados['descricao'].capitalize())
            
            # Chama a função que escolhe a imagem
            self.atualizar_imagem(dados['icone_id'])
        else:
            self.label_desc.setText(f"Erro: {dados['erro']}")

    def atualizar_imagem(self, icone_id):
        # Esta é a lógica que VOCÊ ajudou a construir!
        caminho_imagem = "assets/nuvem.png" # Padrão

        # Sol (01d/n)
        if "01" in icone_id:
            caminho_imagem = "assets/sol.png"
        
        # Nuvens (03 ou 04) - A lógica que adicionamos
        elif "03" in icone_id or "04" in icone_id:
            caminho_imagem = "assets/nuvem.png"
            
        # Chuva (09, 10, 11)
        elif "09" in icone_id or "10" in icone_id or "11" in icone_id:
            caminho_imagem = "assets/chuva.png"

        # Carrega a imagem na tela
        pixmap = QPixmap(caminho_imagem)
        
        # Verifica se a imagem carregou (para não crashar se faltar arquivo)
        if not pixmap.isNull():
            self.label_imagem.setPixmap(pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.label_desc.setText(f"{self.label_desc.text()} (Img não encontrada)")

# Bloco padrão para iniciar o App
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = KumoApp()
    janela.show()
    sys.exit(app.exec())