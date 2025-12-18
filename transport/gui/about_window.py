from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
import sys


class AboutWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Настройка заголовка и фиксированного размера окна
        self.setWindowTitle("О программе")
        self.setFixedSize(350, 250)

        # Создание центрального виджета для размещения элементов
        central = QWidget()
        self.setCentralWidget(central)

        # Общий стиль для информационных меток (Labels)
        label_style = """
            QLabel {
                font: 15px;
                border: 2px solid black;
                border-radius: 6px;
                background-color: white;
                padding: 7px;
            }
        """

        # Метка с номером лабораторной работы
        lb_lr = QLabel("Лабораторная 13", central)
        lb_lr.setStyleSheet(label_style)
        lb_lr.setGeometry(20, 20, 150, 40)

        # Метка с номером варианта
        lb_var = QLabel("Вариант 2", central)
        lb_var.setStyleSheet(label_style)
        lb_var.setGeometry(20, 80, 150, 40)

        # Метка с фамилией автора и группой
        lb_name = QLabel("Зайцев 89ТП", central)
        lb_name.setStyleSheet(label_style)
        lb_name.setGeometry(20, 140, 150, 40)

        # Кнопка закрытия окна
        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(20, 190, 140, 40)
        # Соединение нажатия кнопки со встроенным методом close()
        btn_close.clicked.connect(self.close)

    # Метож для закрытия окна при нажатии клавиши esc.
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            # Если нажата другая клавиша, передаем событие дальше
            super().keyPressEvent(event)
