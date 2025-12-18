from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QComboBox, QLineEdit, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QShowEvent, QKeyEvent
from transport.task_3.truck import Truck
from transport.task_3.ship import Ship

class AddVehicle(QMainWindow):
    # Сигнал передающий объект созданного транспорта обратно в вызывающее окно
    vehicle_added = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        # Инициализация параметров окна
        self.setWindowTitle("Добавить транспорт")
        self.setFixedSize(500, 250)

        # Создание основного виджета
        central = QWidget()
        self.setCentralWidget(central)

        # Выбор типа транспорта
        self.combo = QComboBox(central)
        self.combo.setGeometry(50, 50, 140, 30)
        self.combo.addItems(["Грузовик", "Судно"])
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                color: black;
                font: 15px;
            }
            QComboBox QAbstractItemView {
                color: black;
                background-color: #ffffff;
                selection-background-color: #bdbbbb;
                selection-color: #000000;
            }
        """)

        # Поле ввода грузоподъемности 
        self.line_capacity = QLineEdit(central)
        self.line_capacity.setPlaceholderText("Введите вместительность")
        self.line_capacity.setGeometry(50, 100, 375, 30)
        self.line_capacity.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: black;
                font: 15px;
            }
        """)

        # Поле ввода названия
        self.line_name = QLineEdit(central)
        self.line_name.setPlaceholderText("Введите имя")
        self.line_name.setGeometry(50, 150, 375, 30)
        self.line_name.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: black;
                font: 15px;
            }
        """)

        # Поле ввода цвета
        self.line_color = QLineEdit(central)
        self.line_color.setPlaceholderText("Введите цвет")
        self.line_color.setGeometry(50, 150, 375, 30)
        self.line_color.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: black;
                font: 15px;
            }
        """)
        self.line_color.hide()

        # Кнопка добавления
        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 200, 120, 40)

        # Кнопка закрытия
        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 200, 120, 40)
        btn_close.clicked.connect(self.close)

        # Привязка обработчиков событий
        btn.clicked.connect(self.on_add_vehicle)
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        
        # Установка начального состояния полей
        self.on_combo_changed(self.combo.currentText())

    # Закрытие окна при нажатии клавиши Esc
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
