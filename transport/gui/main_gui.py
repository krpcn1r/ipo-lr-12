import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QTableWidgetItem, QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, \
    QTableWidget, QHeaderView, QComboBox, QLabel, QFrame, QMessageBox
from PyQt6.QtCore import Qt
from transport.gui.clients_gui.add_client import AddClient
from transport.gui.clients_gui.change_client import ChangeClient
from transport.gui.vehicle_gui.add_vehicle import AddVehicle
from transport.gui.vehicle_gui.change_vehicle import ChangeVehicle
from transport.gui.about_window import AboutWindow
from transport.task_3.transportCompany import TransportCompany
from transport.task_1.client import Client
from transport.task_3.ship import Ship
from transport.task_3.truck import Truck
import json

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Экземпляр класса компании
        self.company = TransportCompany("My Transport Company")

        # Окна управления
        self.cv_window = ChangeVehicle(self.company)
        self.cv_window.vehicle_changed.connect(self.on_vehicle_changed)
        self.av_window = AddVehicle()
        self.av_window.vehicle_added.connect(self.add_vehicle_to_table)
        self.cc_window = ChangeClient(self.company)
        self.cc_window.client_changed.connect(self.on_client_changed)
        self.au_window = AddClient()
        self.au_window.client_added.connect(self.add_client_to_table)
        self.aw_window = AboutWindow()
        
        self.setWindowTitle(self.company.name)
        self.setFixedSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        label = QLabel("Выберите таблицу:", central)
        label.setGeometry(50, 55, 200, 25)

        self.combo = QComboBox(central)
        self.combo.setGeometry(50, 80, 140, 35)
        self.combo.addItems(["Клиенты", "Транспорт"])
        self.combo.currentTextChanged.connect(self.on_combo_changed)

        # Кнопка удаления выбранной записи
        btn_delete = QPushButton("Удалить элемент", central)
        btn_delete.setGeometry(50, 125, 140, 40)
        btn_delete.clicked.connect(self.delete_selected_row)

        for y in [170, 300, 488]:
            line_h = QFrame(central)
            line_h.setFrameShape(QFrame.Shape.HLine)
            line_h.setGeometry(20, y, 200, 30)

        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(240, 25, 2, 630)

        # Кнопки управления
        btn1 = QPushButton("Добавить клиента", central)
        btn1.setGeometry(50, 200, 140, 40)
        btn1.clicked.connect(self.open_add_client)

        btn2 = QPushButton("Изменить клиента", central)
        btn2.setGeometry(50, 250, 140, 40)
        btn2.clicked.connect(self.open_change_client)

        btn3 = QPushButton("Добавить транспорт", central)
        btn3.setGeometry(50, 340, 140, 40)
        btn3.clicked.connect(self.open_add_vehicle)

        btn4 = QPushButton("Изменить транспорт", central)
        btn4.setGeometry(50, 390, 140, 40)
        btn4.clicked.connect(self.open_change_vehicle)

        btn5 = QPushButton("Распределить грузы", central)
        btn5.setGeometry(50, 440, 140, 40)
        btn5.clicked.connect(self.optimize_distribution)

        btn6 = QPushButton("Экспорт результата", central)
        btn6.setGeometry(50, 525, 140, 40)
        btn6.clicked.connect(self.export_to_json)

        btn7 = QPushButton("О программе", central)
        btn7.setGeometry(50, 575, 140, 40)
        btn7.clicked.connect(self.open_about_program)

        # Статусная строка
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Программа запущена")

        # Таблица данных
        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        self.table.setGeometry(325, 85, 700, 500)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # Переключение таблицы отображаемых данных
    def on_combo_changed(self, text):
        try:
            self.table.setRowCount(0)
            if text == "Клиенты":
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
                for client in self.company.clients:
                    self.add_client_row(client)
            elif text == "Транспорт":
                self.table.setColumnCount(6)
                self.table.setHorizontalHeaderLabels(
                    ["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
                for vehicle in self.company.vehicles:
                    self.add_vehicle_row(vehicle)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при загрузке таблицы: {str(e)}", 5000)

    # Вызов окна добавления клиента
    def open_add_client(self):
        self.au_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.au_window.show()

    # Вызов окна изменения клиента
    def open_change_client(self):
        self.cc_window.load_clients(self.company)
        self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cc_window.show()

    # Вызов окна добавления транспорта
    def open_add_vehicle(self):
        self.av_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.av_window.show()

    # Вызов окна изменения транспорта
    def open_change_vehicle(self):
        self.cv_window.load_vehicles(self.company)
        self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cv_window.show()

    # Вызов окна "О программе"
    def open_about_program(self):
        self.aw_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.aw_window.show()

    # Добавление клиента в таблицу
    def add_client_to_table(self, name: str, weight: float, is_vip: bool):
        client = Client(name, weight, is_vip)
        self.company.add_client(client)
        if self.combo.currentText() == "Клиенты":
            self.add_client_row(client)
        else:
            self.combo.setCurrentText("Клиенты")
        self.status_bar.showMessage(f"Клиент '{name}' добавлен", 3000)

    # Добавление транспорта в таблицу
    def add_vehicle_to_table(self, vehicle):
        self.company.add_vehicle(vehicle)
        if self.combo.currentText() == "Транспорт":
            self.add_vehicle_row(vehicle)
        else:
            self.combo.setCurrentText("Транспорт")
        self.status_bar.showMessage(f"Транспорт '{vehicle.vehicle_id}' добавлен", 3000)

    # Вставка строки с данными клиента в таблицу
    def add_client_row(self, client):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(client.name))
        self.table.setItem(row, 1, QTableWidgetItem(str(client.cargo_weight)))
        self.table.setItem(row, 2, QTableWidgetItem("VIP" if client.is_vip else "Обычный"))

    # Вставка строки с характеристиками транспорта в таблицу
    def add_vehicle_row(self, vehicle):
        row = self.table.rowCount()
        self.table.insertRow(row)
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

    # Активация режима редактирования выбранного индекса
    def on_cell_double_clicked(self, row, column):
        if self.combo.currentText() == "Клиенты":
            self.open_change_client()
        elif self.combo.currentText() == "Транспорт":
            self.open_change_vehicle()

    # Удаление выбранного элемента из таблицы
    def delete_selected_row(self):
        row = self.table.currentRow()
        if row == -1:
            self.status_bar.showMessage("Выберите элемент для удаления", 3000)
            return

        if self.combo.currentText() == "Клиенты":
            del self.company.clients[row]
            self.status_bar.showMessage("Клиент удален", 3000)
        elif self.combo.currentText() == "Транспорт":
            del self.company.vehicles[row]
            self.status_bar.showMessage("Транспорт удален", 3000)
        self.table.removeRow(row)

    # Обработка сигнала об изменении клиента
    def on_client_changed(self, index, name, weight, is_vip):
        self.refresh_table()
        self.status_bar.showMessage(f"Клиент '{name}' изменен", 3000)

    # Обработка сигнала об изменении транспорта
    def on_vehicle_changed(self, index, vehicle):
        self.refresh_table()
        self.status_bar.showMessage(f"Транспорт '{vehicle.vehicle_id}' изменен", 3000)

    # Запуск алгоритма распределения грузов
    def optimize_distribution(self):
        try:
            self.company.optimize_cargo_distribution()
            # Временное отключение сигналов для обновления
            self.combo.currentTextChanged.disconnect()
            self.combo.setCurrentText("Транспорт")
            self.refresh_table()
            self.combo.currentTextChanged.connect(self.on_combo_changed)
            self.status_bar.showMessage("Распределение грузов успешно завершено", 5000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка распределения: {str(e)}", 5000)

    # Обновление таблицы
    def refresh_table(self):
        self.on_combo_changed(self.combo.currentText())

    # Экспорт данных в JSON
    def export_to_json(self):
        try:
            data = {
                "clients": [{"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip} for c in self.company.clients],
                "vehicles": [{"vehicle_id": v.vehicle_id, "type": v.__class__.__name__, "capacity": v.capacity, "current_load": v.current_load} for v in self.company.vehicles]
            }
            with open("company_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Экспорт", "Данные сохранены в company_data.json")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось экспортировать данные: {e}")

if __name__ == "__main__":
    app = QApplication([])
    
    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #f5f5f5;
            color: #1a1a1a;
        }
        QPushButton {
            background-color: #ffffff;
            color: #1a1a1a;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #e8e8e8;
            border-color: #909090;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        QComboBox {
            background-color: #ffffff;
            color: #1a1a1a;
            font-size: 13px;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
            padding: 4px 8px;
        }
        QComboBox:hover {
            border-color: #909090;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #1a1a1a;
            selection-background-color: #d0d0d0;
            selection-color: #000000;
            border: 1px solid #b0b0b0;
        }
        QLineEdit {
            background-color: #ffffff;
            color: #1a1a1a;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
            font-size: 13px;
        }
        QLineEdit:focus {
            border-color: #606060;
        }
        QTableWidget {
            background-color: #ffffff;
            color: #1a1a1a;
            gridline-color: #d0d0d0;
            border: 1px solid #b0b0b0;
            border-radius: 4px;
        }
        QTableWidget::item:selected {
            background-color: #d0d0d0;
            color: #000000;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #1a1a1a;
            border: none;
            border-bottom: 1px solid #b0b0b0;
            font-weight: bold;
        }
        QCheckBox {
            color: #1a1a1a;
            font-size: 13px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 3px;
            border: 1px solid #808080;
            background-color: #ffffff;
        }
        QCheckBox::indicator:checked {
            background-color: #00FF00;
            border-color: #303030;
        }
        QCheckBox::indicator:hover {
            border-color: #505050;
        }
        QLabel {
            color: #1a1a1a;
            font-size: 13px;
        }
        QStatusBar {
            background-color: #e0e0e0;
            color: #000000;
            border-top: 1px solid #a0a0a0;
            padding: 4px;
            font-size: 13px;
        }
        QStatusBar QLabel {
            color: #000000;
        }
        QFrame[frameShape="4"], QFrame[frameShape="5"] {
            color: #b0b0b0;
        }
        QMessageBox {
            background-color: #f5f5f5;
        }
        QMessageBox QLabel {
            color: #1a1a1a;
        }
        QMessageBox QPushButton {
            min-width: 80px;
        }
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-height: 30px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }
        QScrollBar:horizontal {
            background-color: #f0f0f0;
            height: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-width: 30px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #a0a0a0;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0;
        }
    """)
    
    window = MainWindow()
    window.show()
    app.exec()
