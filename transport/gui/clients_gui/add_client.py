from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent, QKeyEvent

class AddClient(QMainWindow):
    client_added = pyqtSignal(str, float, bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(500, 220)

        central = QWidget()
        self.setCentralWidget(central)

        self.line_add_name = QLineEdit(central)
        self.line_add_name.setPlaceholderText("Введите имя клиента")
        self.line_add_name.setGeometry(50, 30, 375, 30)

        self.line_add_weight = QLineEdit(central)
        self.line_add_weight.setPlaceholderText("Введите вес груза")
        self.line_add_weight.setGeometry(50, 80, 375, 30)

        self.check_vip = QCheckBox("VIP-клиент", central)
        self.check_vip.move(53, 130)
        self.check_vip.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 170, 120, 40)
        btn.clicked.connect(self.on_add_client)

        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 170, 120, 40)
        btn_close.clicked.connect(self.close)

    # Закрытие окна при нажатии Escape
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    # Очистка полей 
    def clear_fields(self):
        self.line_add_name.clear()
        self.line_add_weight.clear()
        self.check_vip.setChecked(False)

    # Сброс состояния формы при отображении окна
    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.clear_fields()

    # Отображение ошибки 
    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    # Добавление клиента
    def on_add_client(self):
        name = self.line_add_name.text().strip()
        weight_text = self.line_add_weight.text().strip()
        
        # Проводим проверку поля на наличие данных
        if not name:
            self.show_warning("Имя клиента не может быть пустым", self.line_add_name)
            return
            
        # Преобразование строки в float 
        try:
            weight = float(weight_text)
        except ValueError:
            # Обрабатываем ошибку при обнаружении невалидного формата данных
            self.show_warning("Вес груза должен быть числом", self.line_add_weight)
            return
            
        # Проверяем состояние чекбокса
        is_vip = self.check_vip.isChecked()
        
        # Выполняем передачу сигнала с аргументами
        self.client_added.emit(name, weight, is_vip)
        
        # Закрываем окно и очищаем поля
        self.clear_fields()
        self.close()
