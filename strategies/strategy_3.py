from classes import Drone
from utils import dist
from utils import calculate_weigth


def solve(challenge_data):
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict, warehouses_list, orders_list, tick, score = challenge_data

    debug = False
    tick.value = -1
    order_index = 0
    orders = orders_list

    # orders.sort(key=lambda order: (len(order.items), dist(order.coordinates, (rows//2, columns//2))))
    orders.sort(key=lambda order: (len(order.items), dist(order.coordinates, warehouses_list[0].coordinates)))

    drones: list = []
    for i in range(drone_count):
        drones.append(Drone(warehouses_list[0].coordinates, max_load, products_weight, i))

    solution = ""

    order = orders[order_index]
    while tick.value < deadline and order_index < len(orders):
        tick.value += 1

        for i in range(drone_count):
            drone = drones[i]

            drone.tick()
            if drone.drone_busy():
                continue

            if len(order.remaining_items) == 0:
                if debug:
                    print(f"All items of order {order_index} are atributed (tick : {tick.value})")
                order_index += 1
                if order_index >= len(orders):
                    continue
                order = orders[order_index]

            product_type = order.remaining_items[0]
            if drone.state == 0 and tick.value < deadline:
                selected_warehouse = None
                warehouses_ordered_list = sorted(warehouses_list, key=lambda warehouse: dist(warehouse.coordinates, drone.coordinates))
                for warehouse in warehouses_ordered_list:
                    if warehouse.predicted_products_info[product_type] > 0:
                        selected_warehouse = warehouse
                        break

                can_still_load_items = True
                products = {}
                while can_still_load_items and order_index < len(orders):
                    if len(order.remaining_items) == 0:
                        if debug:
                            print(f"All items of order {order_index} are atributed (tick : {tick.value})")
                        order_index += 1
                        if order_index >= len(orders):
                            continue
                        order = orders[order_index]
                    
                    interesting_items = []
                    order_remaining_items_hist = {}
                    for item in order.remaining_items:
                        if item in order_remaining_items_hist:
                            order_remaining_items_hist[item] += 1
                        else:
                            order_remaining_items_hist[item] = 1

                    for item in order_remaining_items_hist:
                        if item in products:
                            available = selected_warehouse.predicted_products_info[item] - products[item]
                        else:
                            available = selected_warehouse.predicted_products_info[item]

                        if available > 0:
                            amount = min(available, order_remaining_items_hist[item])
                            for _ in range(amount):
                                interesting_items.append(item)

                    if len(interesting_items) == 0:
                        break
                    else:
                        item_index = 0
                        product = interesting_items[item_index]
                        can_still_load_items = calculate_weigth(products, products_weight) + products_weight[product] < max_load
                        take_more_items = can_still_load_items and item_index <= len(interesting_items) - 1
                        while take_more_items:
                            if product in products:
                                products[product] += 1
                            else:
                                products[product] = 1
                            
                            order.remaining_items.remove(product)
                            if debug:
                                print(f"Started loading product {product} from warehouse {selected_warehouse.warehouse_id} at tick {tick.value} by drone {i} for order {order.order_id}")
                            solution += f"{i} L {selected_warehouse.warehouse_id} {product} 1\n"

                            drone.orders_memory.append([order, product])

                            item_index += 1
                            if item_index <= len(interesting_items) - 1:
                                product = interesting_items[item_index]
                                can_still_load_items = calculate_weigth(products, products_weight) + products_weight[product] < max_load
                                take_more_items = can_still_load_items
                            else:
                                can_still_load_items = True
                                take_more_items = False

                drone.load(products, selected_warehouse)
                drone.state = 1

            elif drone.state == 1:
                if len(drone.orders_memory) != 0:
                    memory_order, memory_product_type = drone.orders_memory.pop(0)
                    if debug:
                        print(f"Drone {i} Started delivering product {memory_product_type} for order {memory_order.order_id} at tick {tick.value}")
                    drone.deliver({memory_product_type: 1}, memory_order)
                    drone.state = 1
                    solution += f"{i} D {memory_order.order_id} {memory_product_type} 1\n"
                else:
                    drone.state = 0

    while tick.value < deadline:
        tick.value += 1
        for i in range(drone_count):
            drone = drones[i]
            drone.tick()

            if drone.drone_busy():
                continue

            if drone.state == 1:
                if len(drone.orders_memory) != 0:
                    order, product_type = drone.orders_memory.pop(0)
                    if debug:
                        print(f"Drone {i} Started delivering product {product_type} for order {order.order_id} at tick {tick.value} for order {order.order_id}")
                    drone.deliver({product_type: 1}, order)
                    drone.state = 1
                    solution += f"{i} D {order.order_id} {product_type} 1\n"

                else:
                    drone.state = 0

    print(f"Score: {score.value}")

    solution = solution[:-1]
    commands_amount = len(solution.split('\n'))
    solution = f"{commands_amount}\n{solution}"
    return solution
