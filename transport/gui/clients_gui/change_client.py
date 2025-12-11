from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QTableWidget, QHeaderView
import sys


class ChangeClient(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить клиента")
        self.setFixedSize(800, 600)

        central = QWidget()

        table = QTableWidget(0, 3, central)
        table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        table.setGeometry(325, 85, 700, 500)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                gridline-color: #DDDDDD;
                background-color: #FFFFFF;
                alternate-background-color: #FAFAFA;
                color: #212121;
            }
            QHeaderView::section {
                background-color: #cccccc;
                color: #212121;
            }
            QTableCornerButton::section {
                background-color: #DDDDDD;
                border: 1px solid #DDDDDD;
            }
            QTableWidget QLineEdit {
                background-color: #D5D5D5;   /* фон редактора */
                color: #212121;              /* цвет текста редактора */
                border: 1px solid #BDBDBD;   /* рамка редактора */
            }
            QTableWidget::item:selected {
            background-color: #bdbbbb;
            color: #000000;
        }
        """)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
