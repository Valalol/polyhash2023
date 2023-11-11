from __future__ import annotations
from mathematiks import *
from math import ceil
from modified_data_classes import *


class Warehouse:
    def __init__(self, coordinates: tuple[int, int], products_info: dict[int]):
        self.products_info = products_info
        self.coordinates = coordinates
    
    def contains(self, products: int | list[int]):
        contain: bool = True
        if product is not list:
            if self.products_info[product] = 0:
                contain = False
        else:
            for product in products:
                if self.products_info[product] = 0:
                    contain = False
        return contain


class Order:
    def __init__(self, coordinates: tuple[int, int], items: list[int]):
        self.items = items
        self.coordinates = coordinates


class Drone:
    def __init__(self, coordinates: tuple[int, int], max_load: int, item_weights: list[int]):
        self.state = None  # 0:move, 1:deliver, 2:load
        self.coordinates = coordinates
        self.item_dict = {}
        self.current_load = 0
        self.max_load = max_load
        self.turns_left = 0
        self.item_weights = item_weights

    def load(self, items: dict[int]):
        assert not self.drone_busy()
        self.state = 2
        self.item_dict = dict_add(self.item_dict, items)
        self.current_load += items_total_weight(self.item_weights, items)
        self.turns_left = len(items)
        assert 0 <= self.current_load <= self.max_load

    def unload(self, items: dict[int]):
        assert not self.drone_busy()
        self.state = 1
        self.item_dict = dict_subtract(self.item_dict, items)
        self.current_load -= items_total_weight(self.item_weights, items)
        self.turns_left = len(items)
        assert 0 <= self.current_load <= self.max_load

    def travel(self, coordinates: tuple[int, int]):
        assert not self.drone_busy()
        self.state = 0
        self.turns_left = ceil(dist(self.coordinates, coordinates))
        self.coordinates = coordinates

    def wait(self, turns: int):
        assert not self.drone_busy()
        self.state = 0
        self.turns_left = turns

    def drone_busy(self):
        return self.turns_left > 0

    def tick(self):
        if self.drone_busy():
            self.turns_left -= 1
        else:
            pass


class Task:
    def __init__(self, end_coordinates: tuple[int, int], drone: Drone):
        self.drone = drone
        self.time_travel_left = end_coordinates

    def tick(self):
        self.time_travel_left -= 1


class MapSectionsDelimitations:
    def __init__(self, coordinates: tuple[int, int]):
        self.coordinates = coordinates


class MapSection:
    def __init__(self, coordinates: tuple[int, int], warehouse_list: list[Warehouse], order_list: list[Order],
                 drone_number: int):
        self.interest = None
        self.warehouse_list = warehouse_list
        self.order_list = order_list
        self.drone_number = drone_number
        self.coordinates = coordinates
        # maybe coordinates here is maybe rendundant

    def set_interest(self):
        section_max_drones = 2
        interest = len(self.warehouse_list) * len(self.order_list) * (section_max_drones - self.drone_number)
        self.interest = interest


if __name__ == '__main__':
    pass
