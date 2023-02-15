class Car():
    model = "BMW"
    color = "Красный"
    speed = 250
    
    def get_car(self):
        print(f'Машина марки {self.model}, цвет: {self.color}, скорость: {self.speed} км/ч.')
    
vova_car = Car()
vova_car.model = 'Lamborghini'
vova_car.color = 'Оранжевый'
vova_car.speed = 550

vladislav_car = Car()
vladislav_car.model = 'Porshe'
vladislav_car.color = 'Синий'
vladislav_car.speed = 380

print(f"Цвет машины Вовы: {vova_car.color}, Цвет машины Владислава: {vladislav_car.color}")