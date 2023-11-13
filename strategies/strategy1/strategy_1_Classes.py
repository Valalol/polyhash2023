from classes import Warehouse, Drone, Order
from mathematiks import dist

#max_weight is the maximum weight of an item + 1

class IWarehouse(Warehouse):
    def __init__(self, warehouse_id: int,
                 coordinates: tuple[int, int], products_info: list[int],
                 max_weight: int, products_weight: list[int]
                 ):
        """
        A class representing a warehouse that stores products.

        Attributes:
        - warehouse_interest: int: The interest of the warehouse.
        - warehouse_id (int): An optional integer representing the ID of the warehouse.
        - coordinates (tuple[int, int]): The coordinates of the warehouse.
        - products_info (list[int]): A list of integers representing the quantity of each product stored in the warehouse.
        - drones_on_use: list[int] = []: A list of the Drones Objects that are currently using the warehouse as a hive.
        - complete_orders: list[Order]: A list of the Orders that are complete within the warehouse.
        """
        self.warehouse_interest: int = 0
        self.warehouse_id: int = warehouse_id
        self.coordinates: tuple[int, int] = coordinates
        self.products_info: list[int] = products_info
        self.drones_on_use: list[int] = []
        self.complete_orders: list[Order] = []
        
        self.calculate_interest(max_weight, products_weight)
    
    #function used to calculate the interest of the warehouse from its products_info
    def calculate_interest(self,max_weight: int, products_weight: list[int]):
        for product_type, product_number in self.products_info.items():
            self.warehouse_interest += (max_weight - products_weight[product_type]) * product_number
    
    #Use of a setter is needed to update the interest of the warehouse whilst changing the products_info
    def remove_item(self, item: int, max_weight: int, products_weight: list[int]):
        assert self.products_info[item] > 0
        self.products_info[item] -= 1
        self.interest -= (max_weight - products_weight[item])
    
    #Use of a setter is needed to update the interest of the warehouse whilst changing the products_info
    def add_item(self, item: int, max_weight: int, products_weight: list[int]):
        self.products_info[item] += 1
        self.interest += (max_weight - products_weight[item])

class IOrder(Order):
    def __init__(self, order_id: int, products_weight: list[int],
                 coordinates: tuple[int, int], items: list[int]
                 ):
        """
        A class representing an order that stores products.
        
        Attributes:
        - order_interest: int | None: The interest of the order.
        - order_id (int): An optional integer representing the ID of the order.
        - coordinates (tuple[int, int]): The coordinates of the order.
        - items (list[int]): A list of integers representing the IDs of the products ordered.
        - closest_order_warehouse: Warehouse | None: The closest warehouse that contains the order.
        - weight: int: The total weight of the order. 
        """
        self.order_interest: int | None = None
        self.order_id: int = order_id
        self.coordinates: tuple[int, int] = coordinates
        self.items: list[int] = items
        self.closest_order_warehouse: Warehouse = None
        self.weight: int = 0
        
        self.update_weight(products_weight)
    
    #function used to calculate the weight of the order from its items
    def update_weight(self, products_weight: list[int]):
        for item in self.items:
            self.weight += products_weight[item]
    
    #calculates the total interest of the order from various variables
    def calculate_interest(self, warehouses_dict: dict, max_dist: int, products_weight: list, max_weight: int, 
                   items_weight_coeff: int | None = 1, items_weight_pow: int | None = 1,
                   items_num_coeff: int | None = 1, items_num_pow: int | None = 1, 
                   command_dist_coeff: int | None = 1, command_dist_pow: int | None = 1):
        
        items_num: int = len(self.items)
        weight_value: int = self.items_num * max_weight - self.weight
        
        #finds the closest warehouse that contains the order and calculates the distance
        min_distance_value: int = max_dist
        closest_warehouse: Warehouse = list(warehouses_dict.values())[0]
        for warehouse in warehouses_dict.values():
            
            if warehouse.contains(self.items):
                distance_value: int = dist(warehouse.coordinates, self.coordinates)
                if distance_value < min_distance_value:
                    closest_warehouse = warehouse
                    min_distance_value = distance_value
        
        self.closest_order_warehouse = closest_warehouse

        #calculates the total interest of the order
        weight_interest: int = ( items_weight_coeff*weight_value**items_weight_pow )
        number_interest: int = ( items_num_coeff*items_num**items_num_pow )
        dist_interest: int = ( command_dist_coeff*min_distance_value**command_dist_pow )
        
        total_interest: int = weight_interest + number_interest + dist_interest
        
        self.order_interest = total_interest


class IDrone(Drone):
    pass
    
    
        

