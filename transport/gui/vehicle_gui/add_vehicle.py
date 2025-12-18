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

        self.line_capacity = QLineEdit(central)
        self.line_capacity.setPlaceholderText("Введите вместительность")
        self.line_capacity.setGeometry(50, 100, 375, 30)

        self.line_name = QLineEdit(central)
        self.line_name.setPlaceholderText("Введите имя")
        self.line_name.setGeometry(50, 150, 375, 30)

        self.line_color = QLineEdit(central)
        self.line_color.setPlaceholderText("Введите цвет")
        self.line_color.setGeometry(50, 150, 375, 30)
        self.line_color.hide()

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 200, 120, 40)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 200, 120, 40)
        btn_close.clicked.connect(self.close)

        btn.clicked.connect(self.on_add_vehicle)
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        self.on_combo_changed(self.combo.currentText())

    # Закрытие окна при нажатии Escape
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    # Очистка полей
    def clear_fields(self):
        self.line_capacity.clear()
        self.line_name.clear()
        self.line_color.clear()
        self.combo.setCurrentIndex(0)
        self.on_combo_changed(self.combo.currentText())

    # Сброс состояния формы при отображении окна
    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.clear_fields()

    # Смена полей ввода при смене типа транспорта
    def on_combo_changed(self, text):
        if text == "Грузовик":
            self.line_name.hide()
            self.line_name.clear()
            self.line_color.show()
        elif text == "Судно":
            self.line_color.hide()
            self.line_color.clear()
            self.line_name.show()

    # Отображение ошибки
    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    # Добавление транспорта
    def on_add_vehicle(self):
        # Извлечение и нормализация строки
        capacity_text = self.line_capacity.text().strip()
        try:
            # Преобразование строки в float
            capacity = float(capacity_text)
        except ValueError:
            # Обработка ошибки при некорректном формате числа
            self.show_warning("Вместимость должна быть числом", self.line_capacity)
            return

        # Проверка выбранного значения в комбобоксе для определения типа создаваемого объекта
        if self.combo.currentText() == "Грузовик":
            if not self.line_color.text().strip():
                self.show_warning("Цвет грузовика не может быть пустым", self.line_color)
                return
            # Создание объекта класса Truck
            vehicle = Truck(capacity, self.line_color.text().strip())
        else:
            if not self.line_name.text().strip():
                self.show_warning("Имя судна не может быть пустым", self.line_name)
                return
            # Создание объекта класса Ship
            vehicle = Ship(capacity, self.line_name.text().strip())

        # Передача сигнала
        self.vehicle_added.emit(vehicle)
        # Очистка полей
        self.clear_fields()
        self.close()
