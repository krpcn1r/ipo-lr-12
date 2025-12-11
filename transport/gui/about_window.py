from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton
import sys


class AboutWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("О программе")
        self.setFixedSize(600, 400)

        central = QWidget()
