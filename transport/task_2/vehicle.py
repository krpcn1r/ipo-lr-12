import random


class Vehicle:
    def __init__(self, capacity):
        # Проверка входных данных для грузоподъемности
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Вместительность должна быть положительным числом")
        
        # Генерация уникального шестизначного ID
        self.vehicle_id = str(random.randint(100000, 999999))
        self.capacity = float(capacity)
        
        # Инициализация текущей загрузки и списка клиентов
        self.current_load = 0.0
        self.clients_list = []

    def load_cargo(self, client):
        # Проверка входного объекта и его атрибутов перед выполнением погрузки
        if client is None:
            raise ValueError("Клиент не может быть None")
        if not hasattr(client, 'cargo_weight'):
            raise ValueError("Клиент должен иметь атрибут cargo_weight")
        if not isinstance(client.cargo_weight, (int, float)) or client.cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом")
        
        # Проверка наличия свободного места
        if self.current_load + client.cargo_weight <= self.capacity:
            self.current_load += client.cargo_weight
            return self.current_load
        
        return None

    def __str__(self):
        # Формирование строки для удобного вывода в консоль
        return f"ID: {self.vehicle_id}, capacity: {self.capacity}, current_load: {self.current_load}"
