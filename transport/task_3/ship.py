from transport.task_2.vehicle import Vehicle


class Ship(Vehicle):
    def __init__(self, capacity, name):
        # Вызов конструктора базового класса Vehicle для инициализации ID и грузоподъемности
        super().__init__(capacity)
        
        # Установка уникального судна
        self.name = name
