from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, \
    QTableWidget, QHeaderView, QComboBox, QLabel, QFrame
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from transport.gui.clients_gui.add_client import AddClient
from transport.gui.clients_gui.change_client import ChangeClient
from transport.gui.vehicle_gui.add_vehicle import AddVehicle
from transport.gui.vehicle_gui.change_vehicle import ChangeVehicle


from transport.task_3.transportCompany import TransportCompany

class MainWindow(QMainWindow):

    def __init__(self):
        self.cv_window = ChangeVehicle()
        self.av_window = AddVehicle()
        self.cc_window = ChangeClient()
        self.au_window = AddClient()
        company = TransportCompany("My Transport Company")
        super().__init__()
        self.setWindowTitle(company.name)
        self.setFixedSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)

        label = QLabel("Выберите таблицу:", central)
        label.setStyleSheet("""
        QLabel{
            color: black;
            font: 15px;
        }
        """)
        label.setGeometry(52, 80, 200, 20)


        combo = QComboBox(central)
        combo.setGeometry(50, 120, 140, 30)
        combo.addItems(["Клиенты", "Транспорт"])
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

        line_h = QFrame(central)
        line_h.setFrameShape(QFrame.Shape.HLine)
        line_h.setGeometry(20, 155, 200, 30)
        line_h.setStyleSheet("color: black;")

        line_h2 = QFrame(central)
        line_h2.setFrameShape(QFrame.Shape.HLine)
        line_h2.setGeometry(20, 285, 200, 30)
        line_h2.setStyleSheet("color: black;")

        line_h3 = QFrame(central)
        line_h3.setFrameShape(QFrame.Shape.HLine)
        line_h3.setGeometry(20, 468, 200, 30)
        line_h3.setStyleSheet("color: black;")

        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(145, 25, 200, 630)
        line_v.setStyleSheet("color: black;")

        btn1 = QPushButton("Добавить клиента", central)
        btn1.setGeometry(50, 190, 140, 40)
        btn1.clicked.connect(self.open_add_client)

        btn2 = QPushButton("Изменить клиента", central)
        btn2.setGeometry(50, 240, 140, 40)

        btn3 = QPushButton("Добавить транспорт", central)
        btn3.setGeometry(50, 320, 140, 40)
        btn3.clicked.connect(self.open_add_vehicle)

        btn4 = QPushButton("Изменить транспорт", central)
        btn4.setGeometry(50, 370, 140, 40)

        btn5 = QPushButton("Распределить грузы", central)
        btn5.setGeometry(50, 420, 140, 40)

        btn6 = QPushButton("Экспорт результата", central)
        btn6.setGeometry(50, 505, 140, 40)

        btn7 = QPushButton("О программе", central)
        btn7.setGeometry(50, 555, 140, 40)

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


        table = QTableWidget(0, 3, central)
        table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        table.setGeometry(325, 85 , 700, 500)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
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
                background-color: #D5D5D5;   /* фон редактора */
                color: #212121;              /* цвет текста редактора */
                border: 1px solid #BDBDBD;   /* рамка редактора */
            }
            QTableWidget::item:selected {
            background-color: #bdbbbb;   
            color: #000000;             
        }
        """)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        def on_combo_changed(text):
            if text == "Клиенты":
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
            elif text == "Транспорт":
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["ID", "Тип", "Вместительность", "Текущая загрузка"])

            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        combo.currentTextChanged.connect(on_combo_changed)

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

app = QApplication([])

app.setStyleSheet("""
QPushButton {
    background-color: #ffffff;
    color: #212121;
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 6px 12px;
}
QPushButton:hover {
    background-color: #adacac
}
QPushButton:pressed {
    background-color: #C0C0C0;
}
""")

window = MainWindow()
window.show()
palette = QPalette()
palette.setColor(QPalette.ColorRole.Window, QColor("#d9d7d7"))
palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
app.setPalette(palette)
app.exec()