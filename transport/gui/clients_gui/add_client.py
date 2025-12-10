from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QLineEdit
import sys

class AddClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(500, 300)

        central = QWidget()
        self.setCentralWidget(central)

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 250, 120, 30)

        line_edit = QLineEdit("Введите текст", central)
        line_edit.setGeometry(50, 30, 375, 25)