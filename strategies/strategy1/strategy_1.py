from mathematiks import dist
from utils import find_nearest_warehouse
from classes import *
from strategies.strategy1 import *

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
        
        interest, warehouse = order.calculate_interest(order, warehouses_dict, max_dist,  products_weight)
        order_interest_list.append([interest, order, warehouse])
    
    order_interest_list.sort(key=lambda x: x[0])
    
    #list[warehouse.id]->[order.ids]
    warehouse_orders= {}
    for warehouse in warehouses_dict.values():
        warehouse_orders[warehouse.coordinates] = []
    
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
                warehouses_dict[warehouse.coordinates].products_info[item] -= 1
            warehouse_orders[warehouse.coordinates].append(order)
        else:
            #does nothing for now
            pass
    
    
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
        