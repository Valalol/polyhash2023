from __future__ import annotations
from classes import *

"""
variables:
    the format dictionary is of the form dict[product_type] -> product_number
    the format list 1 refers to the format: list[product_type] -> product_number
    the format list 2 refers to the format: list[index] -> product_type

functions:
    find_nearest_warehouse(coordinates, warehouses_dict) -> Warehouse 
        finds the nearest warehouse to the coordinates.
    check_b_in_a(container1, container2, list_type) -> bool
        checks if a container is contained in another container.
    calculate_weigth(container, weight_list, list_type) -> int
        calculates the total weight of a container.
"""


def find_nearest_warehouse(coordinates: tuple[int,int], warehouses_dict: dict[tuple[int,int], Warehouse], max_dist: int) -> Warehouse | None:
    min_dist: int = max_dist
    closest_warehouse: Warehouse | None = None

    for warehouse in warehouses_dict.values():
        
        distance: int = dist(coordinates, warehouse.coordinates)
        if distance <= min_dist:
            min_dist: int = distance
            closest_warehouse = warehouse

    return closest_warehouse


def find_warehouse_containing_order(order: Order, warehouses_container: list[Warehouse] | dict[Warehouse], max_dist: int) -> Warehouse | None:
    min_dist: int = max_dist
    closest_warehouse: Warehouse | None = None

    for warehouse in warehouses_container:
        distance: int = dist(order.coordinates, warehouse.coordinates)
    
        if distance <= min_dist and warehouse.contains(order.items):
            min_dist: int = distance
            closest_warehouse = warehouse

    return closest_warehouse


def check_b_in_a(container1: list | dict, container2: list | dict, container2_list_type: int = 1) -> bool:
    if type(container2) is dict:
        for product_type, product_number in container2.items():
            if type(container1) is dict:
                if product_type not in container1:
                    return False

            if container1[product_type] < product_number:
                return False
    else:
        if container2_list_type == 1:
            for product_type, product_number in enumerate(container2):
                if container1[product_type] < product_number:
                    return False
        else:
            for product_type in container2:
                if container1[product_type] < container2.count(product_type):
                    return False
    return True


def calculate_weigth(container: list | dict, weight_list: list[int], list_type: int = 1,) -> int:
    retour : int = 0
    if type(container) is dict:
        for product_type, product_number in container.items():
            retour += weight_list[product_type] * product_number
    else:
        if list_type ==1:
            for product_type in container:
                retour += weight_list[product_type]
        else:
            for product_type, product_number in enumerate(container):
                retour += weight_list[product_type] * product_number
    return retour


def dict_add(dict_original, dict_to_add) -> dict:
    for key in dict_to_add.keys():
        if key in dict_original.keys():
            dict_original[key] += dict_to_add[key]
        else:
            dict_original[key] = dict_to_add[key]
    return dict_original


def dict_subtract(dict_original, dict_to_sub) -> dict:
    for key in dict_to_sub.keys():
        if key not in dict_original.keys():
            raise Exception("1+ items are not available in stock")
        dict_original[key] -= dict_to_sub[key]
        if dict_original[key] < 0:
            raise Exception("1+ items are not available in stock")
    return dict_original


def dist(a: tuple[int, int], b: tuple[int, int]):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)


def items_total_weight(item_weights: list[int], items_list: dict[int]) -> int:
    somme: int = 0
    for item in items_list:
        quantity = items_list[item]
        somme += item_weights[item] * quantity
    return somme


if __name__ == '__main__':
    pass
