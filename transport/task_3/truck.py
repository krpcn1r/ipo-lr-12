from transport.task_2.vehicle import Vehicle


class Truck(Vehicle):
    def __init__(self, capacity, color):
        # Инициализация базовых свойств транспорта через родительский класс
        super().__init__(capacity)
        
        # Установка цвета 
        self.color = color
