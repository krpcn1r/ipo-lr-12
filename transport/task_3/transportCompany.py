from transport.task_1.client import Client
from transport.task_2.vehicle import Vehicle


class TransportCompany:
    def __init__(self, name):
        # Инициализация компании с названием и пустыми списками транспорта и клиентов
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        # Регистрация нового транспортного средства с проверкой на соответствие базовому классу
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Должен быть классом Vehicle или наследуемым классом")
        self.vehicles.append(vehicle)

    def list_vehicles(self):
        return self.vehicles

    def add_client(self, client):
        # Добавление клиента в список ожидания на отправку груза
        if not isinstance(client, Client):
            raise TypeError("Должен быть классом Client")
        self.clients.append(client)

    def optimize_cargo_distribution(self):
        # Проверка наличия ресурсов для выполнения операции распределения
        if not self.vehicles:
            return
        if not self.clients:
            return

        # Сброс текущей загрузки всех машин перед новым циклом распределения
        for vehicle in self.vehicles:
            vehicle.current_load = 0.0
            vehicle.clients_list = []

        # Сортировка: сначала VIP-клиенты, затем по убыванию веса груза для плотной упаковки
        sorted_clients = sorted(
            self.clients,
            key=lambda c: (not c.is_vip, -c.cargo_weight)
        )

        for client in sorted_clients:
            if client is None:
                continue
            best_vehicle = None
            min_remaining_capacity = float('inf')

            # Поиск наиболее подходящего транспорта 
            for vehicle in self.vehicles:
                if vehicle is None:
                    continue
                remaining_capacity = vehicle.capacity - vehicle.current_load
                if remaining_capacity >= client.cargo_weight:
                    if remaining_capacity < min_remaining_capacity:
                        min_remaining_capacity = remaining_capacity
                        best_vehicle = vehicle

            # Оформление груза на найденный транспорт и добавление клиента
            if best_vehicle is not None:
                try:
                    result = best_vehicle.load_cargo(client)
                    if result is not None:
                        best_vehicle.clients_list.append(client)
                except (ValueError, AttributeError):
                    continue
