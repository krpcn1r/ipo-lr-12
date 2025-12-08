from transport.task_1.client import Client
from transport.task_3.ship import Ship
from transport.task_3.truck import Truck
from transport.task_3.transportCompany import TransportCompany
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import sys

company = TransportCompany("My Transport Company")


def main():
    while True:
        print("\n=== Транспортная компания ===")
        print(">> 1. Добавить клиента")
        print(">> 2. Добавить транспортное средство")
        print(">> 3. Показать список клиентов")
        print(">> 4. Показать список транспортных средств")
        print(">> 5. Оптимизировать распределение грузов")
        print(">> 6. Выйти")

        choice = int(input("Выберите пункт: "))

        match choice:
            case 1:
                name = input("Введите имя клиента: ")
                weight = float(input("Введите вес груза (т): "))
                vip = input("VIP клиент? (y/n): ").lower() == "y"
                client = Client(name, weight, vip)
                company.add_client(client)
                print(f"Клиент {name} добавлен.")
            case 2:
                print("Выберите тип транспорта:")
                print("1. Судно")
                print("2. Грузовик")
                sub_choice = input("Ваш выбор: ")

                capacity = float(input("Введите грузоподъемность (т): "))

                if sub_choice == "1":
                    name = input("Введите название судна: ")
                    ship = Ship(capacity, name)
                    company.add_vehicle(ship)
                    print(f"Судно {name} добавлено.")
                elif sub_choice == "2":
                    color = input("Введите цвет грузовика: ")
                    truck = Truck(capacity, color)
                    company.add_vehicle(truck)
                    print(f"Грузовик {color} добавлен.")
                else:
                    print("Неверный выбор.")
            case 3:
                if not company.clients:
                    print("Список клиентов пуст.")
                else:
                    print("\n--- Клиенты ---")
                    for c in company.clients:
                        status = "VIP" if c.is_vip else "Обычный"
                        print(f"{c.name}, груз: {c.cargo_weight}т, статус: {status}")

            case 4:
                if not company.vehicles:
                    print("Список транспортных средств пуст.")
                else:
                    print("\n--- Транспорт ---")
                    for v in company.vehicles:
                        print(v)

            case 5:
                company.optimize_cargo_distribution()
                print("\n--- Результат распределения ---")
                for v in company.vehicles:
                    print(v)
                    if v.clients_list:
                        for c in v.clients_list:
                            print(f"   - {c.name}, груз: {c.cargo_weight}т")
                    else:
                        print("   (пусто)")

            case 6:
                print("Выход из программы...")
                break

            case _:
                print("Неверный пункт меню.")


def gui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle(f"{company.name}")
    window.setGeometry(100, 100, 600, 400)

    btn1 = QPushButton("Экспорт результата")

    btn2 = QPushButton("О программе")

    btn3 = QPushButton("Добавить клиента")

    btn4 = QPushButton("Добавить транспорт")

    btn5 = QPushButton("Распределить грузы")


    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    gui()
