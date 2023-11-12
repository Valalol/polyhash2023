from mathematiks import dist
from utils import find_nearest_warehouse
from classes import *
# calulating the worth of each command:
max_dist = 1000

# calculate the interest of a given order
def interest_funct(order: Order, warehouses_dict: dict, max_dist: int, products_weight: list,
                   items_weight_coeff: int | None = 1, items_weight_pow: int | None = 1,
                   items_num_coeff: int | None = 1, items_num_pow: int | None = 1, 
                   command_dist_coeff: int | None = 1, command_dist_pow: int | None = 1):
    
    items_weight_coeff = items_weight_coeff
    items_weight_pow  = items_weight_pow
    items_num_coeff = items_num_coeff
    items_num_pow  = items_num_pow
    command_dist_coeff = command_dist_coeff
    command_dist_pow  = command_dist_pow
    
    
    
    #calculate the weight of the order
    weight_value: int = 0
    #sums the weight of the items in the order
    for item in order.items:
        weight_value += products_weight[item]
    
    items_num: int = len(order.items)
    
    #calculate minimum distance of a warehouse who has the items & registers the warehouse
    min_distance_value: int = max_dist
    closest_warehouse: Warehouse = None
    
    for warehouse in warehouses_dict.values():
        as_items: bool = True

        #checks if the warehouse has the items
        i: int = 0
        while i < len(order.items) and as_items is True:
            item = order.items[i]
            i += 1
            if warehouse.products_info[item]  == 0:
                as_items = False

        #checks if the distance of the warehouse is less then the known closest's one
        if as_items is True :
            distance_value: int = dist(warehouse.coordinates,order.coordinates)
            if distance_value < min_distance_value:
                closest_warehouse = warehouse
                min_distance_value = distance_value

    #calculates the total interest of the order
    weight_interest: int = ( items_weight_coeff*weight_value**items_weight_pow )
    number_interest: int = ( items_num_coeff*items_num**items_num_pow )
    dist_interest: int = ( command_dist_coeff*min_distance_value**command_dist_pow )
    
    total_interest: int = weight_interest + number_interest + dist_interest
    
    return total_interest, closest_warehouse

def choosing_warehouse(warehouses_dict: dict, drone: Drone, max_dist: int):
    warehouse = find_nearest_warehouse(drone.coordinates, warehouses_dict, max_dist)
    warehouses_dict.pop(warehouse.coordinates)
    return warehouse, warehouses_dict

def solve(challenge_data):
    
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data
    max_dist = rows + columns

    order_interest_list = [] #list[int, Order, Warehouse]
    #sort orders by interest:
    
    for index,order in enumerate(orders_dict.values()):
        
        interest, warehouse = interest_funct(order, max_dist, warehouses_dict)
        order_interest_list.append([interest, order, warehouse])
    
    order_interest_list.sort(key=lambda x: x[0])
    
    
    warehouse_dict_current_state = warehouses_dict.copy()
    warehouses_dict_new = warehouses_dict.copy()
    for warehouse in warehouses_dict_new.values():
        warehouse.products_info = []
    
    for order in order_interest_list:
        c_interest, order, warehouse = tuple(order)
        
        #checks if the items in the order is in the warehouse
        is_in_warehouse: bool = True
        while index < len(order.items) and is_in_warehouse is True:
            if warehouse.products_info[order.items[index]] == 0:
                is_in_warehouse = False

        #if the items are in the warehouse then it removes them from the warehouse and adds the order to the new warehouse_dict
        if is_in_warehouse :
            for item in order.items:
                warehouse_dict_current_state[warehouse.coordinates].products_info[item] -= 1
            warehouses_dict_new(warehouse.coordinates).products_info.append(order)
        else:
            #does nothing for now
            pass
    
    
    # using drones
    tick = 0
    order_index = 0
    warehouse0 = list(warehouses_dict_new.values())[0]
    orders = warehouse.products_info
    drone = Drone(warehouse0.coordinates, max_load, products_weight)
    drones_info = []
    for _ in range  (drone_count):
        
        order_index = 0
        product_index = 0
        drone_state = 2
        
        drones_info.append(Drone(warehouse0.coordinates, max_load, products_weight), None)
        drones_info[1] = [order_index, product_index]
        drone.state = drone_state
        drone.warehouse, warehouses_dict_new = choosing_warehouse(warehouses_dict_new, drone, max_dist)
    
    while tick < deadline and order_index < len(orders):
        
        for drone, warehouse in drones_info:
            tick += 1
            drone.tick()
            if drone.drone_busy():
                    continue
            
            else:
                
                #checks that the order is not already complete
                
                #check that the maximum number or order from the warehouse is not already reached
                
                product_type = order.items[product_index]
                
                if drone.state == 3:
                    
                    drone.load({product_type: 1})
                    print(f"Loaded product {product_type} at tick {tick}")
                    drone.state = 0   
                
                elif drone.state == 0:
                    
                    drone.travel(order.coordinates)
                    print(f"Started travelling with product index {product_index} for order {order_index} at tick {tick}")
                    drone.state = 1
                
                elif drone.state == 1:
                    
                    drone.unload({product_type: 1})
                    print(f"Unloaded product {product_type} at tick {tick}")
                    product_index += 1
                    order.items.remove(product_type)
                    
                    #checks if the order is completed
                    if len(order.items) == 0:
                        
                        print(f"Order {order_index} completed at tick {tick}")
                        order_index += 1
                        product_index = 0
                        drone.state = 2
                        
                        #check that the maximum number or order from the warehouse is not already reached
                        if order_index < len(warehouse.products_info):
                            order = orders[order_index]
                        else:
                            drone.warehouse, warehouses_dict_new = choosing_warehouse(warehouses_dict_new, drone, max_dist)
                            
                    drone.state = 2
                
                elif drone.state == 2:
                    
                    drone.travel(warehouse.coordinates)
                    print(f"Started travelling to warehouse ({warehouse.coordinates}) at tick {tick}")
                    state = 3
        