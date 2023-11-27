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
            min_dist = distance
            closest_warehouse = warehouse
            
    return closest_warehouse

def find_warehouse_containing_order(order: Order, warehouses_container: list[Warehouse] | dict[Warehouse], max_dist: int, Item_class = False) -> Warehouse | None:
    
    min_dist: int = max_dist
    closest_warehouse: Warehouse | None = None
    
    if Item_class:
        for warehouse in warehouses_container:
            
            distance: int = dist(order.coordinates, warehouse.coordinates)
        
            if distance <= min_dist and warehouse.contains(order.items):
                min_dist = distance
                closest_warehouse = warehouse
        
    else:
        for warehouse in list(warehouses_container.values()):
            
            distance: int = dist(order.coordinates, warehouse.coordinates)
        
            if distance <= min_dist and warehouse.contains(order.items):
                min_dist = distance
                closest_warehouse = warehouse
                
    return closest_warehouse

def check_b_in_a(container1: list | dict, container2: list | dict, container2_list_type: int = 1):
    retour: bool = True
    if type(container2) is dict:
        for product_type, product_number in container2.items():
            if container1[product_type] < product_number:
                retour = False
    else:
        
        if container2_list_type == 1:
            for product_type, product_number in enumerate(container2):
                if container1[product_type] < product_number:
                    retour = False
        else:
            for product_type in container2:
                if container1[product_type] < container2.count(product_type):
                    retour = False
    return retour

def calculate_weigth(container: list | dict, weight_list: list[int], list_type: int = 1,):
    retour : int = 0
    if container is dict:
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
