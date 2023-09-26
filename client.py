# Importações
import socket
import threading
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSignal, QTimer
import random
from PyQt5.QtWidgets import QPushButton




# Hash de identificação do client para identificar o client
hash = str(random.getrandbits(128))

# Classe padrão do PYQT para adicionar o design e as funções
class Ui_MainWindow(QtCore.QObject):

    # Dependencias do Signal (Signal é utilizado para fazer alterações em tempo real sem dar erro)
    update_chat_text_signal = QtCore.pyqtSignal(str)
    video_url_signal = pyqtSignal(str)


    def __init__(self):
        super().__init__()

        # Dependencias do Signal (Signal é utilizado para fazer alterações em tempo real sem dar erro)
        self.update_chat_text_signal.connect(self.display_message)
        self.video_url_signal.connect(self.update_video_url)

        # Threads feito por timer executador em tempo em tempo (para listar e obter alterações em eventos que ocorrerem)
        self.check_position_timer = QTimer(self)
        self.check_position_timer.timeout.connect(self.check_position)
        self.check_position_timer.start(1000)

        self.check_pause_timer = QTimer(self)
        self.check_pause_timer.timeout.connect(self.check_pause)
        self.check_pause_timer.start(500)

        self.listen_thread = threading.Thread(target=self.listen_to_server)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        # Variaveis Globais
        self.old_new_position = 0
        self.resultad = False
        self.pausedold = None
        self.logado = False    
        global conectado
        conectado = False

    # Função de design do PYQT
    def setupUi(self, MainWindow):

        # Fonte padrão
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)

# Estutura do programa - Inicio

        # Define a estrutura do programa
        MainWindow.installEventFilter(self)
        MainWindow.setStyleSheet("QMainWindow { background-color: rgb(40, 44, 52); }") # Cor da background do programa
        MainWindow.setFixedSize(1077, 500) # Tamanho do programa
        MainWindow.resize(1077, 530)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint) # Tira as bordas do progrma
        MainWindow.setObjectName("MainWindow")

        # Define a widge central
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

# Estutura do programa - Fim

# ----------------------------------------

# Estruturas de Frame - Inicio

        # Define o frame onde ficarão os componentes
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Define a segunda frame (Frame do chat)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(750, 20, 841, 491))
        self.frame_2.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Define a terceira frame (Frame para adicionar o usuario ao chat)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(750, 20, 841, 491))
        self.frame_3.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")

        # Define a quarta frame (Frame para adicionar o IP ao chat)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setGeometry(QtCore.QRect(750, 20, 841, 491))
        self.frame_4.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")

# Estruturas de Frame - Fim

# ----------------------------------------

# Estruturas de Botões do programa - Inicio

        # Botão de minimizar para o programa
        self.minimize_button = QPushButton(self.frame)
        self.minimize_button.setGeometry(QtCore.QRect(1000, 0, 21, 21))
        self.minimize_button.setText("➖")
        self.minimize_button.setStyleSheet("QPushButton { border: none; font-size: 16px; color: white; font-size: 16px; font-family: fantasy; }")
        self.minimize_button.clicked.connect(MainWindow.showMinimized)  # Minimiza a main quando é clicado

        # Botão de sair do programa
        self.exit_button = QtWidgets.QPushButton(self.frame)
        self.exit_button.setGeometry(QtCore.QRect(1030, 0, 21, 21))
        self.exit_button.setText("❌")  # Set the label to "X"
        self.exit_button.setStyleSheet("QPushButton { border: none; font-size: 16px; color: white; font-size: 16px; font-family: fantasy; }")
        self.exit_button.clicked.connect(self.exit_application) # Fecha o programa quando clicado

# Estruturas de Botões do programa - Fim



# Estrutura de IP - Inicio


        # Chat de texto para escrever o nome do usuario
        self.SendText3 = QtWidgets.QTextEdit(self.frame_4)
        self.SendText3.setGeometry(QtCore.QRect(10, 400, 281, 21))
        self.SendText3.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.SendText3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SendText3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SendText3.setObjectName("SendText")
        self.SendText3.setStyleSheet("background-color: rgb(40, 44, 52); color: white; font-size: 14px;")



        # Botão para adicionar o nome do ip
        self.SyncButton3 = QtWidgets.QPushButton(self.frame_4)
        self.SyncButton3.setGeometry(QtCore.QRect(10, 430, 281, 23))
        self.SyncButton3.setFont(font)

        # Css do botão
        self.SyncButton3.setStyleSheet("QPushButton {\n"
                                      "    border: 2px solid rgb(52, 59, 72);\n"
                                      "    border-radius: 5px;    \n"
                                      "    background-color: rgb(52, 59, 72);\n"
                                      "    color: white; /* Add this line to set the text color to white */\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(57, 65, 80);\n"
                                      "    border: 2px solid rgb(61, 70, 86);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed {    \n"
                                      "    background-color: rgb(35, 40, 49);\n"
                                      "    border: 2px solid rgb(43, 50, 61);\n"
                                      "}\n"
                                      "")
        self.SyncButton3.setObjectName("SyncButton")

        # Completa a conexao ao servidor
        self.SyncButton3.clicked.connect(self.addIp)

# Estrutura de IP - Fim


# Estrutura de Usuario - Inicio


        # Chat de texto para escrever o nome do usuario
        self.SendText2 = QtWidgets.QTextEdit(self.frame_3)
        self.SendText2.setGeometry(QtCore.QRect(10, 400, 281, 21))
        self.SendText2.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.SendText2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SendText2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SendText2.setObjectName("SendText")
        self.SendText2.setStyleSheet("background-color: rgb(40, 44, 52); color: white; font-size: 14px;")



        # Botão para adicionar o nome do usuario ao chat
        self.SyncButton2 = QtWidgets.QPushButton(self.frame_3)
        self.SyncButton2.setGeometry(QtCore.QRect(10, 430, 281, 23))
        self.SyncButton2.setFont(font)

        # Css do botão chat
        self.SyncButton2.setStyleSheet("QPushButton {\n"
                                      "    border: 2px solid rgb(52, 59, 72);\n"
                                      "    border-radius: 5px;    \n"
                                      "    background-color: rgb(52, 59, 72);\n"
                                      "    color: white; /* Add this line to set the text color to white */\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(57, 65, 80);\n"
                                      "    border: 2px solid rgb(61, 70, 86);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:pressed {    \n"
                                      "    background-color: rgb(35, 40, 49);\n"
                                      "    border: 2px solid rgb(43, 50, 61);\n"
                                      "}\n"
                                      "")
        self.SyncButton2.setObjectName("SyncButton")

# Estrutura de Usuario - Fim

# Estrutura de Chat - Inicio

        #Display do chat
        self.ChatText = QtWidgets.QTextEdit(self.frame_2)
        self.ChatText.setGeometry(QtCore.QRect(10, 10, 281, 381))
        self.ChatText.setStyleSheet("background-color: rgb(40, 44, 52); color: white; font-size: 14px;")
        self.ChatText.setObjectName("ChatText")
        self.ChatText.setReadOnly(True) # Define apenas leitura


        # Escrever texto ao chat
        self.SendText = QtWidgets.QTextEdit(self.frame_2)
        self.SendText.setGeometry(QtCore.QRect(10, 400, 211, 21))
        self.SendText.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.SendText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SendText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.SendText.setObjectName("SendText")
        self.SendText.setStyleSheet("background-color: rgb(40, 44, 52); color: white; font-size: 14px;")


        # Botão para enviar o texto ao chat
        self.SendButton = QtWidgets.QPushButton(self.frame_2)
        self.SendButton.setGeometry(QtCore.QRect(230, 400, 61, 21))
        self.SendButton.setStyleSheet("QPushButton {\n"
                                         "    border: 2px solid rgb(52, 59, 72);\n"
                                         "    border-radius: 5px;    \n"
                                         "    background-color: rgb(52, 59, 72);\n"
                                         "    color: white; /* Add this line to set the text color to white */\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb(57, 65, 80);\n"
                                         "    border: 2px solid rgb(61, 70, 86);\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:pressed {    \n"
                                         "    background-color: rgb(35, 40, 49);\n"
                                         "    border: 2px solid rgb(43, 50, 61);\n"
                                         "}\n"
                                         "")
        self.SendButton.setObjectName("SendButton")

# Estrutura de Chat - Fim

# Estrutura do Youtube - Inicio

        # Botão para adicionar video no youtube
        self.YoutubeButton = QtWidgets.QPushButton(self.frame)
        self.YoutubeButton.setGeometry(QtCore.QRect(650, 430, 91, 21))

        # Css do botâo do youtube
        self.YoutubeButton.setStyleSheet("QPushButton {\n"
                                        "    border: 2px solid rgb(52, 59, 72);\n"
                                        "    border-radius: 5px;    \n"
                                        "    background-color: rgb(52, 59, 72);\n"
                                        "    color: white; /* Add this line to set the text color to white */\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgb(57, 65, 80);\n"
                                        "    border: 2px solid rgb(61, 70, 86);\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed {    \n"
                                        "    background-color: rgb(35, 40, 49);\n"
                                        "    border: 2px solid rgb(43, 50, 61);\n"
                                        "}\n"
                                        "")
        self.YoutubeButton.setObjectName("YoutubeButton")


        # Chat de texto para adicionar o link do video do youtube
        self.YoutubeText = QtWidgets.QTextEdit(self.frame)
        self.YoutubeText.setEnabled(True)
        self.YoutubeText.setGeometry(QtCore.QRect(10, 430, 631, 21))
        self.YoutubeText.setStyleSheet("")
        self.YoutubeText.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.YoutubeText.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.YoutubeText.setObjectName("YoutubeText")
        self.YoutubeText.setStyleSheet("color: white;")


# Estrutura do Youtube - Fim

        # Estrutura
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Verifica se botao foi clicado e redireciona para função

        self.SendButton.clicked.connect(self.send_message)
        self.YoutubeButton.clicked.connect(self.youtube_video)
        self.SyncButton2.clicked.connect(self.adduser)

        # Parametros da estrutura do youtube
        self.webEngineView = None
        self.video_url = ""
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.frame)
        self.webEngineView.setGeometry(QtCore.QRect(0, 10, 731, 411))
        self.webEngineView.setObjectName("webEngineView")


    # Define o IP do servidor
    def addIp(self):
        # Socket para se conectar ao servidor

        self.server_ip = self.SendText3.toPlainText() # Define o IP do servidor
        self.server_port = 12345  # Escolha a porta do servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect((self.server_ip, self.server_port)) # Efetua conexao ao servidor
        self.client_socket.send(("Connected," + str(hash)).encode('utf-8')) # Avisa para o servidor que alguem conectou

        # Altera status p/ conectado = True
        global conectado
        conectado = True

        self.frame_4.deleteLater()

    # Define quem é o usuario
    def adduser(self):
        self.user = self.SendText2.toPlainText()
        self.frame_3.deleteLater() # Libera o chat

    # Evento de movimento quando o programa se mover ele muda de posição
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseMove and event.buttons() == QtCore.Qt.LeftButton:
            MainWindow.move(event.globalPos() - self.dragPosition)
            event.accept()
            return True
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - MainWindow.frameGeometry().topLeft()
            event.accept()
            return True
        return super().eventFilter(obj, event)

    # Verifica se o video esta Pausado
    def check_pause(self):
        try:
            if self.webEngineView:
                self.webEngineView.page().runJavaScript("document.querySelector('video').paused", self.output_pause)
        except Exception as e:
            pass

    # Verifica a posição do video
    def check_position(self):
        try:
            if self.webEngineView:
                self.webEngineView.page().runJavaScript("document.querySelector('video').currentTime",
                                                        self.output_position)
                if self.old_new_position != self.position:
                    self.update_video_position(self.position)
        except Exception as e:
            pass


    # Função de minizar o programa
    def minimize_window(self):
        MainWindow.showMinimized()

    # Função de saida do programa
    def exit_application(self):
        MainWindow.close()

    # Envia mensagem para o servidor e mostra no chat
    def send_message(self):
        message = self.SendText.toPlainText()
        if message:
            self.client_socket.send((f"Message({self.user})" + message + ',' + str(hash)).encode('utf-8')) # Envia servidor
            self.display_message(f"{self.user}: {message}") # Mostra chat
            self.SendText.clear()

    # Mostra a mensagem no chat
    def display_message(self, message):
        current_text = self.ChatText.toPlainText()
        self.ChatText.setPlainText(current_text + message + '\n')

    # Detecta se o video foi movido
    def update_video_position(self, new_position):
        if new_position > self.old_new_position + 4: # Verifica avaçar
            self.webEngineView.page().runJavaScript(
                f"document.querySelector('video').currentTime = {new_position};")
            self.client_socket.send(('Position' + str(new_position) + ',' + str(hash)).encode('utf-8'))
            self.webEngineView.page().runJavaScript("document.querySelector('video').currentTime",
                                                    self.output_position)

        elif new_position < self.old_new_position - 4: # Verifica volta
            self.webEngineView.page().runJavaScript(
                f"document.querySelector('video').currentTime = {new_position};")
            self.client_socket.send(('Position' + str(new_position) + ',' + str(hash)).encode('utf-8'))
            self.webEngineView.page().runJavaScript("document.querySelector('video').currentTime",
                                                    self.output_position)

        elif self.paused == False: # Verifica Pausado
            if new_position != self.old_new_position:
                self.client_socket.send(('PStore' + str(new_position) + ',' + str(hash)).encode('utf-8'))
                self.webEngineView.page().runJavaScript("document.querySelector('video').currentTime",
                                                        self.output_position)

        self.old_new_position = new_position


   ## Detecta Movimento mas pausado
   #def update_video_pause(self, new_position):
   #    if self.paused == True:
   #        self.webEngineView.page().runJavaScript(
   #            f"document.querySelector('video').pause();")
   #        self.client_socket.send(('Position' + str(new_position) + ',' + str(hash)).encode('utf-8'))
   #    elif new_position < self.old_new_position - 4:
   #        self.webEngineView.page().runJavaScript(
   #            f"document.querySelector('video').currentTime = {new_position};")
   #        self.client_socket.send(('Position' + str(new_position) + ',' + str(hash)).encode('utf-8'))
   #    self.old_new_position = new_position

    # Define os nomes dos botões
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.YoutubeButton.setText(_translate("MainWindow", "Enviar Video"))
        self.SendButton.setText(_translate("MainWindow", "Enviar"))
        self.SyncButton2.setText(_translate("MainWindow", "Adicionar Usuario"))
        self.SyncButton3.setText(_translate("MainWindow", "Adicionar IP Servidor"))


    # Recebe os parametros do servidor
    def listen_to_server(self):

        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message.split(',')[-1] != str(hash):
                    if message.split(',')[0].startswith("PButton"):
                        self.webEngineView.page().runJavaScript(
                            "document.querySelector('.ytp-cued-thumbnail-overlay-image').click()")

                    elif message.startswith("FPosition") and self.logado == False:
                        print(self.logado)
                        valors = message.replace('FPosition', '').split(',')
                        numeric_part = valors[0]
                        numeric_part = numeric_part.split('.')[0]
                        valors2 = int(numeric_part)
                        if valors[1] != '':

                            self.video_url2 = f"https://www.youtube.com/embed/{valors[1]}?start={valors2}&autoplay=1&mute=1"
                            self.video_url_signal.emit(self.video_url2)
                            self.logado = True

                    elif message.startswith("Message"):
                        import re
                        username = re.search('\((.*?)\)', message)
                        self.update_chat_text_signal.emit(
                            f"{username.group(1)}: {message.replace('Message', '', 1).replace(f'({username.group(1)})', '').replace(',' + message.split(',')[-1], '')}")
                    elif message.startswith("Position"):
                        self.webEngineView.page().runJavaScript(
                            f"document.querySelector('video').currentTime = {message.split(',')[0].replace('Position', '', 1)}")
                        self.Envio = True
                    elif message.startswith("Sync"):
                        print(message)
                    elif str(message).find('YTBA') != -1:
                        self.video_url2 = f"https://www.youtube.com/embed/{message.split(',')[0].replace('YTBA', '')}?autoplay=1&mute=1"
                        self.video_url_signal.emit(self.video_url2)  # Emit the signal

            except Exception as e:
                pass
        # Listen -Fim

        # Outputs - inicio

    def output_position(self, result):
        if result == None:
            self.position = 0
        else:
            self.position = result

    def output_pause(self, result):
        self.paused = result
        if self.paused != self.pausedold:
            self.client_socket.send(('PButton' + str(result) + ',' + str(hash)).encode('utf-8'))
        self.pausedold = result

        # Outputs - Fim

    def youtube_video(self):
        print(1)
        youtube_text = self.YoutubeText.toPlainText()
        if youtube_text:
            if conectado == True:
                import re
                pattern = r"(?:v=|/embed/|youtu.be/)([A-Za-z0-9_-]+)"
                match = re.search(pattern, youtube_text)
                self.video_url = f"https://www.youtube.com/embed/{str(match.group(1))}?autoplay=1&mute=1"
                self.webEngineView.setUrl(QtCore.QUrl(self.video_url))
                self.client_socket.send(('YTBA' + str(match.group(1)) + ',' + str(hash)).encode('utf-8'))
                self.valor = self.webEngineView.page().runJavaScript("document.querySelector('video').duration")
            else:
                self.YoutubeText.setText("Não conectado ao servidor")

    def update_video_url(self, new_url):
        # This slot will run in the main thread
        self.webEngineView.setUrl(QtCore.QUrl(new_url))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())