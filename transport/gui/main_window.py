from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QStatusBar, \
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLabel, QFrame
import sys


from transport.task_3.transportCompany import TransportCompany

class MainWindow(QMainWindow):

    def __init__(self):
        company = TransportCompany("My Transport Company")
        super().__init__()
        self.setWindowTitle(company.name)
        self.setFixedSize(1100, 700)


        central = QWidget()
        self.setCentralWidget(central)


        label = QLabel("Выберите таблицу:", central)
        label.setStyleSheet("""
        QLabel{
            color: white;
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
        btn2 = QPushButton("Добавить транспорт", central)
        btn2.setGeometry(50, 280, 140, 40)
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
                background-color: #2b2b2b;        /* тёмный фон */
                color: #f0f0f0;                   /* светлый текст */
                border-left: solid #ffffff;   /* серая граница слева */
                border-right: solid #ffffff;  /* серая граница справа */
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

app = QApplication([])
window = MainWindow()
window.show()
app.exec()