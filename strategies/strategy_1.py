from classes import *
from mathematiks import dist
from utils import *
from strategies.strategy1.strategy_1_Classes import *

def choosing_warehouse(warehouses_list: list[int], warehouses_orders: list[int], drone: Drone, max_dist: int)-> Warehouse | None:
    """
    chooses the most interesting warehouse
    """
    most_interesting_warehouse = None
    max_interest = 0
    for warehouse in warehouses_list:
        if warehouse.interest > max_interest and len(warehouses_orders[warehouse.warehouse_id]) != 0 :
            max_interest = warehouse.interest
            most_interesting_warehouse = warehouse
    return most_interesting_warehouse

def update_classes(challenge_data):
    """
    updates the strategy datas to use strategy 1 classes
    
    Args:
        challenge data contains: rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict
    
    Returns:
        new_challenge_data wich contains:
        - level_info, new_warehouses_dict, new_orders_dict
    """
    level_info = LevelInfo(challenge_data)
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data
    
    new_orders_list = []
    for order in list(orders_dict.values()):
        new_orders_list.append(IOrder(order))
    
    new_warehouses_list = []
    for warehouse in list(warehouses_dict.values()):
        new_warehouses_list.append(IWarehouse(warehouse, products_weight))
    
    return [level_info, new_warehouses_list, new_orders_list]

def solve(challenge_data):
    level_info : LevelInfo
    warehouses_list : list[Warehouse]
    order_list : list[Order]
    
    level_info, warehouses_list, orders_list = update_classes(challenge_data)

    order_interest_list = [] #list[int, Order, Warehouse]
    #sort orders by interest:
    
    #### erverything under this needs to be updated ####
    
    for index, order in enumerate(orders_list):
        
        interest = order.calculate_interest(warehouses_list, level_info)
        order_interest_list.append([interest, order])
    
    order_interest_list.sort(key=lambda x: x[0])
    
    #list[warehouse.id]->[order.ids]
    warehouses_orders= [[]] * len(warehouses_list)
    
    for order_info in order_interest_list:
        order = order_info[1]
        
        warehouse = find_warehouse_containing_order(order, warehouses_list, level_info.max_dist, True)
        if warehouse != None:
            for item in order.items:
                warehouse.products_info[item] -= 1
            warehouses_orders[warehouse.warehouse_id].append(order)
    
    print(f'debug={warehouses_orders}')
    
    # using drones
    drone_count = level_info.drone_count
    total_order_number: int = 0
    for warehouse_orders in warehouses_orders:
        total_order_number += len(warehouse_orders)
    total_order_index: int = 0
    
    warehouse0 = warehouses_list[0]
    drones_info = []
    
    for i in range  (drone_count):
        
        order_index = 0
        product_index = 0
        drone_state = 2
        drone = Drone(warehouse0.coordinates, level_info.max_load, level_info.products_weight, i)
        drones_info.append([drone, [order_index, product_index]])
        drone.state = drone_state
        drone.warehouse = choosing_warehouse(warehouses_list, warehouses_orders, drone, level_info.max_dist)
    
    tick = 0
    while tick < level_info.deadline and total_order_index < total_order_number:
        
        for drone, [order_index, product_index] in drones_info:
            warehouse = drone.warehouse
            tick += 1
            drone.tick()
            if drone.drone_busy():
                    continue
            
            else:
                
                product_type = order.items[product_index]
                
                if drone.state == 2:
                    
                    drone.load({product_type: 1}, warehouse)
                    print(f"tried to load product {product_type} at tick {tick}")
                    drone.state = 1
                
                elif drone.state == 1:
                    
                    drone.unload({product_type: 1}, order)
                    print(f"tried to unload product {product_type} at tick {tick}")
                    product_index += 1
                    order.items.remove(product_type)
                    
                    #checks if the order is completed
                    if len(order.items) == 0:
                        
                        print(f"Order {order_index} completed at tick {tick}")
                        order_index += 1
                        total_order_index += 1
                        product_index = 0
                        drone.state = 2
                        
                        #check that the maximum number or order from the warehouse is not reached
                        if order_index < len(warehouse.products_info):
                            order = warehouse.products_info[order_index]
                        else:
                            drone.warehouse = choosing_warehouse(warehouses_list, drone, level_info.max_dist)
                            
                    drone.state = 2
        