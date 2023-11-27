from classes import Warehouse, Drone, Order
from mathematiks import dist


class LevelInfo:
    def __init__(self, challenge_data) -> None:
        (rows, columns, drone_count, deadline, max_load, products_weight,
         warehouses_dict, orders_dict) = challenge_data

        self.rows = rows
        self.columns = columns
        self.max_dist = rows + columns
        self.drone_count = drone_count
        self.deadline = deadline
        self.max_load = max_load
        self.products_weight = products_weight
        self.max_weight = max(products_weight) + 1
        self.warehouse_number = len(warehouses_dict)
        self.order_number = len(orders_dict)


class Item:
    def __init__(self, product_type: int, product_weight: int) -> None:
        self.type = product_type
        self.weight = product_weight
        self.availability = 0


class IWarehouse(Warehouse):
    def __init__(self, warehouse_id: int, coordinates: tuple[int, int],
                 products_info: list[tuple[Item, int]], max_weight: int) -> None:
        super().__init__(coordinates, products_info, warehouse_id)
        self.interest = 0
        self.drones_on_use = []
        self.complete_orders = []

        self.calculate_interest(max_weight)

    def contains_products(self, products: list[int]) -> bool:
        """Check if the warehouse contains the given products."""
        return all(self.products_info[product] >= products.count(product) for product in products)

    def calculate_interest(self, max_weight: int) -> None:
        """Calculate the interest of the warehouse from its products_info."""
        sorted_products = sorted(self.products_info, key=lambda x: (x[0].distance, x[0].weight))

        for i, (product_type, product_number) in enumerate(sorted_products):
            distance_contribution = 1 / (product_type.distance + 1)
            weight_contribution = max(0, max_weight - product_type.weight)
            priority_multiplier = 1 / (i + 1)

            self.interest += (distance_contribution + weight_contribution) * product_number * priority_multiplier

    def remove_item(self, item: int, max_weight: int, item_list: list[Item]) -> None:
        """Remove an item from the warehouse and update its interest."""
        product = item_list[item]
        assert self.products_info[item] > 0
        self.products_info[item] -= 1
        self.interest -= (max_weight - product.weight)

    def add_item(self, item: int, max_weight: int, item_list: list[Item]) -> None:
        """Add an item to the warehouse and update its interest."""
        product = item_list[item]
        self.products_info[item] += 1
        self.interest += (max_weight - product.weight)


class IOrder(Order):
    def __init__(self, order_id: int, coordinates: tuple[int, int], items: list[int]) -> None:
        super().__init__(coordinates, items, order_id)
        self.order_interest = None
        self.closest_order_warehouse = None
        self.weight = 0

    def update_weight(self, products_weight: list[int]) -> None:
        """Calculate the weight of the order from its items."""
        self.weight = sum(products_weight[item] for item in self.items)

    def calculate_interest(self, warehouses_list: list[IWarehouse],
                           items_weight_coeff: int = 1, items_weight_pow: int = 1,
                           items_num_coeff: int = 1, items_num_pow: int = 1,
                           command_dist_coeff: int = 1, command_dist_pow: int = 1) -> int:
        """Calculate the total interest of the order from various variables."""
        items_num = len(self.items)
        weight_value = items_num * self.max_weight - self.weight

        min_distance_value = float('inf')
        closest_warehouse = warehouses_list[0]

        for warehouse in warehouses_list:
            if warehouse.contains_products([n.type for n in self.items]):
                distance_value = dist(warehouse.coordinates, self.coordinates)
                if distance_value < min_distance_value:
                    closest_warehouse = warehouse
                    min_distance_value = distance_value

        self.closest_order_warehouse = closest_warehouse

        weight_interest = items_weight_coeff * weight_value ** items_weight_pow
        number_interest = items_num_coeff * items_num ** items_num_pow
        dist_interest = command_dist_coeff * min_distance_value ** command_dist_pow

        total_interest = weight_interest + number_interest + dist_interest

        self.order_interest = total_interest

        return total_interest
