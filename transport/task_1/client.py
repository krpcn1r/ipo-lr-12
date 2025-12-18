class Client:
    def __init__(self, name, cargo_weight, is_vip):
        # Инициализация имени клиента
        self.name = name
        
        # Установка веса груза в тоннах
        self.cargo_weight = cargo_weight
        
        # Флаг приоритетности
        self.is_vip = is_vip
