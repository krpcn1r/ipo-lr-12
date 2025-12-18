from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent, QKeyEvent


class AddClient(QMainWindow):
    # Сигнал, который передает данные нового клиента в главное окно.
    client_added = pyqtSignal(str, float, bool)

    def __init__(self):
        super().__init__()
        # Настройка параметров окна
        self.setWindowTitle("Добавить клиента")
        self.setFixedSize(500, 220)

        # Создание центрального виджета
        central = QWidget()
        self.setCentralWidget(central)

        # Поле ввода имени клиента
        self.line_add_name = QLineEdit(central)
        self.line_add_name.setPlaceholderText("Введите имя клиента")
        self.line_add_name.setGeometry(50, 30, 375, 30)
        self.line_add_name.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: black;
                font: 15px;
            }
        """)

        # Поле ввода веса груза
        self.line_add_weight = QLineEdit(central)
        self.line_add_weight.setPlaceholderText("Введите вес груза")
        self.line_add_weight.setGeometry(50, 80, 375, 30)
        self.line_add_weight.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: black;
                font: 15px;
            }
        """)

        # Чекбокс для установки VIP-статуса
        self.check_vip = QCheckBox("VIP-клиент", central)
        self.check_vip.move(53, 130)
        self.check_vip.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
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

        # Кнопка подтверждения добавления
        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 170, 120, 40)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #adacac;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
        """)
        btn.clicked.connect(self.on_add_client)

        # Кнопка закрытия окна без сохранения
        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 170, 120, 40)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #212121;
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #adacac;
            }
            QPushButton:pressed {
                background-color: #C0C0C0;
            }
        """)
        btn_close.clicked.connect(self.close)

    # Обработка нажатия клавиш 
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    # Очистка всех полей ввода
    def clear_fields(self):
        self.line_add_name.clear()
        self.line_add_weight.clear()
        self.check_vip.setChecked(False)

    # Очищаем поля при каждом открытии
    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.clear_fields()

    # Вывода исключений при некорректном вводе
    def show_warning(self, message, field):
        QMessageBox.warning(self, "Ошибка ввода", message)
        field.clear()

    # Основная логика сбора данных и отправки сигнала
    def on_add_client(self):
        name = self.line_add_name.text().strip()
        weight_text = self.line_add_weight.text().strip()
        
        # Проверка на пустое имя
        if not name:
            self.show_warning("Имя клиента не может быть пустым", self.line_add_name)
            return
            
        # Попытка преобразования веса в число
        try:
            weight = float(weight_text)
        except ValueError:
            self.show_warning("Вес груза должен быть числом", self.line_add_weight)
            return
            
        # Получение статуса VIP и испускание сигнала
        is_vip = self.check_vip.isChecked()
        self.client_added.emit(name, weight, is_vip)
        
        self.clear_fields()
        self.close()
