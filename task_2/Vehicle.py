import random

from Client import Client


class Vehicle:
    vehicle_id = str(random.randint(10000, 99999))
    capacity = 0.0
    current_load = 0.0
    clients_list = []

    def load_cargo(self, client):
        client = Client()
        if client.cargo_weight + self.current_load < self.capacity:
            self.current_load = client.cargo_weight
            if client.name is str:
                self.clients_list.append(client.name)

    def __str__(self):
        return f"ID: {self.vehicle_id}, capacity: {self.capacity}, current_load: {self.current_load}"
