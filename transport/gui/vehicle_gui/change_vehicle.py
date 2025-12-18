from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, \
    QHeaderView, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent
from transport.task_3.ship import Ship
from transport.task_3.truck import Truck


class ChangeVehicle(QMainWindow):
    vehicle_changed = pyqtSignal(int, object)

    def __init__(self, company=None):
        super().__init__()
        self.company = company
        self.setWindowTitle("Изменить транспорт")
        self.setFixedSize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)

        self.table = QTableWidget(0, 6, central)
        self.table.setHorizontalHeaderLabels(["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
        self.table.setGeometry(20, 20, 760, 400)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.edit_widget = QWidget(central)
        self.edit_widget.setGeometry(20, 440, 760, 70)
        self.edit_widget.hide()

        self.label_type = QLabel("Тип:", self.edit_widget)
        self.label_type.setGeometry(10, 5, 100, 25)

        self.label_type_value = QLabel("", self.edit_widget)
        self.label_type_value.setGeometry(10, 30, 100, 25)
        self.label_type_value.setStyleSheet("QLabel { background-color: #e0e0e0; padding: 4px; border-radius: 3px; }")

        self.label_capacity = QLabel("Вместительность:", self.edit_widget)
        self.label_capacity.setGeometry(120, 5, 150, 25)

        self.line_capacity = QLineEdit(self.edit_widget)
        self.line_capacity.setGeometry(120, 30, 150, 30)
        self.line_capacity.setPlaceholderText("Вместительность")

        self.label_color = QLabel("Цвет:", self.edit_widget)
        self.label_color.setGeometry(280, 5, 150, 25)
        self.label_color.hide()

        self.line_color = QLineEdit(self.edit_widget)
        self.line_color.setGeometry(280, 30, 150, 30)
        self.line_color.hide()

        self.label_name = QLabel("Название:", self.edit_widget)
        self.label_name.setGeometry(280, 5, 150, 25)
        self.label_name.hide()

        self.line_name = QLineEdit(self.edit_widget)
        self.line_name.setGeometry(280, 30, 150, 30)
        self.line_name.hide()

        btn_save = QPushButton("Сохранить", self.edit_widget)
        btn_save.setGeometry(450, 30, 100, 30)
        btn_save.clicked.connect(self.on_save)

        btn_cancel = QPushButton("Отмена", self.edit_widget)
        btn_cancel.setGeometry(560, 30, 100, 30)
        btn_cancel.clicked.connect(self.cancel_edit)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(660, 550, 120, 40)
        btn_close.clicked.connect(self.close)

        self.current_index = None
        self.current_vehicle = None

    # Закрытие окна при нажатии Escape
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    # Загрузка транспорта
    def load_vehicles(self, company):
        self.company = company
        vehicles_list = company.vehicles if hasattr(company, 'vehicles') else []
        # Очистка таблицы
        self.table.setRowCount(0)
        for idx, vehicle in enumerate(vehicles_list):
            row = self.table.rowCount()
            self.table.insertRow(row)
            # Заполнение ячеек
            self.table.setItem(row, 0, QTableWidgetItem(vehicle.vehicle_id))
            self.table.setItem(row, 1, QTableWidgetItem(vehicle.__class__.__name__))
            self.table.setItem(row, 2, QTableWidgetItem(str(vehicle.capacity)))
            self.table.setItem(row, 3, QTableWidgetItem(str(vehicle.current_load)))
            
            # Заполнение ячеек в зависимости от типа транспорта
            if isinstance(vehicle, Truck):
                self.table.setItem(row, 4, QTableWidgetItem(vehicle.color))
                self.table.setItem(row, 5, QTableWidgetItem("-"))
            elif isinstance(vehicle, Ship):
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem(vehicle.name))
            else:
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem("-"))

    # Активация режима редактирования выбранного индекса
    def on_cell_double_clicked(self, row, column):
        if self.company is None:
            return

        vehicles_list = self.company.vehicles if hasattr(self.company, 'vehicles') else []
        if row < len(vehicles_list):
            self.current_index = row
            vehicle = vehicles_list[row]
            self.load_vehicle(vehicle, row)
            self.edit_widget.show()

    # Заполнение полей
    def load_vehicle(self, vehicle, index):
        self.current_index = index
        self.current_vehicle = vehicle

        self.label_type_value.setText(vehicle.__class__.__name__)
        self.line_capacity.setText(str(vehicle.capacity))

        # Управление видимостью полей
        if isinstance(vehicle, Truck):
            self.label_color.show()
            self.line_color.show()
            self.label_name.hide()
            self.line_name.hide()
            self.line_color.setText(vehicle.color)
        elif isinstance(vehicle, Ship):
            self.label_color.hide()
            self.line_color.hide()
            self.label_name.show()
            self.line_name.show()
            self.line_name.setText(vehicle.name)

    # Отмена изменений
    def cancel_edit(self):
        self.edit_widget.hide()
        self.current_index = None
        self.current_vehicle = None

    # Отображение ошибки
    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        if field:
            field.clear()

    # Сохранение изменений
    def on_save(self):
        if self.current_index is None or self.company is None or self.current_vehicle is None:
            return

        # Извлечение и нормализация строки
        capacity_text = self.line_capacity.text().strip()
        try:
            capacity = float(capacity_text)
            if capacity <= 0:
                self.show_warning("Вместительность должна быть больше 0", self.line_capacity)
                return
        except ValueError:
            self.show_warning("Вместительность должна быть числом", self.line_capacity)
            return

        vehicles_list = self.company.vehicles if hasattr(self.company, 'vehicles') else []
        if self.current_index >= len(vehicles_list):
            return

        # Обновление атрибутов объекта
        vehicles_list[self.current_index].capacity = capacity

        # Обновление ячеек
        if isinstance(self.current_vehicle, Truck):
            color = self.line_color.text().strip()
            if not color:
                self.show_warning("Цвет грузовика не может быть пустым", self.line_color)
                return
            vehicles_list[self.current_index].color = color
            self.table.setItem(self.current_index, 2, QTableWidgetItem(str(capacity)))
            self.table.setItem(self.current_index, 4, QTableWidgetItem(color))

        elif isinstance(self.current_vehicle, Ship):
            name = self.line_name.text().strip()
            if not name:
                self.show_warning("Название судна не может быть пустым", self.line_name)
                return
            vehicles_list[self.current_index].name = name
            self.table.setItem(self.current_index, 2, QTableWidgetItem(str(capacity)))
            self.table.setItem(self.current_index, 5, QTableWidgetItem(name))

        # Передача сигнала
        self.vehicle_changed.emit(self.current_index, vehicles_list[self.current_index])

        # Скрытие контейнера управления
        self.edit_widget.hide()
        self.current_index = None
        self.current_vehicle = None
        QMessageBox.information(self, "Успех", "Транспорт успешно изменен")
