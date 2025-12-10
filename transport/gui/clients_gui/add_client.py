from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QLineEdit, QCheckBox
from PyQt6.QtCore import Qt
import sys

class AddClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(500, 250)

        central = QWidget()
        self.setCentralWidget(central)

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 200, 120, 40)
        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 200, 120, 40)
        btn_close.clicked.connect(self.close)
        line_add_name = QLineEdit(central)
        line_add_name.setPlaceholderText("Введите имя клиента")
        line_add_name.setStyleSheet("""
        QLineEdit{
            background-color: #ffffff;
            color: black;
            font: 15px;
        }
        """)
        line_add_name.setGeometry(50, 30, 375, 30)

        line_add_weight = QLineEdit(central)
        line_add_weight.setPlaceholderText("Введите вес груза")
        line_add_weight.setStyleSheet("""
        QLineEdit{
            background-color: #ffffff;
            color: black;
            font: 15px;
        }
        """)
        line_add_weight.setGeometry(50, 80, 375, 30)

        check_vip = QCheckBox("VIP-клиент ", central)
        check_vip.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        check_vip.setStyleSheet("""
        QCheckBox{
            font: 15px;
        }
        QCheckBox::indicator {
            width: 13px;
            height: 13px;
            border-radius: 6.7px;       
            background-color: #ffffff;
        }
        QCheckBox::indicator:checked {
            background-color: #4CAF50; 
            border: 2px solid #2E7D32;  
        }
        QCheckBox::indicator:unchecked {
            background-color: #FFFFFF;
            border: 2px solid #333333;   
        }
        """)
        check_vip.move(53, 130)