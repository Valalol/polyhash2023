from classes import Warehouse, Drone, Order
from mathematiks import dist

class IWarehouse(Warehouse):
    def __init__(self, warehouse_id: int,
                 coordinates: tuple[int, int], products_info: list[int]
                 ):
        self.warehouse_interest = 0
        self.warehouse_id = warehouse_id
        self.coordinates = coordinates
        self.products_info = products_info
        
    def calculate_interest(self):
        pass

class IOrder(Order):
    def __init__(self, order_id: int,
                 coordinates: tuple[int, int], items: list[int]
                 ):
        self.order_interest = 0
        self.order_id = order_id
        self.coordinates = coordinates
        self.items = items
        self.order_warehouse = None
    
    def calculate_interest(self, warehouses_dict: dict, max_dist: int, products_weight: list,
                   items_weight_coeff: int | None = 1, items_weight_pow: int | None = 1,
                   items_num_coeff: int | None = 1, items_num_pow: int | None = 1, 
                   command_dist_coeff: int | None = 1, command_dist_pow: int | None = 1):
        
        #calculate the weight of the order
        weight_value: int = 0
        #sums the weight of the items in the order
        for item in self.items:
            weight_value += products_weight[item]
        
        items_num: int = len(self.items)
        
        #calculate minimum distance of a warehouse who has the items & registers the warehouse
        min_distance_value: int = max_dist
        closest_warehouse: Warehouse = list(warehouses_dict.values())[0]
        for warehouse in warehouses_dict.values():
            
            if warehouse.contains(dict(self.items)):
                distance_value: int = dist(warehouse.coordinates,self.coordinates)
                if distance_value < min_distance_value:
                    closest_warehouse = warehouse
                    min_distance_value = distance_value

        #calculates the total interest of the order
        weight_interest: int = ( items_weight_coeff*weight_value**items_weight_pow )
        number_interest: int = ( items_num_coeff*items_num**items_num_pow )
        dist_interest: int = ( command_dist_coeff*min_distance_value**command_dist_pow )
        
        total_interest: int = weight_interest + number_interest + dist_interest
        
        return total_interest, closest_warehouse    


class IDrone(Drone):
    def __init__(self, drone_id: int,
                 coordinates: tuple[int, int], max_load: int, item_weights: list[int]
                 ):
        self.drone_id = drone_id
        self.drone_interest = 0
        self.state = None  # 0:move, 1:deliver, 2:load
        self.coordinates = coordinates
        self.item_dict = {}
        self.current_load = 0
        self.max_load = max_load
        self.turns_left = 0
        self.item_weights = item_weights
        
    def calculate_interest(self):
        pass

