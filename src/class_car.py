class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start(self):
        return f"{self.make} {self.model} is starting."

    def stop(self):
        return f"{self.make} {self.model} is stopping."
car1=Car("Toyota", "Camry", 2020)
car2=Car("Honda", "Civic", 2019)

print(car1.start())
print(car1.make)
print(car2.stop())
print(car2.model)