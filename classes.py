from __future__ import annotations
from mathematiks import *
from math import ceil
from modified_data_classes import *
from utils import check_b_in_a


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
        """
        Ckecks if the warehouse contains the given products.
        
        
        """
        
        return check_b_in_a(self.products_info, products, 2)
    
    def remove_products(self, products: dict[int] | list[int]):
        """
        Removes products from the warehouse
        
        Args: 
            products (dict[int]): products to remove
        
        Raises:
            ValueError: If the warehouse does not contain at least one product.
        
        """
        
        if self.contains(products):
            
            if products is dict: #dict[product_type] -> product_number
                for product_type, product_number in products.items():
                    self.products_info[product_type] -= product_number
            
            elif products is list: #dict[index] -> product_type
                for product_type in products:
                    self.products_info[product_type] -= product_number
                    
        else:
            raise ValueError("The warehouse does not contain at least one product.")

class Order:
    """
    Represents an order with a list of items and coordinates for delivery.

    Attributes:
        coordinates (tuple[int, int]): The coordinates for delivery.
        items (list[int]): The list of items in the order.
        order_id (int): The ID of the order.
        
    functions:
        require(self, products: dict[int]) -> bool: Checks if the drone contains the requested items.
        deliver(self, products: dict[int]) -> None: Removes the requested items from the drone
    """
    def __init__(self, coordinates: tuple[int, int], items: list[int], order_id: int = 0):
        self.items = items.copy()
        self.remaining_items = items.copy()
        self.coordinates = coordinates
        self.order_id = order_id
    
    #functions that checks if the drones contains t
    def require(self, products: dict[int]):
        """
        checks if the drone contains the requested items.
        
        args:
            products (dict[int]): A dictionary of product IDs and their quantities.
        
        """
        for product in products:
            if self.items.count(product) < products[product]:
                return False
        return True
    
    
    def deliver(self, products: dict[int]):
        """
        substracts the items that have been delivered from the drone's inventory
        """
        for product in products:
            self.items.pop(self.items.index(product))


class Drone:
    """
    Represents a drone.
    
    Attributes:
        state: int = the state of the drone ( 0:move, 1:deliver, 2:load )
        coordinates: (tuple[int, int]) = The coordinates of the drone.
        item_dict: dict[coordinates]= Item = A dictionary of item Objects and their quantities.
        
    """
    def __init__(self, coordinates: tuple[int, int], max_load: int, item_weights: list[int], drone_id: int = 0):
        self.state = 0
        self.coordinates = coordinates
        self.item_dict = {}
        self.current_load = 0
        self.max_load = max_load
        self.turns_left = 0
        self.item_weights = item_weights
        self.drone_id = drone_id
        self.current_order = None


    def load(self, items: dict[int], warehouse: Warehouse):
        """
        Loads items from a warehouse onto the drone.

        Args:
            items (dict[int]): A dictionary of item IDs and their quantities to be loaded onto the drone.
            warehouse (Warehouse): The warehouse from which the items are to be loaded.

        Assertions:
            The drone must no be busy
            The warehouse msut contain the requested items
            The drone must not be overloaded or underloaded.
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
            coordinates (tuple): A tuple of integers representing the destination coordinates.
        Raises:
            AssertionError: If the drone is already busy.
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
        """checks if the drone is busy"""
        return self.turns_left > 0


    def tick(self):
        """decrements the number of turns left before finishing what he is doing"""
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
