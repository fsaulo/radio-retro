import sys
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QTextEdit, QPushButton, QApplication, QAction,
                             QVBoxLayout, QHBoxLayout, QDialog, QWidget, QLabel)
import modem

class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle('Radio Retro')
        self.setCentralWidget(widget)


class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # -------- Charts
        # - SpectogramChartLayout
        receivedSpectogramChartLayout = QVBoxLayout()
        receivedSpectogramChartLayout.addWidget(QLabel("Espectograma"))
        receivedSpectogramChartLayout.addWidget(QTextEdit())
        # - SignalChartLAyout
        receivedSignalChartLayout = QVBoxLayout()
        receivedSignalChartLayout.addWidget(QLabel("Sinal"))
        receivedSignalChartLayout.addWidget(QTextEdit())

        # Receiving Signal Layout
        receivedSignalLayout = QHBoxLayout()
        receivedSignalLayout.addWidget(QLabel("Mensagem Enviada"))
        receivedSignalLayout.addLayout(receivedSpectogramChartLayout)
        receivedSignalLayout.addLayout(receivedSignalChartLayout)

        # Sending Signal Layout
        # - SpectogramChartLayout
        sentSpectogramChartLayout = QVBoxLayout()
        sentSpectogramChartLayout.addWidget(QLabel("Espectograma"))
        sentSpectogramChartLayout.addWidget(QTextEdit())
        # - SignalChartLAyout
        sentSignalChartLayout = QVBoxLayout()
        sentSignalChartLayout.addWidget(QLabel("Sinal"))
        sentSignalChartLayout.addWidget(QTextEdit())

        # Receiving Signal Layout
        sentSignalLayout = QHBoxLayout()
        sentSignalLayout.addWidget(QLabel("Mensagem Recebida"))
        sentSignalLayout.addLayout(sentSpectogramChartLayout)
        sentSignalLayout.addLayout(sentSignalChartLayout)

        # ------------------------------------
        # SignalsLayout
        signalsLayout = QVBoxLayout()
        signalsLayout.addLayout(sentSignalLayout)
        signalsLayout.addLayout(receivedSignalLayout)

        # Chat Area Layout
        self.chatArea = QTextEdit()

        # Bottom Layout
        self.textMessageField = QLineEdit()
        self.textMessageField.setPlaceholderText("Digite aqui sua mensagem")
        self.textMessageField.returnPressed.connect(self.sendTextMessage)

        self.sendTextMessageButton = QPushButton("Enviar")
        self.sendTextMessageButton.clicked.connect(self.sendTextMessage)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.textMessageField)
        bottomLayout.addWidget(self.sendTextMessageButton)

        # Set Final layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(signalsLayout)
        self.layout.addWidget(self.chatArea)
        self.layout.addLayout(bottomLayout)
        self.setLayout(self.layout)

    def sendTextMessage(self):
        print('Eu: ' + self.textMessageField.text())

        # emitMessage(self.textMessageField.text())
        self.chatArea.append('<strong>Eu:</strong> ' +
                             self.textMessageField.text())
        self.textMessageField.clear()
        transmitter = modem.Transmitter()
        # modem.config(Bd=500)
        transmitter.config(Bd=10, carrier=1200)
        # modem.send_generic_message('Enviando uma mensagem muito mais longa mas lentamente§')
        transmitter.send_generic_message(self.textMessageField.text())


if __name__ == '__main__':
    app = QApplication([])

    widget = Widget()

    appWindow = MainWindow(widget)
    appWindow.resize(800, 600)
    appWindow.show()
    # create form
    # show form
    sys.exit(app.exec_())
