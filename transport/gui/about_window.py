from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
import sys


class AboutWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("О программе")
        self.setFixedSize(350, 250)

        central = QWidget()
        self.setCentralWidget(central)

        lb_lr = QLabel("Лабораторная 13", central)
        lb_lr.setStyleSheet("""
            QLabel {
                font: 15px;
                border: 2px solid black;
                border-radius: 6px;
                background-color: white;
                padding: 7px;
            }
        """)
        lb_lr.setGeometry(20, 20, 150, 40)

        lb_var = QLabel("Вариант 2", central)
        lb_var.setStyleSheet("""
            QLabel {
                font: 15px;
                border: 2px solid black;
                border-radius: 6px;
                background-color: white;
                padding: 7px;
            }
        """)
        lb_var.setGeometry(20, 80, 150, 40)

        lb_name = QLabel("Зайцев 89ТП", central)
        lb_name.setStyleSheet("""
            QLabel {
                font: 15px;
                border: 2px solid black;
                border-radius: 6px;
                background-color: white;
                padding: 7px;
            }
        """)
        lb_name.setGeometry(20, 140, 150, 40)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(20, 190, 140, 40)
        btn_close.clicked.connect(self.close)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)