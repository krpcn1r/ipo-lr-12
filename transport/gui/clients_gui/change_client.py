from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class ChangeClient(QMainWindow):
    client_changed = pyqtSignal(int, str, float, bool)  # индекс + новые данные

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Изменить клиента")
        self.setFixedSize(500, 250)

        central = QWidget()
        self.setCentralWidget(central)

        self.line_name = QLineEdit(central)
        self.line_name.setGeometry(50, 30, 375, 30)
        self.line_name.setPlaceholderText("Имя клиента")
        self.line_name.setStyleSheet("QLineEdit{background:#fff; font:15px; color: black}")

        self.line_weight = QLineEdit(central)
        self.line_weight.setGeometry(50, 80, 375, 30)
        self.line_weight.setPlaceholderText("Вес груза")
        self.line_weight.setStyleSheet("QLineEdit{background:#fff; font:15px;; color: black}}")

        self.check_vip = QCheckBox("VIP-клиент", central)
        self.check_vip.move(53, 130)
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

        btn_save = QPushButton("Сохранить", central)
        btn_save.setGeometry(50, 180, 120, 40)
        btn_save.clicked.connect(self.on_save)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 180, 120, 40)
        btn_close.clicked.connect(self.close)

        self.index = None

    def load_client(self, client, index):
        self.index = index
        self.line_name.setText(client.name)
        self.line_weight.setText(str(client.cargo_weight))
        self.check_vip.setChecked(client.is_vip)

    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    def on_save(self):
        name = self.line_name.text().strip()
        weight_text = self.line_weight.text().strip()

        if not name or len(name) < 2 or not name.isalpha():
            self.show_warning("Имя должно содержать минимум 2 буквы", self.line_name)
            return
        try:
            weight = float(weight_text)
            if weight <= 0 or weight > 10000:
                self.show_warning("Вес должен быть >0 и ≤10000", self.line_weight)
                return
        except ValueError:
            self.show_warning("Вес должен быть числом", self.line_weight)
            return

        is_vip = self.check_vip.isChecked()
        self.client_changed.emit(self.index, name, weight, is_vip)
        self.close()
