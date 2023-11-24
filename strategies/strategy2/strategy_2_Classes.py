from classes import Warehouse, Drone, Order
from mathematiks import dist


# max_weight is the maximum weight of an item + 1

class LevelInfo:

    def __init__(self, challenge_data) -> None:
        rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data
        self.rows = rows
        self.columns = columns
        self.max_dist = rows + columns
        self.drone_count = drone_count
        self.deadline = deadline
        self.max_load = max_load
        self.products_weight = products_weight
        self.max_weight = max(products_weight) + 1
        self.warehouse_number = len(warehouses_dict.keys())
        self.order_number = len(orders_dict.keys())


class Item():
    """
    A class representing a product.

    Attributes:
    - product_type (int): An integer representing the type of the product.
    - product_weight (int): An integer representing the weight of the product.
    - product_availability (int): An integer representing the availability of the product on the map.
    """

    def __init__(self, product_type: int, product_weight: int):
        self.type = product_type
        self.weight = product_weight
        self.availability: int = 0


class IWarehouse(Warehouse):
    """
    A class representing a warehouse that stores products.

    Attributes:
    - warehouse_interest: int: The interest of the warehouse.
    - warehouse_id (int): An optional integer representing the ID of the warehouse.
    - coordinates (tuple[int, int]): The coordinates of the warehouse.
    - products_info (list[int]): A list of integers representing the quantity of each product stored in the warehouse.
    - drones_on_use: list[int] = []: A list of the Drones Objects that are currently using the warehouse as a hive.
    - complete_orders: list[Order]: A list of the Orders that are complete within the warehouse.
    - max_weight (int): The maximum weight of an item + 1.
    """

    def __init__(self, warehouse_id: int,
                 coordinates: tuple[int, int], products_info: list[tuple[Item, int]],
                 max_weight: int
                 ):
        Warehouse.__init__(self, coordinates, products_info, warehouse_id)
        self.interest: int = 0
        self.drones_on_use: list[int] = []
        self.complete_orders: list[Order] = []

        self.calculate_interest(max_weight)

    def contains_products(self, products: list[int]):
        """
        Ckecks if the warehouse contains the given products.

        Args:
            products (list[int]): A list of integers representing the IDs of the products.
        """
        contain = True
        for product in products:
            if self.products_info[product] < products.count(product):
                contain = False

        return contain

    def calculate_interest(self, max_weight: int):
        """Calculate the interest of the warehouse from its products_info."""
        # Trier les produits par distance (en ordre croissant) et poids (en ordre croissant)
        sorted_products = sorted(self.products_info, key=lambda x: (x[0].distance, x[0].weight))

        for i, product_info in enumerate(sorted_products):
            product_type, product_number = product_info
            distance_contribution = 1 / (product_type.distance + 1)  # Fonction décroissante de la distance
            weight_contribution = max(0, max_weight - product_type.weight)

            priority_multiplier = 1 / (i + 1)  # Priorité décroissante avec l'index dans la liste triée

            self.interest += (distance_contribution + weight_contribution) * product_number * priority_multiplier
    def remove_item(self, item: int, max_weight: int, item_list: list[Item]):
        """the function removes an item from the warehouse and changes it's interest"""
        product = item_list[item]
        assert self.products_info[item] > 0
        self.products_info[item] -= 1
        self.interest -= (max_weight - product.weight)

    def add_item(self, item: int, max_weight: int, item_list: list[Item]):
        """the function adds an item to the warehouse and changes it's interest"""
        product = item_list[item]
        self.products_info[item] += 1
        self.interest += (max_weight - product.weight)


class IOrder(Order):
    def __init__(self, order_id: int, coordinates: tuple[int, int], items: list[int]
                 ):
        """
        A class representing an order that stores products.

        Attributes:
        - order_interest: int | None: The interest of the order.
        - order_id (int): An optional integer representing the ID of the order.
        - coordinates (tuple[int, int]): The coordinates of the order.
        - items (list[int]): A list of integers representing the IDs of the products ordered.
        - closest_order_warehouse: Warehouse | None: The closest warehouse that contains the order.
        - weight: int: The total weight of the order.
        """

        Order.__init__(self, coordinates, items, order_id)
        self.order_interest: int | None = None
        self.closest_order_warehouse: Warehouse = None
        self.weight: int = 0

    def update_weight(self, products_weight: list[int]):
        """the function calculates the weight of the order from its items"""
        for item in self.items:
            self.weight += item.weight

    def calculate_interest(self, warehouses_list: list[IWarehouse], level_info: LevelInfo,
                           items_weight_coeff: int | None = 1, items_weight_pow: int | None = 1,
                           items_num_coeff: int | None = 1, items_num_pow: int | None = 1,
                           command_dist_coeff: int | None = 1, command_dist_pow: int | None = 1):
        """the function calculates the total interest of the order from various variables"""

        items_num: int = len(self.items)
        weight_value: int = items_num * level_info.max_weight - self.weight

        # finds the closest warehouse that contains the order and calculates the distance
        min_distance_value: int = level_info.max_dist
        closest_warehouse: Warehouse = warehouses_list[0]
        for warehouse in warehouses_list:

            print(f'bug={[n.type for n in self.items]}')
            if warehouse.contains([n.type for n in self.items]):
                distance_value: int = dist(warehouse.coordinates, self.coordinates)
                if distance_value < min_distance_value:
                    closest_warehouse = warehouse
                    min_distance_value = distance_value

        self.closest_order_warehouse = closest_warehouse

        # calculates the total interest of the order
        weight_interest: int = (items_weight_coeff * weight_value ** items_weight_pow)
        number_interest: int = (items_num_coeff * items_num ** items_num_pow)
        dist_interest: int = (command_dist_coeff * min_distance_value ** command_dist_pow)

        total_interest: int = weight_interest + number_interest + dist_interest

        self.order_interest = total_interest

        return self.interest



