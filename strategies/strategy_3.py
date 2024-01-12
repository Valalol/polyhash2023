from classes import *

def solve(challenge_data):
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict, warehouses_list, orders_list = challenge_data

    # Dumb brute force solution
    # starts with the first order and uses only one drone

    tick = -1
    order_index = 0
    orders = orders_list
    drone: list = []
    for i in range (drone_count):
        drone.append(Drone(list(warehouses_dict.keys())[0], max_load, products_weight, i))

    solution = ""


    while tick < deadline and order_index < len(orders):
        product_index = 0
        order = orders[order_index]
        
        
        while tick < deadline and len(order.remaining_items) > 0:
            tick += 1

            for i in range (drone_count):
                
                product_type = order.remaining_items[0]

                drone[i].tick()

                if drone[i].drone_busy():
                    continue
                
                #print(f"Drone {i} has items : {drone[i].item_dict}, {tick}, drone busy for {drone[i].turns_left}")

                if drone[i].state == 0:
                    selected_warehouse = None
                    for warehouse in warehouses_list:
                        if warehouse.products_info[product_type] > 0:
                            selected_warehouse = warehouse
                            break
                    drone[i].load({product_type: 1}, selected_warehouse)
                    drone[i].current_order = order
                    order.remaining_items.pop(0)
                    print(f"Started loading product {product_type} from warehouse {selected_warehouse.warehouse_id} at tick {tick} by drone {i}")
                    solution += f"{i} L {selected_warehouse.warehouse_id} {product_type} 1\n"
                    drone[i].state = 1

                elif drone[i].state == 1:
                    delivered_item = None
                    for item_stocked in drone[i].item_dict:
                        if drone[i].item_dict[item_stocked] >= 1:
                            delivered_item = item_stocked
                            break
                    drone[i].deliver({delivered_item: 1}, drone[i].current_order)
                    print(f"Started delivering product {delivered_item} for order {drone[i].current_order.order_id} at tick {tick} by drone {i}")
                    solution += f"{i} D {drone[i].current_order.order_id} {delivered_item} 1\n"
                    product_index += 1
                    drone[i].state = 0
                
                #print(f"Drone {i} has items : {drone[i].item_dict}, {tick}, drone busy for {drone[i].turns_left}")

                if len(drone[i].current_order.remaining_items) == 0:
                    print(f"All items of order {order_index} are atributed (tick : {tick})")
                    order_index += 1
                    if order_index >= len(orders):
                        break
                    order = orders[order_index]
                

    
    
    solution = solution[:-1]
    commands_amount = len(solution.split('\n'))
    solution = f"{commands_amount}\n{solution}"
    return solution