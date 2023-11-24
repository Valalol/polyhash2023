from classes import *
from mathematiks import dist
from utils import *
from strategies.strategy1.strategy_1_Classes import *

def choosing_warehouse(warehouses_dict: dict, drone: Drone, max_dist: int):
    warehouse = find_nearest_warehouse(drone.coordinates, warehouses_dict, max_dist)
    warehouses_dict.pop(warehouse.coordinates)
    return warehouse, warehouses_dict

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
    
    new_item_list = [None] * len(products_weight)
    for item_id, weight in enumerate(products_weight):
        new_item_list[item_id] = Item(item_id, weight)
    
    new_order_list = [None] * len(orders_dict.values())
    for order_id, order in enumerate(orders_dict.values()):
        new_order_item_list = []
        for index, item_id in enumerate(order.items):
            new_order_item_list.append( new_item_list[item_id] )
        new_order_list[order_id] = IOrder(order_id, order.coordinates, new_order_item_list)
    
    new_warehouse_list = [None] * len(warehouses_dict.values())
    for warehouse_id, warehouse in enumerate(warehouses_dict.values()):
        new_warehouse_item_list = []
        for item_id, item_number in enumerate(warehouse.products_info):
            new_warehouse_item_list.append( [new_item_list[item_id], item_number] )
        new_warehouse_list[warehouse_id] = IWarehouse(warehouse_id, warehouse.coordinates, new_warehouse_item_list, level_info.max_weight)
    
    return [level_info, new_warehouse_list, new_order_list]

def solve(challenge_data):
    
    level_info, warehouse_list, order_list = update_classes(challenge_data)

    order_interest_list = [] #list[int, Order, Warehouse]
    #sort orders by interest:
    
    #### erverything under this needs to be updated ####
    
    for index, order in enumerate(order_list):
        
        interest = order.calculate_interest(warehouse_list, level_info)
        order_interest_list.append([interest, order])
    
    order_interest_list.sort(key=lambda x: x[0])
    
    #list[warehouse.id]->[order.ids]
    warehouse_orders= {}
    for warehouse in warehouse_list:
        warehouse_orders = [] * len(warehouse_list)
    
    for order_info in order_interest_list:
        order = tuple(order_info)
        
        #checks if the items in the order is in the warehouse
        is_in_warehouse: bool = True
        while index < len(order.items) and is_in_warehouse is True:
            if warehouse.products_info[order.items[index]] == 0:
                is_in_warehouse = False

        #if the items are in the warehouse then it removes them from the warehouse and adds the order to the new warehouse_dict
        if is_in_warehouse :
            for item in order.items:
                warehouse_list[warehouse.warehouse_id].products_info[item] -= 1
            warehouse_orders[warehouse.warehouse_id].append(order)
        else:
            #does nothing for now
            pass
    
    """ to finish patching updates"""
    
    # using drones
    
    total_order_number: int = 0
    for warehouse in warehouse_orders.values():
        total_order_number += len(warehouse_orders)
    total_order_index: int = 0
    
    warehouse0 = list(warehouses_dict.values())[0]
    drones_info = []
    for i in range  (drone_count):
        
        
        order_index = 0
        product_index = 0
        drone_state = 2
        drone = Drone(warehouse0.coordinates, max_load, products_weight, i)
        drones_info.append([drone, [order_index, product_index]])
        drone.state = drone_state
        drone.warehouse, warehouse_orders = choosing_warehouse(warehouses_dict, drone, max_dist)
    
    tick = 0
    while tick < deadline and total_order_index < total_order_number:
        
        for drone, warehouse in drones_info:
            tick += 1
            drone.tick()
            if drone.drone_busy():
                    continue
            
            else:
                
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
                        total_order_index += 1
                        product_index = 0
                        drone.state = 2
                        
                        #check that the maximum number or order from the warehouse is not reached
                        if order_index < len(warehouse.products_info):
                            order = warehouse.products_info[order_index]
                        else:
                            drone.warehouse, warehouse_orders = choosing_warehouse(warehouse_orders, drone, max_dist)
                            
                    drone.state = 2
                
                elif drone.state == 2:
                    
                    drone.travel(warehouse.coordinates)
                    print(f"Started travelling to warehouse ({warehouse.coordinates}) at tick {tick}")
                    state = 3
        