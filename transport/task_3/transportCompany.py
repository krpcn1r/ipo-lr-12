from transport.task_1.client import Client
from transport.task_2.vehicle import Vehicle


class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Должен быть классов Vehicle или наследуемым классом")
        self.vehicles.append(vehicle)

    def list_vehicles(self):
        return self.vehicles

    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Должен быть классом Client")
        self.clients.append(client)

    def optimize_cargo_distribution(self):
        sorted_clients = sorted(self.clients, key=lambda c: not c.is_vip)
        for client in sorted_clients:
            for vehicle in sorted(self.vehicles, key=lambda v: v.current_load):
                try:
                    vehicle.load_cargo(client)
                    break
                except ValueError:
                    continue
