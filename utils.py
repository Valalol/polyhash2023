from classes import *

def find_nearest_warehouse(coordinates: tuple[int,int], warehouses_dict: dict[tuple[int,int], Warehouse], max_dist: int) -> Warehouse | None:
    
    min_dist: int = max_dist
    closest_warehouse: Warehouse | None = None
    
    for warehouse in warehouses_dict.values():
        
        distance: int = dist(coordinates, warehouse.coordinates)
        if distance < min_dist:
            min_dist = distance
            closest_warehouse = warehouse
            
    return closest_warehouse