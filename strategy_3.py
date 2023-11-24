from classes import *

def solve(challenge_data):
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data

    # Dumb brute force solution
    # starts with the first order and uses only one drone

    tick = -1
    order_index = 0
    orders = list(orders_dict.values())
    drone: list = []
    for i in range (drone_count):
        drone.append(Drone(list(warehouses_dict.keys())[0], max_load, products_weight, 0))

    solution = ""


    while tick < deadline and order_index < len(orders):
        product_index = 0
        order = orders[order_index]
        
        state = 0
        
        while tick < deadline and len(order.items) > 0:
            product_type = order.items[0]
            
            tick += 1

            for i in range (drone_count):

                drone[i].tick()

                if drone[i].drone_busy():
                    continue
                    
                
                if state == 0:
                    selected_warehouse = None
                    for warehouse in warehouses_dict.values():
                        if warehouse.products_info[product_type] > 0:
                            selected_warehouse = warehouse
                            break
                    drone[i].load({product_type: 1}, selected_warehouse)
                    print(f"Started loading product {product_type} from warehouse {selected_warehouse.warehouse_id} at tick {tick}")
                    solution += f"{i} L {selected_warehouse.warehouse_id} {product_type} 1\n"
                    state = 1
                
                elif state == 1:
                    drone[i].deliver({product_type: 1}, order)
                    print(f"Started delivering product {product_type} for order {order_index} at tick {tick}")
                    solution += f"{i} D {order_index} {product_type} 1\n"
                    product_index += 1
                    if len(order.items) == 0:
                        print(f"Order {order_index} completed at tick {tick}")
                        order_index += 1
                        order = orders[order_index]
                    state = 0

    
    
    solution = solution[:-1]
    commands_amount = len(solution.split('\n'))
    solution = f"{commands_amount}\n{solution}"
    return solution