from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QCheckBox, QMessageBox, QTableWidget, \
    QTableWidgetItem, QHeaderView, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent


class ChangeClient(QMainWindow):
    client_changed = pyqtSignal(int, str, float, bool)

    def __init__(self, company=None):
        super().__init__()
        self.company = company
        self.setWindowTitle("Изменить клиента")
        self.setFixedSize(600, 500)

        central = QWidget()
        self.setCentralWidget(central)

        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        self.table.setGeometry(20, 20, 560, 350)
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
            QTableWidget::item:selected {
                background-color: #bdbbbb;
                color: #000000;
            }
        """)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)

        self.edit_widget = QWidget(central)
        self.edit_widget.setGeometry(20, 380, 560, 80)
        self.edit_widget.hide()

        self.line_name = QLineEdit(self.edit_widget)
        self.line_name.setGeometry(10, 0, 200, 30)
        self.line_name.setPlaceholderText("Имя клиента")
        self.line_name.setStyleSheet("QLineEdit{background:#fff; font:15px; color: black}")

        self.line_weight = QLineEdit(self.edit_widget)
        self.line_weight.setGeometry(220, 0, 150, 30)
        self.line_weight.setPlaceholderText("Вес груза")
        self.line_weight.setStyleSheet("QLineEdit{background:#fff; font:15px; color: black}")

        self.check_vip = QCheckBox("VIP-клиент", self.edit_widget)
        self.check_vip.move(380, 5)
        self.check_vip.setStyleSheet("""
            QCheckBox {
                font: 15px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border-radius: 6.7px;       
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50; 
                border: 2px solid #2E7D32;  
            }
            QCheckBox::indicator:unchecked {
                background-color: #FFFFFF;
                border: 2px solid #333333;   
            }
        """)

        btn_save = QPushButton("Сохранить", self.edit_widget)
        btn_save.setGeometry(480, 0, 70, 30)
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 6px 12px;
            }
        """)
        btn_save.clicked.connect(self.on_save)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(460, 450, 120, 40)
        btn_close.clicked.connect(self.close)

        self.current_index = None

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def load_clients(self, company):
        self.company = company
        if company is None or not hasattr(company, 'clients'):
            return

        clients_list = company.clients
        self.table.setRowCount(0)
        for idx, client in enumerate(clients_list):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(client.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(client.cargo_weight)))
            self.table.setItem(row, 2, QTableWidgetItem("VIP" if client.is_vip else "Обычный"))

    def on_cell_double_clicked(self, row, column):
        if self.company is None:
            return

        clients_list = self.company.clients if hasattr(self.company, 'clients') else []
        if row < len(clients_list):
            self.current_index = row
            client = clients_list[row]
            self.load_client(client, row)
            self.edit_widget.show()

    def load_client(self, client, index):
        self.current_index = index
        self.line_name.setText(client.name)
        self.line_weight.setText(str(client.cargo_weight))
        self.check_vip.setChecked(client.is_vip)

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    def on_save(self):
        if self.current_index is None or self.company is None:
            return

        name = self.line_name.text().strip()
        weight_text = self.line_weight.text().strip()

        if not name or len(name) < 2 or not name.isalpha():
            self.show_warning("Имя должно содержать минимум 2 буквы", self.line_name)
            return
        try:
            weight = float(weight_text)
            if weight <= 0 or weight > 10000:
                self.show_warning("Вес должен быть >0 и <10000", self.line_weight)
                return
        except ValueError:
            self.show_warning("Вес должен быть числом", self.line_weight)
            return

        is_vip = self.check_vip.isChecked()

        clients_list = self.company.clients if hasattr(self.company, 'clients') else []
        if self.current_index < len(clients_list):
            clients_list[self.current_index].name = name
            clients_list[self.current_index].cargo_weight = weight
            clients_list[self.current_index].is_vip = is_vip

            self.table.setItem(self.current_index, 0, QTableWidgetItem(name))
            self.table.setItem(self.current_index, 1, QTableWidgetItem(str(weight)))
            self.table.setItem(self.current_index, 2, QTableWidgetItem("VIP" if is_vip else "Обычный"))

            self.client_changed.emit(self.current_index, name, weight, is_vip)

            self.edit_widget.hide()
            self.current_index = None
            QMessageBox.information(self, "Успех", "Клиент успешно изменен")
