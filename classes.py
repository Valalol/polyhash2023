from __future__ import annotations
from math import ceil
from utils import check_b_in_a, dict_subtract, dict_add, items_total_weight, dist



class Tick:
    def __init__(self):
        self.value: int = -1

class Score:
    def __init__(self):
        self.value: int = 0

class Warehouse:
    """
    A class representing a warehouse that stores products.

    Attributes:
    - coordinates (tuple[int, int]): The coordinates of the warehouse.
    - products_info (list[int]): A list of integers representing the quantity of each product stored in the warehouse.
    - warehouse_id (int): An optional integer representing the ID of the warehouse.
    """

    def __init__(self, coordinates: tuple[int, int], products_info: list[int], warehouse_id: int = 0):
        self.products_info: list[int] = products_info.copy()
        self.predicted_products_info: list[int] = products_info.copy()
        self.coordinates: tuple[int,int] = coordinates
        self.warehouse_id: int = warehouse_id
    
    def contains(self, products: dict[int] | list[int]) -> bool:
        """
        Ckecks if the warehouse contains the given products.
        
        """
        
        return check_b_in_a(self.products_info, products, 2)
    
    def remove_products(self, products: dict[int] | list[int], real: bool = True) -> None:
        """
        Removes products from the warehouse
        
        Args:
            products (dict[int]): products to remove
            real (bool): if True, removes the products from the real inventory, else removes them from the predicted inventory
        
        Raises:
            ValueError: If the warehouse does not contain at least one product.
        
        """
        
        if self.contains(products):
            
            if type(products) is dict: #dict[product_type] -> product_number
                for product_type, product_number in products.items():
                    if real:
                        self.products_info[product_type] -= product_number
                    else:
                        self.predicted_products_info[product_type] -= product_number
            
            elif type(products) is list: #dict[index] -> product_type
                for product_type in products:
                    if real:
                        self.products_info[product_type] -= product_number
                    else:
                        self.predicted_products_info[product_type] -= product_number
        else:
            raise ValueError("The warehouse does not contain at least one product.")

class Order:
    """
    Represents an order with a list of items and coordinates for delivery.

    Attributes:
        coordinates (tuple[int, int]): The coordinates for delivery.
        items (list[int]): The list of items in the order.
        order_id (int): The ID of the order.
        deadline (int): The deadline for delivering the order.
        tick (Tick): The current tick of the simulation.
        score (Score): The score of the order.
        
    Functions:
        require(self, products: dict[int]) -> bool: Checks if the drone contains the requested items.
        deliver(self, products: dict[int]) -> None: Removes the requested items from the drone.
    """
    
    def __init__(self, coordinates: tuple[int, int], items: list[int], order_id: int, deadline: int, tick: Tick, score: Score):
        self.items: list[int] = items.copy()
        self.remaining_items: list[int] = items.copy()
        self.coordinates: tuple(int,int) = coordinates
        self.order_id: int = order_id
        self.deadline: int = deadline
        self.tick: Tick = tick
        self.score: Score = score
    
    def require(self, products: dict[int]) -> bool:
        """
        Checks if the drone contains the requested items.

        Args:
            products (dict[int]): A dictionary of product IDs and their quantities.

        Returns:
            bool: True if the drone contains all the requested items, False otherwise.
        """
        for product in products:
            if self.items.count(product) < products[product]:
                return False
        return True
    
    def deliver(self, products: dict[int]) -> None:
        """
        Subtracts the items that have been delivered from the drone's inventory.
        
        Args:
            products (dict[int]): A dictionary of product IDs and their quantities.
        """
        for product in products:
            self.items.pop(self.items.index(product))
        
        if len(self.items) == 0:
            new_score = ceil((self.deadline - self.tick.value) / self.deadline * 100)
            self.score.value += new_score
            # print(f"Order {self.order_id} delivered at tick {self.tick.value} with a score of {new_score}")


class Drone:
    """
    Represents a drone.
    
    Attributes:
        state (int): The state of the drone (0: move, 1: deliver, 2: load).
        coordinates (tuple[int, int]): The coordinates of the drone.
        item_dict (dict[coordinates]= Item): A dictionary of item Objects and their quantities.
        current_load (int): The current load of the drone.
        max_load (int): The maximum load capacity of the drone.
        turns_left (int): The number of turns left before the drone finishes its current task.
        item_weights (list[int]): The weights of different items.
        drone_id (int): The ID of the drone.
        current_order (Order): The current order the drone is handling.
        memory (list): A list of commands stored in the memory.
        orders_memory (list): A list of orders stored in the memory.

    Methods:
        load(self, items: dict[int], warehouse: Warehouse): Loads items onto the drone from the warehouse.
        true_load(self, items: dict[int], warehouse: Warehouse): [Internal use only] Used to load one or more items of the same type from a warehouse when the droens reaches the warehouse.
        deliver(self, items: dict[int], order: Order): Delivers items from the drone to an order.
        true_deliver(self, items: dict[int], order: Order): [Internal use only] Used to deliver one or more items of the same type to an order when the drone reaches the order.
        __travel(self, coordinates: tuple[int, int]): [Internal use only] Moves the drone to the specified coordinates. (called by load and deliver)
        wait(self, turns: int): Waits for a specified number of turns.
        drone_busy(self): Checks if the drone is busy.
        tick(self): Decrements the number of turns left before finishing its current task and executes commands from the memory if the drone is not busy.
        update_memory(self, command: list): Updates the memory with a new command.
        exec_memory(self): Executes the oldest command stored in the memory.
    """

    def __init__(self, coordinates: tuple[int, int], max_load: int, item_weights: list[int], drone_id: int = 0):
        self.state: int = 0
        self.coordinates: tuple(int,int) = coordinates
        self.item_dict: dict = {}
        self.current_load: int = 0
        self.max_load: int = max_load
        self.turns_left: int = 0
        self.item_weights: list = item_weights
        self.drone_id: int = drone_id
        self.current_order: Order | None = None
        self.memory: list = []
        self.orders_memory: list = []


    def load(self, items: dict[int], warehouse: Warehouse) -> None:
        """
        This function is a facade meant to be used by the user.
        It checks if it is possible to load the given items onto the drone from the warehouse.
        Then it adds the times it takes to travel to the destination to the drone's turns_left attribute.
        Finally it adds as much true_load as the number of different "items" in the items dictionary in the memory.

        Args:
            items (dict[int]): A dictionary of item IDs and their quantities to be loaded onto the drone.
            warehouse (Warehouse): The warehouse from which the items are to be loaded.

        Assertions:
            The drone must not be busy.
            The warehouse must contain the requested items.
            The drone must not be overloaded or underloaded.
        """
        assert not self.drone_busy(), (f"Drone {self.drone_id} is busy for {self.turns_left} more turns.")
        assert warehouse.contains(items), (f"Warehouse {warehouse.warehouse_id} does not contain {items}.")
        new_items_total_weight: int = items_total_weight(self.item_weights, items)
        predictive_load: int = self.current_load + new_items_total_weight
        assert 0 <= predictive_load <= self.max_load, (f"Drone {self.drone_id} is overloaded or underloaded. (Predictive load: {predictive_load}, Max load: {self.max_load})")
        
        self.__travel(warehouse.coordinates)
        self.state = 2
        warehouse.remove_products(items, real=False)
        # Set into memory: true load
        for item, number in items.items():
            new_dict: dict = {item: number}
            self.update_memory(["load", new_dict, warehouse])

    def true_load(self, items: dict[int], warehouse: Warehouse) -> None:
        """
        Loads one or more item of the same type from a warehouse.

        Parameters:
        - items (dict[int]): A dictionary representing the items to be loaded, where the keys are item IDs and the values are quantities.
        - warehouse (Warehouse): The warehouse from which the items are being loaded.

        Returns:
        None
        """
        warehouse.remove_products(items, real=True)
        self.item_dict = dict_add(self.item_dict, items)
        self.current_load += items_total_weight(self.item_weights, items)
        self.turns_left += len(items)


    def deliver(self, items: dict[int], order: Order) -> None:
        """
        This function is a facade meant to be used by the user.
        It checks if it is possible to deliver the given items from the drone to the order.
        Then it adds the times it takes to travel to the destination to the drone's turns_left attribute.
        Finally it adds as much true_deliver as the number of different items in the "items" dictionary in the memory.

        Args:
            items (dict[int, int]): A dictionary of item IDs and their quantities.
            order (Order): The order to deliver the items to.

        Raises:
            AssertionError: If the drone is busy, the order does not require the given items, or the drone is overloaded or underloaded.
        """
        assert not self.drone_busy(), (f"Drone {self.drone_id} is busy for {self.turns_left} more turns.")
        assert order.require(items), (f"Order {order.order_id} does not require {items}.")
        assert check_b_in_a(self.item_dict, items), (f"Drone {self.drone_id} does not possess {items}.")
        removed_items_total_weight: int = items_total_weight(self.item_weights, items)
        predictive_load: int = self.current_load - removed_items_total_weight
        assert 0 <= predictive_load <= self.max_load, (f"Drone {self.drone_id} is overloaded or underloaded. (Predictive load: {predictive_load}, Max load: {self.max_load})")
        
        self.__travel(order.coordinates)
        self.state = 1
        #set into memory : true unload
        new_dict = {}
        for item, number in items.items():
            new_dict[item] = number
            self.update_memory(["deliver", new_dict,order])

    def true_deliver(self, items: dict[int], order: Order) -> None:
        """
        Delivers one or more item of the same type to an order.
        """
        self.item_dict = dict_subtract(self.item_dict, items)
        order.deliver(items)
        self.current_load -= items_total_weight(self.item_weights, items)
        self.turns_left += len(items)

    def __travel(self, coordinates: tuple[int, int]) -> None:
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


    def wait(self, turns: int) -> None:
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


    def drone_busy(self) -> bool:
        """checks if the drone is busy"""
        return self.turns_left > 0


    def tick(self) -> None:
        """
        decrements the number of turns left before finishing what he is doing
        checks and executes for the memory in case the drone is not busy
        """
        if self.drone_busy():
            self.turns_left -= 1
        if not self.drone_busy() and len(self.memory) > 0 :
            self.exec_memory()
    
    def update_memory(self, command: list) -> None:
        self.memory.append(command)
    
    def exec_memory(self) -> None:
        """
        executes the oldest command stored in the memory.
        """
        if len(self.memory) != 0:
            command = self.memory.pop(0)
            if command[0] == "load":
                self.true_load(*command[1:])
            elif command[0] == "deliver":
                self.true_deliver(*command[1:])

if __name__ == '__main__':
    pass
