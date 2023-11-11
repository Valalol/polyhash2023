from mathematiks import dist()
from new_data_classes import *
# calulating the worth of each command:
max_dist = 1000

# calculate the interest of a given order
def interest_funct(order: Order, warehouses_dict: dict,
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
    
    items_number: int = len(order.items)
    
    #calculate minimum distance of a warehouse who has the items & registers the warehouse
    min_distance_value: int = max_dist
    closest_warehouse: Warehouse = None
    
    for warehouse in warehouse_dict.values():
        as_items: bool = True

        #checks if the warehouse has the items
        while i < len(order.items) and as_items is True:
            if warehouse.products_info[item] = 0:
                as_items = False

        #checks if the distance of the warehouse is less then the known closest's one
        if as_items is True :
            distance_value: int = dist(warehouse.coordinates,order.coordinates)
            if distance_value < min_distance_value:
                closest_warehouse = warehouse
                min_distance_value = distance_value

    #calculates the total interest of the order
    weight_interest: int = ( items_weight_coeff*weight_value**items_weight_pow )
    number_interest: int = ( items_number_coeff*items_number**items_number_pow )
    dist_interest: int = ( command_dist_coeff*min_distance_value**command_dist_pow )
    
    total_interest: int = weight_interest + number_interest + dist_interest
    
    return total_interest, closest_warehouse


def solve(challenge_data):
    
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data

    order_interest_list = [] #list[int, Order, Warehouse]
    #sort orders by interest:
    for index,order in enumerate(orders_dict.values()):
        
        interest, warehouse = interest_funct(order, warehouses_dict)
        
        #inserts the order_info in a sorted way:
        min,max = 0, len(order_interest_list)-1
        moy = (min + max) // 2
        
        if index !=2:
            while not (order_interest_list[moy][0] <= c_interest <= liste[moy+1][0]):
                moy = (min + max) // 2
                if order_interest_list[moy][0] < c_interest:
                    min = moy + 1
                else:
                    max = moy - 1
                order_interest_list.insert(moy+1, [c_interest, order, warehouse])
                continue
        
        elif index == 1:
            order_interest_list.append([c_interest, order, warehouse])
        elif index == 2:
            if order_interest_list[0] > c_interest:
                order_interest_list.insert(0, [c_interest, order, warehouse])
            else:
                order_interest_list.append([c_interest, order, warehouse])

    warehouse_dict_current_state = warehouses_dict.copy()
    warehouses_dict_new = warehouses_dict.copy()
    for warehouse in warehouses_dict_new.values():
        warehouse.products_info = []
    
    for order in order_interest_list:
        c_interest, order, warehouse = tuple(order)
        
        #checks if the items in the order is in the warehouse
        is_in_warehouse: bool = True
        while index < len(order.items) and is_in_warehouse is True:
            if warehouse.products_info[order.items[index]] = 0:
                is_in_warehouse = False

        #if the items are in the warehouse then it removes them from the warehouse and adds the order to the new warehouse_dict
        if is_in_warehouse :
            for item in order.items:
                warehouse_dict_current_state[warehouse.coordinates].products_info[item] -= 1:
            warehouses_dict_new(warehouse.coordinates).products_info.append(order)
        else:
            #does nothing for now
            pass
    
    tick = 0
    order_index = 0
    warehouse0 = list(warehouses_dict_new.values())[0]
    orders = warehouse.products_info
    drone = Drone(warehouse0.coordinates, max_load, products_weight)
    
    while tick < deadline and order_index < len(orders):
        product_index = 0
        order = orders[order_index]
        
        state = 2
        
        while tick < deadline and product_index < len(order.items):
            product_type = order.items[product_index]
            
            drone.tick()
            tick += 1
            
            if drone.drone_busy():
                continue
                
            
            if state == 3:
                drone.load({product_type: 1})
                print(f"Loaded product {product_type} at tick {tick}")
                state = 0   
            
            elif state == 0:
                drone.travel(order.coordinates)
                print(f"Started travelling with product index {product_index} for order {order_index} at tick {tick}")
                state = 1
            
            elif state == 1:
                drone.unload({product_type: 1})
                print(f"Unloaded product {product_type} at tick {tick}")
                product_index += 1
                order.items.remove(product_type)
                if len(order.items) == 0:
                    order_index += 1
                    order = orders[order_index]
                    print(f"Order {order_index} completed at tick {tick}")
                state = 2
            
            elif state == 2:
                for warehouse in warehouses_dict.values():
                    if warehouse.products_info[product_type] > 0:
                        warehouse_coordinates = warehouse.coordinates
                        break
                drone.travel(warehouse_coordinates)
                print(f"Started travelling to warehouse ({warehouse_coordinates}) at tick {tick}")
                state = 3
    
    
        
    
        
    
