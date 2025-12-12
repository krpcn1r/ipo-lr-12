from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QTableWidget, QHeaderView
import sys


class ChangeVehicle(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить транспорт")
        self.setFixedSize(700, 570)

        central = QWidget()
        self.setCentralWidget(central)

        btn_save = QPushButton("Сохранить", central)
        btn_save.setGeometry(100, 515, 140, 40)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(460, 515, 140, 40)
        btn_close.clicked.connect(self.close)

        table = QTableWidget(0, 3, central)
        table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        table.setGeometry(0, 0, 700, 500)
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
