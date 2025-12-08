from transport.task_2.vehicle import Vehicle


class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        self.color = color
