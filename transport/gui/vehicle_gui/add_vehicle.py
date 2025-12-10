from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QComboBox, QLineEdit
import sys

class AddVehicle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить транспорт")
        self.setFixedSize(500, 250)

        central = QWidget()
        self.setCentralWidget(central)
        label = QLabel("Выберите тип транспорта:", central)
        label.move(50, 20)
        label.setStyleSheet("""
        QLabel{
            color: black;
            font: 15px;
        }
        """)

        combo = QComboBox(central)
        combo.setGeometry(50, 50, 140, 30)
        combo.addItems(["Грузовик", "Судно"])
        combo.setStyleSheet("""
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

        line_capacity = QLineEdit(central)
        line_capacity.setPlaceholderText("Введите вместительность")
        line_capacity.setGeometry(50, 100, 375, 30)
        line_capacity.setStyleSheet("""
        QLineEdit{
            background-color: #ffffff;
            color: black;
            font: 15px;
        }
        """)

        line_name = QLineEdit(central)
        line_name.setPlaceholderText("Введите имя")
        line_name.setGeometry(50, 150, 375, 30)
        line_name.setStyleSheet("""
        QLineEdit{
            background-color: #ffffff;
            color: black;
            font: 15px;
        }
        """)
        line_color = QLineEdit(central)
        line_color.hide()

        btn = QPushButton("Добавить", central)
        btn.setGeometry(50, 200, 120, 40)
        btn_close = QPushButton("Закрыть", central)
        btn_close.setGeometry(330, 200, 120, 40)
        btn_close.clicked.connect(self.close)

        def on_combo_changed(text):
            if text == "Грузовик":
                line_color.hide()
                line_name.setPlaceholderText("Введите имя")
                line_name.setGeometry(50, 150, 375, 30)
                line_name.show()
            elif text == "Судно":
                line_name.hide()
                line_color.setPlaceholderText("Введите цвет")
                line_color.setGeometry(50, 150, 375, 30)
                line_color.setStyleSheet("""
                QLineEdit{
                    background-color: #ffffff;
                    color: black;
                    font: 15px;
                }
                """)
                line_color.show()
        combo.currentTextChanged.connect(on_combo_changed)

