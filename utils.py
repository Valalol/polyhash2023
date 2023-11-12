from classes import *

def find_nearest_warehouse(coordinates: tuple[int,int], warehouses_dict: dict[tuple[int,int], Warehouse], max_dist: int) -> Warehouse | None:
    
    min_dist: int = max_dist
    closest_warehouse: Warehouse | None = None
    
    for warehouse in warehouses_dict.values():
        
        distance: int = dist(coordinates, warehouse.coordinates)
        if distance <= min_dist:
            min_dist = distance
            closest_warehouse = warehouse
            
    return closest_warehouse

def check_b_in_a(container1: list | dict, container2: list | dict):
    retour: bool = True
    if container2 is dict:
        for product_type, product_number in container2.items():
            if container1[product_type] < product_number:
                retour = False
    else:
        for product in container2:
            if container1[product_type] < 1:
                retour = False
    return retour
        