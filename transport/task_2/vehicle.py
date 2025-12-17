import random


class Vehicle:
    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Вместительность должна быть положительным числом")
        self.vehicle_id = str(random.randint(100000, 999999))
        self.capacity = float(capacity)
        self.current_load = 0.0
        self.clients_list = []

    def load_cargo(self, client):
        if client is None:
            raise ValueError("Клиент не может быть None")
        if not hasattr(client, 'cargo_weight'):
            raise ValueError("Клиент должен иметь атрибут cargo_weight")
        if not isinstance(client.cargo_weight, (int, float)) or client.cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом")
        if self.current_load + client.cargo_weight <= self.capacity:
            self.current_load += client.cargo_weight
            return self.current_load
        return None

    def __str__(self):
        return f"ID: {self.vehicle_id}, capacity: {self.capacity}, current_load: {self.current_load}"
