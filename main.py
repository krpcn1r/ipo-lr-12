from transport.task_1.client import Client
from transport.task_3.ship import Ship
from transport.task_3.truck import Truck
from transport.task_3.transportCompany import TransportCompany
import sys

# Инициализация объекта компании
company = TransportCompany("My Transport Company")


def main():
    while True:
        # Основное меню взаимодействия с пользователем 
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
                # Создание клинта
                name = input("Введите имя клиента: ")
                weight = float(input("Введите вес груза (т): "))
                vip = input("VIP клиент? (y/n): ").lower() == "y"
                client = Client(name, weight, vip)
                company.add_client(client)
                print(f"Клиент {name} добавлен.")
            case 2:
                # Создание различных типов транспорта (Судно или Грузовик)
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
                # Вывод списка клиентов компании
                if not company.clients:
                    print("Список клиентов пуст.")
                else:
                    print("\n--- Клиенты ---")
                    for c in company.clients:
                        status = "VIP" if c.is_vip else "Обычный"
                        print(f"{c.name}, груз: {c.cargo_weight}т, статус: {status}")

            case 4:
                # Вывод списка транспорта компании
                if not company.vehicles:
                    print("Список транспортных средств пуст.")
                else:
                    print("\n--- Транспорт ---")
                    for v in company.vehicles:
                        print(v)

            case 5:
                # Вызов фукнции для распределения грузов
                company.optimize_cargo_distribution()
                print("\n--- Результат распределения ---")
                for v in company.vehicles:
                    print(v)
                    if v.clients_list:
                        for c in v.clients_list:
                            print(f"    - {c.name}, груз: {c.cargo_weight}т")
                    else:
                        print("    (пусто)")

            case 6:
                print("Выход из программы...")
                break

            case _:
                print("Неверный пункт меню.")



if __name__ == "__main__":
    # Точка входа в программу
    main()
