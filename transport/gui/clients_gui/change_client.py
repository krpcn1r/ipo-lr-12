from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton
import sys

class ChangeClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)

        label = QLabel("Изменить клиента", central)
        label.move(50, 80)