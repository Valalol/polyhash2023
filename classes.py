from __future__ import annotations
from mathematiks import *
from math import ceil
from modified_data_classes import *


class Warehouse:
    """
    A class representing a warehouse that stores products.

    Attributes:
    - coordinates (tuple[int, int]): The coordinates of the warehouse.
    - products_info (list[int]): A list of integers representing the quantity of each product stored in the warehouse.
    - warehouse_id (int): An optional integer representing the ID of the warehouse.
    """

    def __init__(self, coordinates: tuple[int, int], products_info: list[int], warehouse_id: int = 0):
        self.products_info = products_info
        self.coordinates = coordinates
        self.warehouse_id = warehouse_id
    
    def contains(self, products: dict[int] | list[int]):
        
        if products is dict: #dict[product_type] -> product_number
            for product_type, product_number in products.items():
                if self.products_info[product_type] <product_number:
                    return False
        
        elif products is list: #dict[index] -> product_type
            for product_type in products:
                if self.products_info[product_type] < 1:
                    return False
        
        return True
    
    def remove_products(self, products: dict[int]):
        for product in products:
            self.products_info[product] -= products[product]


class Order:
    """
    Represents an order with a list of items and coordinates for delivery.

    Attributes:
        coordinates (tuple[int, int]): The coordinates for delivery.
        items (list[int]): The list of items in the order.
        order_id (int): The ID of the order.
    """
    def __init__(self, coordinates: tuple[int, int], items: list[int], order_id: int = 0):
        self.items = items
        self.coordinates = coordinates
        self.order_id = order_id
    
    def require(self, products: dict[int]):
        for product in products:
            if self.items.count(product) < products[product]:
                return False
        return True
    
    def deliver(self, products: dict[int]):
        for product in products:
            self.items.pop(self.items.index(product))


class Drone:
    def __init__(self, coordinates: tuple[int, int], max_load: int, item_weights: list[int], drone_id: int = 0):
        self.state = None  # 0:move, 1:deliver, 2:load
        self.coordinates = coordinates
        self.item_dict = {}
        self.current_load = 0
        self.max_load = max_load
        self.turns_left = 0
        self.item_weights = item_weights
        self.drone_id = drone_id


    def load(self, items: dict[int], warehouse: Warehouse):
        """
        Loads items from a warehouse onto the drone.

        Args:
            items (dict[int]): A dictionary of item IDs and their quantities to be loaded onto the drone.
            warehouse (Warehouse): The warehouse from which the items are to be loaded.

        Raises:
            AssertionError: If the drone is currently busy, the warehouse does not contain the requested items, or the drone is overloaded or underloaded.
        """
        assert not self.drone_busy(), (f"Drone {self.drone_id} is busy for {self.turns_left} more turns.")
        assert warehouse.contains(items), (f"Warehouse {warehouse.warehouse_id} does not contain {items}.")
        new_items_total_weight = items_total_weight(self.item_weights, items)
        assert 0 <= self.current_load + new_items_total_weight <= self.max_load, (f"Drone {self.drone_id} is overloaded or underloaded.")
        
        self.__travel(warehouse.coordinates)
        self.state = 2
        warehouse.remove_products(items)
        self.item_dict = dict_add(self.item_dict, items)
        self.current_load += new_items_total_weight
        self.turns_left += len(items)


    def deliver(self, items: dict[int], order: Order):
        """
        Delivers items to an order.

        Args:
            items (dict[int, int]): A dictionary of item IDs and their quantities.
            order (Order): The order to deliver the items to.

        Raises:
            AssertionError: If the drone is busy, the order does not require the given items, or the drone is overloaded or underloaded.
        """
        assert not self.drone_busy(), (f"Drone {self.drone_id} is busy for {self.turns_left} more turns.")
        assert order.require(items), (f"Order {order.order_id} does not require {items}.")
        removed_items_total_weight = items_total_weight(self.item_weights, items)
        assert 0 <= self.current_load - removed_items_total_weight <= self.max_load, (f"Drone {self.drone_id} is overloaded or underloaded.")
        
        self.__travel(order.coordinates)
        self.state = 1
        self.item_dict = dict_subtract(self.item_dict, items)
        order.deliver(items)
        self.current_load -= removed_items_total_weight
        self.turns_left += len(items)


    def __travel(self, coordinates: tuple[int, int]):
        """
        Moves the drone to the specified coordinates.

        Args:
            coordinates: A tuple of integers representing the destination coordinates.
        """
        assert not self.drone_busy(), (f"Drone {self.drone_id} is busy for {self.turns_left} more turns.")
        self.state = 0
        self.turns_left = ceil(dist(self.coordinates, coordinates))
        self.coordinates = coordinates


    def wait(self, turns: int):
            """
            Wait for a specified number of turns.

            Args:
                turns (int): The number of turns to wait.

            Raises:
                AssertionError: If the drone is already busy.
            """
            assert not self.drone_busy(), (f"Drone {self.drone_id} is busy for {self.turns_left} more turns.")
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
