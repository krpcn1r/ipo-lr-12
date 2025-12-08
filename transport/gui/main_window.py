from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem
import sys

from pyqt_tools.messages import show_message

from transport.task_3.transportCompany import TransportCompany

class MainWindow(QMainWindow):

    def __init__(self):
        company = TransportCompany("My Transport Company")
        super().__init__()
        self.setWindowTitle(company.name)
        self.setFixedSize(1100, 700)
        self.setMinimumSize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        btn1 = QPushButton("Добавить клиента", central)
        btn1.setGeometry(50, 100, 140, 40)
        btn2 = QPushButton("Добавить транспорт", central)
        btn2.setGeometry(50, 200, 140, 40)
        btn3 = QPushButton("Распределить грузы", central)
        btn3.setGeometry(50, 300, 140, 40)
        btn4 = QPushButton("Экспорт результата", central)
        btn4.setGeometry(50, 400, 140, 40)
        btn5 = QPushButton("О программе", central)
        btn5.setGeometry(50, 500, 140, 40)

        status = QStatusBar()
        status.setStyleSheet("""
            QStatusBar {
                background-color: #292929;
                border-top: 1px solid #2C2C2C;
                font-size: 10pt;
                padding: 3px;
                color: white;
            }
        """)
        self.setStatusBar(status)
        status.showMessage("Программа запущена")


app = QApplication([])
window = MainWindow()
window.show()
app.exec()