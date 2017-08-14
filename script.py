from random import randint
from pprint import pprint as pp
import time
import threading


def a_generator():
    i = 0
    while True:
        yield i + 1
# to_drive = a_generator()


class Car(object):
    all_cars = []

    def __init__(self, engine_type, gasoline_tank, max_mileage,
                 rate_per_hundred, price_of_overhaul, distance, delta):
        self.price = 10000
        self.mileage_on_tachograph = 0
        self.engine_type = engine_type
        self.gasoline_tank = gasoline_tank
        self.money_spent = 0
        self.max_mileage = max_mileage
        self.rate_per_hundred = rate_per_hundred
        self.price_of_overhaul = price_of_overhaul
        self.distance = distance
        self.utilization = False
        self.delta = delta
        Car.all_cars.append(self)
        self.fuel_price = 0
        self.count_of_refillings = 0
        self.generation = a_generator()
        self.permission_to_drive = True

    def set_a_distance(self):
        if not self.utilization:
            self.distance = randint(55000, 286000)
        return self.distance

    def drive(self):
        self.count_of_refillings += 1
        if self.permission_to_drive:
            while self.mileage_on_tachograph < self.distance:
                if (self.mileage_on_tachograph - self.kilometres_with_a_full_tank()*self.count_of_refillings) \
                        > self.kilometres_with_a_full_tank():
                    self.permission_to_drive = False
                    self.set_permission()
                    self.a_refilling()
                self.mileage_on_tachograph += self.generation.next()
            self.residual_value()
        return self.mileage_on_tachograph

    def set_permission(self):
        self.permission_to_drive = True
        return self.permission_to_drive

    def a_refilling(self):
        time.sleep(0.01)
        self.count_of_refillings += 1
        return self.count_of_refillings

    def kilometres_with_a_full_tank(self):
        kilometres_with_a_full_tank = (self.gasoline_tank / self.rate_per_hundred)*100
        return kilometres_with_a_full_tank

    def residual_value(self):
        length_in_thousand_km = self.mileage_on_tachograph // 1000
        for i in range(0, length_in_thousand_km):
            self.price -= self.delta
        if self.mileage_on_tachograph >= self.max_mileage:
            self.money_spent = self.price_of_overhaul*(self.distance//self.max_mileage)
        return self.price

    def how_much_fuel(self):
        fuel_in_litres = (self.distance/100)*self.rate_per_hundred
        return fuel_in_litres

    def money_spent_on_fuel(self):
        money_spent_on_fuel = self.how_much_fuel() * self.fuel_price
        return money_spent_on_fuel

    def what_is_rate_per_hundred(self):
        length_in_thousand_km = self.mileage_on_tachograph // 1000
        for i in range(0, length_in_thousand_km):
            self.rate_per_hundred += 0.01 * self.rate_per_hundred
        return self.rate_per_hundred

    def to_utilization(self):
        self.utilization = True
        return self.utilization

    def __str__(self):
        return str(id(self))

    # @property
    # def mileage_on_tachograph(self):
    #     return self.mileage_on_tachograph
    #
    # @mileage_on_tachograph.setter
    # def mileage_on_tachograph(self, value):
    #     if self.mileage_on_tachograph > value:
    #         raise TypeError('Bla-bla')
    #     self.mileage_on_tachograph = value


class PetrolCar(Car):
    all_petrol_cars = []

    def __init__(self):
        Car.__init__(self, engine_type='petrol', gasoline_tank=60,max_mileage=100000,
                     rate_per_hundred=8, price_of_overhaul=500, distance=0, delta=9.5)
        self.fuel_price_ai92 = 2.2
        self.fuel_price_ai95 = 2.4
        PetrolCar.all_petrol_cars.append(self)

    def how_much_fuel(self):
        fuel_in_litres_ai92 = 500*self.rate_per_hundred
        fuel_in_litres_ai95 = (self.distance - 50000) * self.rate_per_hundred / 100
        return fuel_in_litres_ai92, fuel_in_litres_ai95

    def money_spent_on_fuel(self):
        quantity_of_fuel = self.how_much_fuel()
        money_spent_on_fuel = quantity_of_fuel[0] * self.fuel_price_ai92
        money_spent_on_fuel += quantity_of_fuel[1] * self.fuel_price_ai95
        return money_spent_on_fuel


class DieselCar(Car):
    all_diesel_cars = []

    def __init__(self):
        Car.__init__(self, engine_type='diesel', gasoline_tank=60,max_mileage=150000,
                     rate_per_hundred=6, price_of_overhaul=700, distance=0, delta=10.5)
        self.fuel_price = 2.0
        DieselCar.all_diesel_cars.append(self)


if __name__ == '__main__':

    def create_a_taxi_station(number_of_cars):
        for i in xrange(number_of_cars):
            if i % 3 == 0:
                a_car = DieselCar()
            else:
                a_car = PetrolCar()
        return Car.all_cars

    create_a_taxi_station(100)
    max_connections = 10
    semaphore = threading.BoundedSemaphore(max_connections)

    def at_finish(number):
        Car.all_cars[number].set_a_distance()
        semaphore.acquire(max_connections)
        Car.all_cars[number].drive()
        semaphore.release()
        print("I finished! I'm {} car. I have driven {} km. "
              "My pos in all_cars {}".format(id(Car.all_cars[number]),
                                             Car.all_cars[number].mileage_on_tachograph,
                                             number))

    for i in xrange(0, len(Car.all_cars)):
        p = threading.Thread(target=at_finish, args=[i, ])
        p.start()
