from classes import *

def solve(challenge_data):
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data

    # Dumb brute force solution
    # starts with the first order and uses only one drone

    tick = 0
    order_index = 0
    orders = list(orders_dict.values())
    drone = Drone(list(warehouses_dict.keys())[0], max_load, products_weight, 0)

    solution = ""

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
                solution += f"0 D {order_index} {product_type} 1\n"
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
                selected_warehouse = None
                for warehouse in warehouses_dict.values():
                    if warehouse.products_info[product_type] > 0:
                        selected_warehouse = warehouse
                        break
                drone.travel(selected_warehouse.coordinates)
                print(f"Started travelling to warehouse ({selected_warehouse.coordinates}) at tick {tick}")
                solution += f"0 L {selected_warehouse.warehouse_id} {product_type} 1\n"
                state = 3
    
    solution = solution[:-1]
    solution = f"{len(solution)}\n{solution}"
    return solution