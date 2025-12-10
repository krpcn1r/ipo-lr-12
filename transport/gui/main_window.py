from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QStatusBar, \
    QTableWidget, QHeaderView, QComboBox, QLabel, QFrame
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
        self.ac_window = AddClient()
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
        label.setGeometry(52, 70, 200, 20)


        combo = QComboBox(central)
        combo.setGeometry(50, 110, 140, 30)
        combo.addItems(["Клиенты", "Транспорт"])


        line_h = QFrame(central)
        line_h.setFrameShape(QFrame.Shape.HLine)
        line_h.setGeometry(20, 145, 200, 30)


        line_v = QFrame(central)
        line_v.setFrameShape(QFrame.Shape.VLine)
        line_v.setGeometry(145, 25, 200, 630)

        btn1 = QPushButton("Добавить клиента", central)
        btn1.setGeometry(50, 190, 140, 40)
        btn1.clicked.connect(self.open_add_client)

        btn2 = QPushButton("Добавить транспорт", central)
        btn2.setGeometry(50, 280, 140, 40)
        btn2.clicked.connect(self.open_add_vehicle)

        btn3 = QPushButton("Распределить грузы", central)
        btn3.setGeometry(50, 370, 140, 40)
        btn4 = QPushButton("Экспорт результата", central)
        btn4.setGeometry(50, 460, 140, 40)
        btn5 = QPushButton("О программе", central)
        btn5.setGeometry(50, 550, 140, 40)


        status = QStatusBar()
        status.setStyleSheet("""
            QStatusBar {
                background-color: #292929;
                border-top: 1px solid #2C2C2C;
                font-size: 10pt;
                padding: 3px;
                color: white;
            }
        """)
        self.setStatusBar(status)
        status.showMessage("Программа запущена")


        table = QTableWidget(20, 3, central)
        table.setHorizontalHeaderLabels(["Имя", "Вес груза", "VIP-статус"])
        table.setGeometry(325, 85 , 700, 500)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: grey;        /* тёмный фон */
                color: #f0f0f0;                   /* светлый текст */
                border-left: #ffffff;   /* серая граница слева */
                border-right: #ffffff;  /* серая граница справа */
                gridline-color: #555555;          /* цвет внутренних линий */
                selection-background-color: #444444; /* фон выделенной строки */
                selection-color: #ffffff;         /* цвет текста при выделении */
            }
        """)


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
        self.ac_window.show()
    def open_change_client(self):
        self.cc_window.show()
    def open_add_vehicle(self):
        self.av_window.show()
    def open_change_vehicle(self):
        self.cv_window.show()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()