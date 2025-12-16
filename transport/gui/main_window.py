from PyQt6.QtWidgets import QTableWidgetItem, QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, \
    QTableWidget, QHeaderView, QComboBox, QLabel, QFrame
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from transport.gui.clients_gui.add_client import AddClient
from transport.gui.clients_gui.change_client import ChangeClient
from transport.gui.vehicle_gui.add_vehicle import AddVehicle
from transport.gui.vehicle_gui.change_vehicle import ChangeVehicle
from transport.gui.about_window import AboutWindow
from transport.task_3.transportCompany import TransportCompany
from transport.task_1.client import Client
import json
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.cv_window = ChangeVehicle()
        self.av_window = AddVehicle()
        self.av_window.vehicle_added.connect(self.add_vehicle_to_table)
        self.cc_window = ChangeClient()
        self.au_window = AddClient()
        self.au_window.client_added.connect(self.add_client_to_table)
        self.aw_window = AboutWindow()

        self.company = TransportCompany("My Transport Company")
        self.setWindowTitle(self.company.name)
        self.setFixedSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        label = QLabel("Выберите таблицу:", central)
        label.setStyleSheet("QLabel{color: black; font: 15px;}")
        label.setGeometry(52, 80, 200, 20)

        self.combo = QComboBox(central)
        self.combo.setGeometry(50, 120, 140, 30)
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

        for y in [155, 285, 468]:
            line_h = QFrame(central)
            line_h.setFrameShape(QFrame.Shape.HLine)
            line_h.setGeometry(20, y, 200, 30)
            line_h.setStyleSheet("color: black;")

        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(145, 25, 200, 630)
        line_v.setStyleSheet("color: black;")

        btn1 = QPushButton("Добавить клиента", central)
        btn1.setGeometry(50, 190, 140, 40)
        btn1.clicked.connect(self.open_add_client)

        btn2 = QPushButton("Изменить клиента", central)
        btn2.setGeometry(50, 240, 140, 40)
        btn2.clicked.connect(self.open_change_client)

        btn3 = QPushButton("Добавить транспорт", central)
        btn3.setGeometry(50, 320, 140, 40)
        btn3.clicked.connect(self.open_add_vehicle)

        btn4 = QPushButton("Изменить транспорт", central)
        btn4.setGeometry(50, 370, 140, 40)
        btn4.clicked.connect(self.open_change_vehicle)

        btn5 = QPushButton("Распределить грузы", central)
        btn5.setGeometry(50, 420, 140, 40)
        btn5.clicked.connect(self.optimize_distribution)

        btn6 = QPushButton("Экспорт результата", central)
        btn6.setGeometry(50, 505, 140, 40)

        btn7 = QPushButton("О программе", central)
        btn7.setGeometry(50, 555, 140, 40)
        btn7.clicked.connect(self.open_about_program)

        btn_delete = QPushButton("Удалить", central)
        btn_delete.setGeometry(50, 600, 140, 40)
        btn_delete.clicked.connect(self.delete_selected_row)

        status = QStatusBar()
        status.setStyleSheet("""
            QStatusBar {
                background-color: #F0F0F0;
                border-top: 1px solid #2C2C2C;
                font-size: 10pt;
                padding: 3px;
                color: #333333;
            }
        """)
        self.setStatusBar(status)
        status.showMessage("Программа запущена")

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
        self.table.setRowCount(0)
        if text == "Клиенты":
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
            for client in self.company.clients:
                self.add_client_row(client)
        elif text == "Транспорт":
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Тип", "Вместительность", "Текущая загрузка"])
            for vehicle in self.company.vehicles:
                self.add_vehicle_row(vehicle)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def open_add_client(self):
        self.au_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.au_window.show()

    def open_change_client(self):
        self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cc_window.show()

    def open_add_vehicle(self):
        self.av_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.av_window.show()

    def open_change_vehicle(self):
        self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cv_window.show()

    def open_about_program(self):
        self.aw_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.aw_window.show()

    def add_client_to_table(self, name: str, weight: float, is_vip: bool):
        client = Client(name, weight, is_vip)
        self.company.add_client(client)
        self.add_client_row(client)

    def add_vehicle_to_table(self, vehicle):
        self.company.add_vehicle(vehicle)
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(vehicle.vehicle_id))
        self.table.setItem(row_position, 1, QTableWidgetItem(vehicle.__class__.__name__))
        self.table.setItem(row_position, 2, QTableWidgetItem(str(vehicle.capacity)))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(vehicle.current_load)))

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

    def on_cell_double_clicked(self, row, column):
        if self.combo.currentText() == "Клиенты":
            client = self.company.clients[row]
            self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.cc_window.show()
        elif self.combo.currentText() == "Транспорт":
            vehicle = self.company.vehicles[row]
            self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.cv_window.show()

    def delete_selected_row(self):
        row = self.table.currentRow()
        if row == -1:
            return

        if self.combo.currentText() == "Клиенты":
            del self.company.clients[row]
        elif self.combo.currentText() == "Транспорт":
            del self.company.vehicles[row]

        self.table.removeRow(row)

    def optimize_distribution(self):
        self.company.optimize_cargo_distribution()
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        if self.combo.currentText() == "Клиенты":
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
            for client in self.company.clients:
                self.add_client_row(client)
        elif self.combo.currentText() == "Транспорт":
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["ID", "Тип", "Вместительность", "Текущая загрузка"])
            for vehicle in self.company.vehicles:
                self.add_vehicle_row(vehicle)


    def export_to_json(self):
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
        try:
            with open("company_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Экспорт", "Данные успешно экспортированы в company_data.json")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка экспорта", f"Не удалось сохранить файл: {e}")


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