from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QComboBox, QLineEdit, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QShowEvent, QKeyEvent
from transport.task_3.truck import Truck
from transport.task_3.ship import Ship

class AddVehicle(QMainWindow):
    vehicle_added = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить транспорт")
        self.setFixedSize(500, 250)

        central = QWidget()
        self.setCentralWidget(central)

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

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 200, 120, 40)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 200, 120, 40)
        btn_close.clicked.connect(self.close)

        btn.clicked.connect(self.on_add_vehicle)
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        self.on_combo_changed(self.combo.currentText())

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def clear_fields(self):
        self.line_capacity.clear()
        self.line_name.clear()
        self.line_color.clear()
        self.combo.setCurrentIndex(0)
        self.on_combo_changed(self.combo.currentText())

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.clear_fields()

    def on_combo_changed(self, text):
        if text == "Грузовик":
            self.line_name.hide()
            self.line_name.clear()
            self.line_color.show()
        elif text == "Судно":
            self.line_color.hide()
            self.line_color.clear()
            self.line_name.show()

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    def on_add_vehicle(self):
        capacity_text = self.line_capacity.text().strip()
        try:
            capacity = float(capacity_text)
        except ValueError:
            self.show_warning("Вместимость должна быть числом", self.line_capacity)
            return
        if self.combo.currentText() == "Грузовик":
            if not self.line_color.text().strip():
                self.show_warning("Цвет грузовика не может быть пустым", self.line_color)
                return
            vehicle = Truck(capacity, self.line_color.text().strip())
        else:
            if not self.line_name.text().strip():
                self.show_warning("Имя судна не может быть пустым", self.line_name)
                return
            vehicle = Ship(capacity, self.line_name.text().strip())

        self.vehicle_added.emit(vehicle)
        self.clear_fields()
        self.close()
