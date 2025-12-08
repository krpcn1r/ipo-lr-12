import random


class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = f"{random.randint(100000, 999999)}"
        self.capacity = capacity
        self.current_load = 0.0
        self.clients_list = []
    
    def load_cargo(self, client):
        if type(self.current_load) and type(client.cargo_weight) is float:
            if self.current_load + client.cargo_weight <= self.capacity:
                self.current_load += client.cargo_weight
                return self.current_load
        return None

    def __str__(self):
        return f"ID: {self.vehicle_id}, capacity: {self.capacity}, current_load: {self.current_load}"
