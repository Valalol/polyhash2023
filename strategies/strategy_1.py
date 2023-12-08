from classes import *
from mathematiks import dist
from utils import *
from strategies.strategy1.strategy_1_Classes import *

def choosing_warehouse(warehouses_list: list[int], warehouses_orders: list[int], warehouses_interest: list[int])-> Warehouse | None:
    """
    chooses the most interesting warehouse
    """
    most_interesting_warehouse = None
    max_interest = 0
    for warehouse in warehouses_list:
        warehouse_interest = warehouses_interest[warehouse.warehouse_id]*len(warehouses_orders[warehouse.warehouse_id])
        if warehouse_interest > max_interest:
            max_interest = warehouse.interest
            most_interesting_warehouse = warehouse
    
    #print(f'warehouse {warehouse.warehouse_id} is the most interesting with {warehouse_interest} interest')
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
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict, warehouses_list, orders_list = challenge_data
    
    new_orders_list = [None] * len(orders_list)
    for order in orders_list:
        new_orders_list[order.order_id] = IOrder(order)
    
    new_warehouses_list = [None] * len(warehouses_list)
    for warehouse in warehouses_list:
        new_warehouses_list[warehouse.warehouse_id] = IWarehouse(warehouse, products_weight)
    
    return [level_info, new_warehouses_list, new_orders_list, products_weight]

def solve(challenge_data):
    level_info : LevelInfo
    warehouses_list : list[Warehouse]
    order_list : list[Order]
    
    level_info, warehouses_list, orders_list, products_weight = update_classes(challenge_data)

    order_interest_list = [] #list[int, Order, Warehouse]
    #sort orders by interest:
    
    for index, order in enumerate(orders_list):
        
        interest = order.calculate_interest(warehouses_list, level_info)
        order_interest_list.append([interest, order])
    
    order_interest_list.sort(key=lambda x: x[0])
    
    #list[warehouse.id]->[warehouse_orders]
    warehouses_orders = [None] * len(warehouses_list)
    
    #trie quelles order sont dans quel warehouse
    
    for order_info in order_interest_list:
        order = order_info[1]
        
        warehouse = find_warehouse_containing_order(order, warehouses_list, level_info.max_dist)
        if warehouse != None:
            if warehouse.contains(order.items):
                for item in order.items:
                    warehouse.products_info[item] -= 1
                if warehouses_orders[warehouse.warehouse_id] == None:
                    warehouses_orders[warehouse.warehouse_id] = []
                else:
                    warehouses_orders[warehouse.warehouse_id].append(order)
    
    for warehouse_id,warehouse_orders in enumerate(warehouses_orders):
        print(f'warehouse {warehouse_id} contains {[n.order_id for n in warehouse_orders]}')
    
    #rajoute les items enlevé just avant
    for warehouse_id,warehouse_order in enumerate(warehouses_orders):
        warehouse = warehouses_list[warehouse_id]        
        for order in warehouse_order:
            for item in order.items:
                warehouse.products_info[item] += 1
    
    # using drones
    drone_count = level_info.drone_count
    
    #this part creates lists to store the orders for each of the warehouses
    
    total_order_number: int = 0
    for warehouse_orders in warehouses_orders:
        total_order_number += len(warehouse_orders)
        for order in warehouse_orders:
            order.init_current_orders_status()
    total_order_index: int = 0
    
    #this creates the list to calculate the interest of each warehouse during the simulation
    warehouse_interest = []
    for warehouse_id, warehouse_orders in enumerate(warehouses_orders):
        warehouse_interest.append(warehouses_list[warehouse_id].interest/len(warehouse_orders))
    
    #this part initializes the drones and puts them in a list
    #it also creates a memory to store actions to be executed later on
    
    warehouse0 = warehouses_list[0]
    drones_list= []
    drones_memory = []
    
    for i in range  (drone_count):
        
        drone_state = 2
        drone = Drone(warehouse0.coordinates, level_info.max_load, level_info.products_weight, i)
        drone.state = drone_state
        drone.warehouse = choosing_warehouse(warehouses_list, warehouses_orders, warehouse_interest)
        drones_list.append(drone)
        drones_memory.append([])
        drone.state = 0
    
    #deux drone ne pourront pas travailler sur la même order
    #après chaque commande complète le drone cherche le warehous le plus interessant
    solution = ''
    
    
    if False:
        order = orders_list[913]
        print(f' does order {order.order_id} require {163}: {order.require({163:1})}')
        print(order.items)
        print(f'warehouse 3 contains object 162:{warehouses_list[2].contains({162: 1})}')
    
    overall_state = True
    tick = 0
    while tick < level_info.deadline and total_order_index < total_order_number:
        tick += 1
        for drone in drones_list:
            #print(f'{tick} drone: {drone.drone_id}, drone state: {drone.state}, drone current load: {drone.current_load}, is busy: {drone.drone_busy()}, overall state {overall_state}')
            if not overall_state:
                drone.state = 1
            state = drone.state
            memory = drones_memory[drone.drone_id]         
            drone.tick()
            if drone.drone_busy():
                    continue
            else:
                if state == 0:
                    nombre_items = 0
                    while overall_state and nombre_items == 0:
                        warehouse = drone.warehouse
                        warehouse_orders = warehouses_orders[warehouse.warehouse_id]
                        if len(order.current_items) == 0:
                            if len(warehouses_orders[warehouse.warehouse_id]) == 0:
                                warehouse = choosing_warehouse(warehouses_list, warehouses_orders, warehouse_interest)
                                warehouse_orders = warehouses_orders[warehouse.warehouse_id]
                                drone.warehouse = warehouse
                                print(f'Drone {drone.drone_id} choosed warehouse {warehouse.warehouse_id} with {len(warehouses_orders[warehouse.warehouse_id])} orders')
                                if len(warehouse_orders) == 0:
                                    overall_state = False
                            else:
                                warehouse_orders.pop(0)
                        
                        warehouse_orders = warehouses_orders[warehouse.warehouse_id]
                        if type(warehouse_orders) == IOrder:
                            warehouse_orders = [warehouse_orders]
                        
                        if overall_state and len(warehouse_orders) != 0 :
                            order = warehouse_orders[0]
                            nombre_items = len(order.current_items)
                        else:
                            warehouses_orders.pop(0)
                    
                    if overall_state:
                        product_type = order.current_items[0]

                    if drone.current_load + products_weight[product_type] < level_info.max_load :
                        if len(order.current_items) != 0:
                            #print(f'order: {order.order_id} contains: {order.current_items}')
                            print(f"Drone {drone.drone_id} Started loading product {product_type} from warehouse {warehouse.warehouse_id} at tick {tick} for order {order.order_id}")
                            #print(len(order.current_items))
                            drone.load({product_type: 1},warehouse)
                            drone.state = 0
                            solution += f"{drone.drone_id} L {warehouse.warehouse_id} {product_type} 1\n"
                            memory.append([order, product_type])
                            order.current_items.pop(0)
                            if len(order.current_items) == 0:
                                warehouse_orders.pop(0)
                                if len(warehouse_orders) == 0:
                                    drone.warehouse = choosing_warehouse(warehouses_list, warehouses_orders, warehouse_interest)
                                    f'drone {drone.drone_id} choosed warehouse {warehouse.warehouse_id}'
                        else:
                            warehouse_orders.pop(0)
                            print(len(warehouse_orders))
                            if len(warehouse_orders) == 0:
                                drone.warehouse = choosing_warehouse(warehouses_list, warehouses_orders, warehouse_interest)
                                f'Drone {drone.drone_id} choosed warehouse {warehouse.warehouse_id}'
                    else:
                        drone.state = 1
                
                elif state == 1:
                    #this part changes the most as now we can execute the memory in the drone
                    if len(memory) != 0:
                        #print(f'object in inventory:{[n[1] for n in memory]}')
                        order, product_type = memory[0]
                        print(f"Drone {drone.drone_id} Started delivering product {product_type} for order {order.order_id} at tick {tick}")
                        drone.deliver({product_type:1}, order)
                        drone.state = 1
                        solution += f"{drone.drone_id} D {order.order_id} {product_type} 1\n"
                        memory.pop(0)
                    else:
                        drone.state = 0
    
    commands_amount = len(solution.split('\n'))
    solution = f"{commands_amount}\n{solution}"
    return solution

#drone tries to take items from an order from the wrong warehouse