from __future__ import annotations

# stocker les poids des produits:
Weights = dict[int]


# stocker les objects Warehouse dans une dictionnaire liant un tuple de coordonnées aux objects
class Warehouse:
    def __init__(self, coordinates: tuple[int, int], products_info: dict[int]):
        self.products_info = products_info
        self.coordinates = coordinates


class Order:
    def __init__(self, coordinates: tuple[int, int], items: list[int]):
        self.items = items
        self.coordinates = coordinates


class Drone:
    def __init__(self, coordinates: tuple[int, int], state: int, item):
        self.state = state  # 0:move,1:deliver,2:load
        self.coordinates = coordinates


class Restrictions:
    def __init__(self, row_number: int, column_number: int, drone_number: int, deadline: int, drone_max_load: int):
        self.drone_max_load = drone_max_load
        self.deadline = deadline
        self.drone_number = drone_number
        self.column_number = column_number
        self.row_number = row_number


class Map_sections_delimitations:
    def __init__(self, coordinates: tuple[int, int]):
        self.coordinates = coordinates


class Utilities:  # can and should be changed ASAP
    def __init__(self):
        self.orders_info: list[Order] = []
        self.orders_number: int | None = None
        self.warehouses_number: int | None = None
        self.weights: list[str] = []
        self.products_number: int | None = None
        self.warehouses_info: list[Warehouse] = []

    def get_products_info(self, products_number: int, products_data_line: str):
        self.products_number = products_number
        weights: list[str] = products_data_line.split(" ")
        self.weights = weights

    def get_warehouses_info(self, warehouses_number: int, warehouse_data_lines: list[str]):
        self.warehouses_number = warehouses_number
        index: int = 0
        x: int
        y: int
        while index < 2 * warehouses_number:
            x, y = warehouse_data_lines[index].split(" ")
            products_info: list[str] = warehouse_data_lines[index + 1].split(" ")
            index += 2
            warehouse = Warehouse(coordinates=(x, y), products_info=products_info)
            self.warehouses_info.append(warehouse)

    def get_orders_info(self, orders_number: int, orders_data_lines):
        self.orders_number = orders_number
        index: int = 0
        x: int
        y: int
        while index < 3 * orders_number:
            x, y = orders_data_lines[index].split(" ")
            order_product_number: int = orders_data_lines[index + 1]
            order_info: list[int] = orders_data_lines[index + 2].split(" ")
            index += 3
            order = Order(coordinates=(x, y), item_number=order_product_number, items=order_info)
            self.orders_info.append(order)


if __name__ == '__main__':
    product = Product((53, 65), 34, 23)
