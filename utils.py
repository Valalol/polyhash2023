def find_nearest_warehouse(coordinates, warehouses_dict):
    
    min_dist: int = max_dist
    closest_warehouse: Warehouse | None = None
    
    for warehouse in warehouse_dict.values():
        
        distance: int = dist(coordinates, warehouse.coordinates)
        if distance < min_dist:
            min_dist = distance
            closest_warehouse = warehouse
            
    return closest_warehouse