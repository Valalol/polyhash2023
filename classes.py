from __future__ import annotations

# stocker les poids des produits:
Weights = dict[int]

section_max_drones = 2


class Warehouse:
    def __init__(self, coordinates: tuple[int, int], products_info: dict[int]):
        self.products_info = products_info
        self.coordinates = coordinates


class Order:
    def __init__(self, coordinates: tuple[int, int], items: list[int]):
        self.items = items
        self.coordinates = coordinates


class Drone:
    def __init__(self, coordinates: tuple[int, int], state: int, items_weight: int, item_dict: dict[int]):
        self.state = state  # 0:move,1:deliver,2:load
        self.coordinates = coordinates
        self.item_dict = item_dict
        self.items_weight = items_weight


class MapSectionsDelimitations:
    def __init__(self, coordinates: tuple[int, int]):
        self.coordinates = coordinates


class MapSection:

    def __init__(self, coordinates: tuple[int, int], warehouse_list: list[Warehouse], order_list: list[Order],
                 drone_number: int):
        self.interest = None
        self.warehouse_list = warehouse_list
        self.order_list = order_list
        self.drone_number = drone_number
        self.coordinates = coordinates
        # maybe coordinates here is rendundant

    def set_interest(self, v_interest: int | None = None):
        interest = len(self.warehouse_list) * len(self.order_list) * (section_max_drones - self.drone_number)
        self.interest = interest


if __name__ == '__main__':
    pass
