import sys
from pathlib import Path

# Динамическое добавление корневой директории проекта в пути поиска модулей
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QTableWidgetItem, QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, \
    QTableWidget, QHeaderView, QComboBox, QLabel, QFrame, QMessageBox
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

# Импорт внутренних компонентов системы
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
    # Главное окно приложения транспортной компании

    def __init__(self):
        super().__init__()

        # Инициализация объекта компании
        self.company = TransportCompany("My Transport Company")

        # Инициализация вспомогательных окон и связывание их сигналов с методами обновления таблиц
        self.cv_window = ChangeVehicle(self.company)
        self.cv_window.vehicle_changed.connect(self.on_vehicle_changed)
        
        self.av_window = AddVehicle()
        self.av_window.vehicle_added.connect(self.add_vehicle_to_table)
        
        self.cc_window = ChangeClient(self.company)
        self.cc_window.client_changed.connect(self.on_client_changed)
        
        self.au_window = AddClient()
        self.au_window.client_added.connect(self.add_client_to_table)
        
        self.aw_window = AboutWindow()

        # Настройка параметров основного окна
        self.setWindowTitle(self.company.name)
        self.setFixedSize(1100, 700)

        # Создание центрального виджета для размещения элементов управления
        central = QWidget()
        self.setCentralWidget(central)

        # Текстовая метка выбора таблицы
        label = QLabel("Выберите таблицу:", central)
        label.setStyleSheet("QLabel{color: black; font: 15px;}")
        label.setGeometry(52, 60, 200, 20)

        # Выпадающий список для переключения между таблицами клиентов и транспортом
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

        # Кнопка для удаления выбранной строки из таблицы
        btn_delete = QPushButton("Удалить элемент", central)
        btn_delete.setGeometry(50, 130, 140, 40)
        btn_delete.clicked.connect(self.delete_selected_row)

        # Отрисовка разделительных горизонтальных линий
        for y in [170, 300, 488]:
            line_h = QFrame(central)
            line_h.setFrameShape(QFrame.Shape.HLine)
            line_h.setGeometry(20, y, 200, 30)
            line_h.setStyleSheet("color: black;")

        # Вертикальная линия между меню и таблицей
        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(145, 25, 200, 630)
        line_v.setStyleSheet("color: black;")

        # Кнопки управления данными 
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

        # Кнопка запуска автоматического распределения грузов
        btn5 = QPushButton("Распределить грузы", central)
        btn5.setGeometry(50, 440, 140, 40)
        btn5.clicked.connect(self.optimize_distribution)

        # Кнопка экспорта текущих данных в JSON
        btn6 = QPushButton("Экспорт результата", central)
        btn6.setGeometry(50, 525, 140, 40)
        btn6.clicked.connect(self.export_to_json)

        # Кнопка вызова окна информации о программе
        btn7 = QPushButton("О программе", central)
        btn7.setGeometry(50, 575, 140, 40)
        btn7.clicked.connect(self.open_about_program)

        # Настройка статус бара для уведомлений пользователя
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

        # Настройка главной таблицы для отображения данных
        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        self.table.setGeometry(325, 85, 700, 500)
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
            QTableWidget::item:selected {
                background-color: #bdbbbb;
                color: #000000;
            }
        """)
        # Настройка поведения таблицы
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    def on_combo_changed(self, text):
        # Метод переключения структуры таблицы в зависимости от выбранной категории
        try:
            self.table.setRowCount(0) # Очистка таблицы
            if text == "Клиенты":
                self.table.setColumnCount(3)
                self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
                for client in self.company.clients:
                    self.add_client_row(client)
                self.status_bar.showMessage(f"Отображено клиентов: {len(self.company.clients)}", 2000)
            elif text == "Транспорт":
                self.table.setColumnCount(6)
                self.table.setHorizontalHeaderLabels(
                    ["ID", "Тип", "Вместительность", "Текущая загрузка", "Цвет", "Название"])
                for vehicle in self.company.vehicles:
                    self.add_vehicle_row(vehicle)
                self.status_bar.showMessage(f"Отображено транспорта: {len(self.company.vehicles)}", 2000)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при загрузке таблицы: {str(e)}", 5000)

    # Методы открытия модальных окон
    def open_add_client(self):
        self.au_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.au_window.show()

    def open_change_client(self):
        self.cc_window.load_clients(self.company)
        self.cc_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cc_window.show()

    def open_add_vehicle(self):
        self.av_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.av_window.show()

    def open_change_vehicle(self):
        self.cv_window.load_vehicles(self.company)
        self.cv_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.cv_window.show()

    def open_about_program(self):
        self.aw_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.aw_window.show()

    def add_client_to_table(self, name: str, weight: float, is_vip: bool):
        # Обработка добавления нового клиента в систему
        try:
            client = Client(name, weight, is_vip)
            self.company.add_client(client)
            # Если сейчас открыта таблица транспорта, переключаем на клиентов
            if self.combo.currentText() == "Транспорт":
                self.combo.setCurrentText("Клиенты")
            else:
                self.add_client_row(client)
            self.status_bar.showMessage(f"Клиент '{name}' успешно добавлен", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при добавлении клиента: {str(e)}", 5000)

    def add_vehicle_to_table(self, vehicle):
        # Обработка добавления транспортного средства
        try:
            self.company.add_vehicle(vehicle)
            if self.combo.currentText() == "Клиенты":
                self.combo.setCurrentText("Транспорт")
            else:
                self.add_vehicle_row(vehicle)
            self.status_bar.showMessage(f"Транспорт успешно добавлен", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при добавлении транспорта: {str(e)}", 5000)

    def add_client_row(self, client):
        # Добавление одной строки в таблицу клиентов
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(client.name))
        self.table.setItem(row, 1, QTableWidgetItem(str(client.cargo_weight)))
        self.table.setItem(row, 2, QTableWidgetItem("VIP" if client.is_vip else "Обычный"))

    def add_vehicle_row(self, vehicle):
        # Визуальное добавление одной строки в таблицу транспорта 
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(vehicle.vehicle_id))
        self.table.setItem(row, 1, QTableWidgetItem(vehicle.__class__.__name__))
        self.table.setItem(row, 2, QTableWidgetItem(str(vehicle.capacity)))
        self.table.setItem(row, 3, QTableWidgetItem(str(vehicle.current_load)))
        # Заполнение полей 
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
        # Открытие окна редактирования при двойном клике на ячейку
        if self.combo.currentText() == "Клиенты":
            self.open_change_client()
        elif self.combo.currentText() == "Транспорт":
            self.open_change_vehicle()

    def delete_selected_row(self):
        # Удаление выбранного объекта из памяти компании и таблицы
        try:
            row = self.table.currentRow()
            if row == -1:
                self.status_bar.showMessage("Выберите элемент для удаления", 2000)
                return

            if self.combo.currentText() == "Клиенты":
                del self.company.clients[row]
            elif self.combo.currentText() == "Транспорт":
                del self.company.vehicles[row]
            
            self.table.removeRow(row)
            self.status_bar.showMessage("Элемент удален", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при удалении: {str(e)}", 5000)

    def on_client_changed(self, index, name, weight, is_vip):
        # Слот для обновления таблицы после изменения данных клиента
        self.refresh_table()
        self.status_bar.showMessage(f"Данные клиента '{name}' обновлены", 3000)

    def on_vehicle_changed(self, index, vehicle):
        # Слот для обновления таблицы после изменения транспорта
        self.refresh_table()
        self.status_bar.showMessage("Данные транспорта обновлены", 3000)

    def optimize_distribution(self):
        #. Метод вызова функции распределения грузов по транспорту
        try:
            if not self.company.clients or not self.company.vehicles:
                self.status_bar.showMessage("Недостаточно данных для распределения", 3000)
                return

            self.company.optimize_cargo_distribution()

            # Временное отключение сигналов 
            self.combo.currentTextChanged.disconnect()
            try:
                self.combo.setCurrentText("Транспорт")
                self.refresh_table()
            finally:
                self.combo.currentTextChanged.connect(self.on_combo_changed)

            self.status_bar.showMessage("Грузы успешно распределены по транспорту", 5000)
        except Exception as e:
            self.status_bar.showMessage(f"Ошибка при распределении: {str(e)}", 5000)

    def refresh_table(self):
        # Обновление текущей таблицы
        self.on_combo_changed(self.combo.currentText())

    def export_to_json(self):
        # Экспорт в JSON
        try:
            data = {
                "clients": [
                    {"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip}
                    for c in self.company.clients
                ],
                "vehicles": [
                    {
                        "vehicle_id": v.vehicle_id,
                        "type": v.__class__.__name__,
                        "capacity": v.capacity,
                        "current_load": v.current_load
                    }
                    for v in self.company.vehicles
                ]
            }
            with open("company_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Экспорт", "Данные успешно экспортированы в company_data.json")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка экспорта", f"Не удалось сохранить файл: {e}")


# Точка входа в приложение
if __name__ == "__main__":
    app = QApplication([])
    # Глобальная стилизация кнопок приложения
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

    # Настройка цветовой палитры интерфейса
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#d9d7d7"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
    app.setPalette(palette)
    
    app.exec() # Запуск цикла обработки событий
