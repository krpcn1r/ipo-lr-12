import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QTableWidgetItem, QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, \
    QTableWidget, QHeaderView, QComboBox, QLabel, QFrame, QMessageBox
from PyQt6.QtGui import QPalette, QColor
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

        self.company = TransportCompany("My Transport Company")

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
        label.setStyleSheet("QLabel{color: black; font: 15px;}")
        label.setGeometry(52, 60, 200, 20)

        self.combo = QComboBox(central)
        self.combo.setGeometry(50, 90, 140, 30)
        self.combo.addItems(["Клиенты", "Транспорт"])
        self.combo.setStyleSheet("""
            QComboBox{
                background-color: #ffffff;
                color: black;
            }
            QComboBox QAbstractItemView {
                color: black;             
                background-color: #ffffff;   
                selection-background-color: #bdbbbb;
                selection-color: #bdbbbb;  
            }
        """)
        self.combo.currentTextChanged.connect(self.on_combo_changed)

        btn_delete = QPushButton("Удалить элемент", central)
        btn_delete.setGeometry(50, 130, 140, 40)
        btn_delete.clicked.connect(self.delete_selected_row)

        for y in [170, 300, 488]:
            line_h = QFrame(central)
            line_h.setFrameShape(QFrame.Shape.HLine)
            line_h.setGeometry(20, y, 200, 30)
            line_h.setStyleSheet("color: black;")

        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(145, 25, 200, 630)
        line_v.setStyleSheet("color: black;")

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

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #F0F0F0;
                border-top: 1px solid #2C2C2C;
                font-size: 10pt;
                padding: 3px;
                color: #333333;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Программа запущена")

        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        self.table.setGeometry(325, 85, 700, 500)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("""
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
                background-color: #D5D5D5;
                color: #212121;
                border: 1px solid #BDBDBD;
            }
            QTableWidget::item:selected {
                background-color: #bdbbbb;
                color: #000000;
            }
        """)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    def on_combo_changed(self, text):
        try:
            self.table.setRowCount(0)
            if text == "Клиенты":
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
                for client in self.company.clients:
                    self.add_client_row(client)
                count = len(self.company.clients)
                self.status_bar.showMessage(f"Отображено клиентов: {count}", 2000)
            elif text == "Транспорт":
                self.table.setColumnCount(6)
                self.table.setHorizontalHeaderLabels(
                    ["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
                for vehicle in self.company.vehicles:
                    self.add_vehicle_row(vehicle)
                count = len(self.company.vehicles)
                self.status_bar.showMessage(f"Отображено транспорта: {count}", 2000)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при загрузке таблицы: {str(e)}", 5000)

    def open_add_client(self):
        try:
            self.au_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.au_window.show()
            self.status_bar.showMessage("Окно добавления клиента открыто", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при открытии окна: {str(e)}", 5000)

    def open_change_client(self):
        try:
            self.cc_window.load_clients(self.company)
            self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.cc_window.show()
            self.status_bar.showMessage("Окно изменения клиентов открыто", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при открытии окна: {str(e)}", 5000)

    def open_add_vehicle(self):
        try:
            self.av_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.av_window.show()
            self.status_bar.showMessage("Окно добавления транспорта открыто", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при открытии окна: {str(e)}", 5000)

    def open_change_vehicle(self):
        try:
            self.cv_window.load_vehicles(self.company)
            self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.cv_window.show()
            self.status_bar.showMessage("Окно изменения транспорта открыто", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при открытии окна: {str(e)}", 5000)

    def open_about_program(self):
        self.aw_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.aw_window.show()

    def add_client_to_table(self, name: str, weight: float, is_vip: bool):
        try:
            client = Client(name, weight, is_vip)
            self.company.add_client(client)
            if self.combo.currentText() == "Транспорт":
                self.combo.setCurrentText("Клиенты")
            else:
                self.add_client_row(client)
            self.status_bar.showMessage(f"Клиент '{name}' успешно добавлен", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при добавлении клиента: {str(e)}", 5000)

    def add_vehicle_to_table(self, vehicle):
        try:
            self.company.add_vehicle(vehicle)
            vehicle_name = vehicle.name if isinstance(vehicle, Ship) else (
                vehicle.color if isinstance(vehicle, Truck) else vehicle.vehicle_id)
            vehicle_type = vehicle.__class__.__name__
            if self.combo.currentText() == "Клиенты":
                self.combo.setCurrentText("Транспорт")
            else:
                self.add_vehicle_row(vehicle)
            self.status_bar.showMessage(f"Транспорт '{vehicle_type}' (ID: {vehicle.vehicle_id}) успешно добавлен", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при добавлении транспорта: {str(e)}", 5000)

    def add_client_row(self, client):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(client.name))
        self.table.setItem(row, 1, QTableWidgetItem(str(client.cargo_weight)))
        self.table.setItem(row, 2, QTableWidgetItem("VIP" if client.is_vip else "Обычный"))

    def add_vehicle_row(self, vehicle):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(vehicle.vehicle_id))
        self.table.setItem(row, 1, QTableWidgetItem(vehicle.__class__.__name__))
        self.table.setItem(row, 2, QTableWidgetItem(str(vehicle.capacity)))
        self.table.setItem(row, 3, QTableWidgetItem(str(vehicle.current_load)))
        if isinstance(vehicle, Truck):
            self.table.setItem(row, 4, QTableWidgetItem(vehicle.color))
            self.table.setItem(row, 5, QTableWidgetItem("-"))
        elif isinstance(vehicle, Ship):
            self.table.setItem(row, 4, QTableWidgetItem("-"))
            self.table.setItem(row, 5, QTableWidgetItem(vehicle.name))
        else:
            self.table.setItem(row, 4, QTableWidgetItem("-"))
            self.table.setItem(row, 5, QTableWidgetItem("-"))

    def on_cell_double_clicked(self, row, column):
        if self.combo.currentText() == "Клиенты":
            self.cc_window.load_clients(self.company)
            self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.cc_window.show()
        elif self.combo.currentText() == "Транспорт":
            self.cv_window.load_vehicles(self.company)
            self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.cv_window.show()

    def delete_selected_row(self):
        try:
            row = self.table.currentRow()
            if row == -1:
                self.status_bar.showMessage("Выберите элемент для удаления", 2000)
                return

            if self.combo.currentText() == "Клиенты":
                client_name = self.company.clients[row].name
                del self.company.clients[row]
                self.table.removeRow(row)
                self.status_bar.showMessage(f"Клиент '{client_name}' успешно удален", 3000)
            elif self.combo.currentText() == "Транспорт":
                vehicle_id = self.company.vehicles[row].vehicle_id
                vehicle_type = self.company.vehicles[row].__class__.__name__
                del self.company.vehicles[row]
                self.table.removeRow(row)
                self.status_bar.showMessage(f"Транспорт '{vehicle_type}' (ID: {vehicle_id}) успешно удален", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при удалении: {str(e)}", 5000)

    def on_client_changed(self, index, name, weight, is_vip):
        try:
            self.refresh_table()
            self.status_bar.showMessage(f"Данные клиента '{name}' успешно сохранены", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при сохранении клиента: {str(e)}", 5000)

    def on_vehicle_changed(self, index, vehicle):
        try:
            self.refresh_table()
            vehicle_type = vehicle.__class__.__name__
            self.status_bar.showMessage(
                f"Данные транспорта '{vehicle_type}' (ID: {vehicle.vehicle_id}) успешно сохранены", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при сохранении транспорта: {str(e)}", 5000)

    def optimize_distribution(self):
        try:
            if not self.company.clients:
                self.status_bar.showMessage("Нет клиентов для распределения", 3000)
                return
            if not self.company.vehicles:
                self.status_bar.showMessage("Нет транспорта для распределения грузов", 3000)
                return

            self.company.optimize_cargo_distribution()

            self.combo.currentTextChanged.disconnect()
            try:
                self.combo.setCurrentText("Транспорт")

                self.table.setRowCount(0)
                self.table.setColumnCount(6)
                self.table.setHorizontalHeaderLabels(
                    ["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
                for vehicle in self.company.vehicles:
                    self.add_vehicle_row(vehicle)
                self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

                self.table.update()
                self.table.repaint()
            finally:
                self.combo.currentTextChanged.connect(self.on_combo_changed)

            used_vehicles = sum(1 for v in self.company.vehicles if v.current_load > 0)
            total_clients = len(self.company.clients)
            loaded_clients = sum(len(v.clients_list) for v in self.company.vehicles)

            status_msg = f"Распределение завершено: {loaded_clients}/{total_clients} клиентов загружено"
            if used_vehicles > 0:
                status_msg += f" в {used_vehicles} транспорт(а)"
            else:
                status_msg += " (нет подходящего транспорта)"

            load_details = []
            for v in self.company.vehicles:
                load_details.append(f"ID {v.vehicle_id}: {v.current_load:.1f}/{v.capacity:.1f}")
            if load_details:
                status_msg += f" | {'; '.join(load_details)}"

            self.status_bar.showMessage(status_msg, 5000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при распределении грузов: {str(e)}", 5000)

    def refresh_table(self):
        try:
            self.table.setRowCount(0)
            if self.combo.currentText() == "Клиенты":
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
                for client in self.company.clients:
                    self.add_client_row(client)
            elif self.combo.currentText() == "Транспорт":
                self.table.setColumnCount(6)
                self.table.setHorizontalHeaderLabels(
                    ["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
                for vehicle in self.company.vehicles:
                    self.add_vehicle_row(vehicle)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при обновлении таблицы: {str(e)}", 5000)

    def export_to_json(self):
        try:
            data = {
                "clients": [
                    {
                        "name": client.name,
                        "cargo_weight": client.cargo_weight,
                        "is_vip": client.is_vip
                    }
                    for client in self.company.clients
                ],
                "vehicles": [
                    {
                        "vehicle_id": vehicle.vehicle_id,
                        "type": vehicle.__class__.__name__,
                        "capacity": vehicle.capacity,
                        "current_load": vehicle.current_load
                    }
                    for vehicle in self.company.vehicles
                ]
            }
            with open("company_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Экспорт", "Данные успешно экспортированы в company_data.json")
            self.status_bar.showMessage("Данные успешно экспортированы в company_data.json", 3000)
        except Exception as e:
            error_msg = f"Ошибка экспорта: {str(e)}"
            QMessageBox.warning(self, "Ошибка экспорта", f"Не удалось сохранить файл: {e}")
            self.status_bar.showMessage(error_msg, 5000)


app = QApplication([])
app.setStyleSheet(""" 
    QPushButton { 
        background-color: #ffffff;
        color: #212121;
        border: 1px solid #BDBDBD;
        border-radius: 4px; padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #adacac 
    } 
    QPushButton:pressed {
        background-color: #C0C0C0; 
    } """)

window = MainWindow()
window.show()
palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor("#d9d7d7"))
palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
app.setPalette(palette)
app.exec()

