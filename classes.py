from __future__ import annotations

# stocker les poids des produits:
Weights = dict[int]


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


if __name__ == '__main__':
    pass
