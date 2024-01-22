from classes import Drone, Order, Warehouse
from utils import dist
from utils import calculate_weigth


def solve(challenge_data) -> str:
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict, warehouses_list, orders_list, tick, score = challenge_data

    tick.value = -1
    order_index: int = 0
    orders: list = orders_list

    # On trie les commandes par nombre d'item puis par distance à l'entrepôt de départ.
    orders.sort(key=lambda order: (len(order.items), dist(order.coordinates, warehouses_list[0].coordinates)))

    # On crée les drones
    drones: list = []
    for i in range(drone_count):
        drones.append(Drone(warehouses_list[0].coordinates, max_load, products_weight, i))

    solution: str = ""

    order: Order = orders[order_index]
    # Tant qu'il reste des commandes à traiter et que le temps n'est pas écoulé
    while tick.value < deadline and order_index < len(orders):
        tick.value += 1

        for i in range(drone_count):
            drone: Drone = drones[i]

            # On fait avancer le drone et on stop là si il est encore occupé après le tick
            drone.tick()
            if drone.drone_busy():
                continue

            # Si la commande est vide, on passe à la suivante
            if len(order.remaining_items) == 0:
                # print(f"All items of order {order_index} are atributed (tick : {tick.value})")
                order_index += 1
                if order_index >= len(orders):
                    continue
                order: Order = orders[order_index]

            # On récupère le premier produit de la commande actuelle et on cherche l'entrepôt le plus proche qui en contient
            product_type: int = order.remaining_items[0]
            if drone.state == 0 and tick.value < deadline:
                selected_warehouse: Warehouse | None = None
                warehouses_ordered_list = sorted(warehouses_list, key=lambda warehouse: dist(warehouse.coordinates, drone.coordinates))
                for warehouse in warehouses_ordered_list:
                    if warehouse.predicted_products_info[product_type] > 0:
                        selected_warehouse = warehouse
                        break

                # Tant que le drone n'est pas plein et que la commande est faisable depuis cet entrepôt, on continue de charger des produits
                can_still_load_items: bool = True
                products: dict = {}
                while can_still_load_items and order_index < len(orders):
                    # si la commande est vide, on passe à la suivante
                    if len(order.remaining_items) == 0:
                        # print(f"All items of order {order_index} are atributed (tick : {tick.value})")
                        order_index += 1
                        if order_index >= len(orders):
                            continue
                        order: Order = orders[order_index]

                    interesting_items: list = []
                    order_remaining_items_hist: dict = {}
                    for item in order.remaining_items:
                        if item in order_remaining_items_hist:
                            order_remaining_items_hist[item] += 1
                        else:
                            order_remaining_items_hist[item] = 1

                    # On note tous les produits intéressants de la commande (ceux qui sont dans l'entrepôt sélectionné)
                    for item in order_remaining_items_hist:
                        if item in products:
                            available: int = selected_warehouse.predicted_products_info[item] - products[item]
                        else:
                            available: int = selected_warehouse.predicted_products_info[item]

                        if available > 0:
                            amount: int = min(available, order_remaining_items_hist[item])
                            for _ in range(amount):
                                interesting_items.append(item)

                    if len(interesting_items) == 0:
                        break
                    else:
                        # Tant que le drone n'est pas plein et qu'il reste des produits intéressants à charger, on continue de charger des produits
                        # On calcule le poids des produits déjà chargés et du produit suivant
                        item_index: int = 0
                        product: int = interesting_items[item_index]
                        can_still_load_items: bool = calculate_weigth(products, products_weight) + products_weight[product] < max_load
                        take_more_items: bool = can_still_load_items and item_index <= len(interesting_items) - 1
                        while take_more_items:
                            # On ajoute le produit à la liste des produits à charger
                            if product in products:
                                products[product] += 1
                            else:
                                products[product] = 1

                            # On enlève le produit de la liste des produits restanats de la commande
                            order.remaining_items.remove(product)
                            # print(f"Started loading product {product} from warehouse {selected_warehouse.warehouse_id} at tick {tick.value} by drone {i} for order {order.order_id}")
                            # On note la saisie du produit dans la solution
                            solution += f"{i} L {selected_warehouse.warehouse_id} {product} 1\n"

                            # On note la commande et le produit dans la mémoire du drone
                            drone.orders_memory.append([order, product])

                            item_index += 1
                            if item_index <= len(interesting_items) - 1:
                                product = interesting_items[item_index]
                                can_still_load_items = calculate_weigth(products, products_weight) + products_weight[product] < max_load
                                take_more_items = can_still_load_items
                            else:
                                can_still_load_items = True
                                take_more_items = False

                # On envoit le drone à l'entrepôt sélectionné pour charger les produits
                drone.load(products, selected_warehouse)
                drone.state = 1

            # Si le drone est en état de livrer et qu'il reste des produits à livrer, on continue de livrer
            elif drone.state == 1:
                # Pour chaque élément de la mémoire du drone, on va livrer le produit pour la commande associée
                if len(drone.orders_memory) != 0:
                    memory_order, memory_product_type = drone.orders_memory.pop(0)
                    # print(f"Drone {i} Started delivering product {memory_product_type} for order {memory_order.order_id} at tick {tick.value}")
                    drone.deliver({memory_product_type: 1}, memory_order)
                    drone.state = 1
                    solution += f"{i} D {memory_order.order_id} {memory_product_type} 1\n"

                # S'il n'y a plus de produits à livrer, on passe le drone en état de chargement
                else:
                    drone.state = 0

    # On fait avancer les drones jusqu'à la fin du temps imparti pour qu'ils finissent de livrer les commandes en cours
    while tick.value < deadline:
        tick.value += 1
        for i in range(drone_count):
            drone: Drone = drones[i]
            drone.tick()

            if drone.drone_busy():
                continue

            if drone.state == 1:
                if len(drone.orders_memory) != 0:
                    order, product_type = drone.orders_memory.pop(0)
                    # print(f"Drone {i} Started delivering product {product_type} for order {order.order_id} at tick {tick.value} for order {order.order_id}")
                    drone.deliver({product_type: 1}, order)
                    drone.state = 1
                    solution += f"{i} D {order.order_id} {product_type} 1\n"

                else:
                    drone.state = 0

    # On affiche le score calculé pendant la simulation et on renvoit la solution formatée
    print(f"Score: {score.value}")

    solution = solution[:-1]
    commands_amount: int = len(solution.split('\n'))
    solution = f"{commands_amount}\n{solution}"
    return solution
