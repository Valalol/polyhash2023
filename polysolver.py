#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""

from classes import *
import Strategies.strategy_1 as strategy_1


def solve(challenge_data: list, solve_strategy: int = 1):
    """
    Solves the given challenge data using the specified strategy.
    
    Args:
    - challenge_data (list): A list containing the following challenge data:
        - rows (int): The number of rows in the grid.
        - columns (int): The number of columns in the grid.
        - drone_count (int): The number of drones available.
        - deadline (int): The number of turns available.
        - max_load (int): The maximum weight that a drone can carry.
        - products_weight (list): A list containing the weight of each product type.
        - warehouses_dict (dict): A dictionary containing the warehouses information.
        - orders_dict (dict): A dictionary containing the orders information.
            - order_info (list): A list containing the order information. Wich are : list of items
    - solve_strategy (int): An integer representing the strategy to use for solving the challenge data.
    
    Returns:
    - solution (list): A list containing the solution to the challenge data.
    """
def solve(challenge_data: list, solve_strategy: int = 1):
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data
    
    if solve_strategy == 0:
        # Dumb brute force solution
        # starts with the first order and uses only one drone
        tick = 0
        order_index = 0
        orders = list(orders_dict.values())
        drone = Drone(list(warehouses_dict.keys())[0], max_load, products_weight)
        
        while tick < deadline and order_index < len(orders):
            product_index = 0
            order = orders[order_index]
            
            state = 2
            
            while tick < deadline and product_index < len(order.items):
                product_type = order.items[product_index]
                
                drone.tick()
                tick += 1
                
                if drone.drone_busy():
                    continue
                    
                
                if state == 3:
                    drone.load({product_type: 1})
                    print(f"Loaded product {product_type} at tick {tick}")
                    state = 0   
                
                elif state == 0:
                    drone.travel(order.coordinates)
                    print(f"Started travelling with product index {product_index} for order {order_index} at tick {tick}")
                    state = 1
                
                elif state == 1:
                    drone.unload({product_type: 1})
                    print(f"Unloaded product {product_type} at tick {tick}")
                    product_index += 1
                    order.items.remove(product_type)
                    if len(order.items) == 0:
                        order_index += 1
                        order = orders[order_index]
                        print(f"Order {order_index} completed at tick {tick}")
                    state = 2
                
                elif state == 2:
                    for warehouse in warehouses_dict.values():
                        if warehouse.products_info[product_type] > 0:
                            warehouse_coordinates = warehouse.coordinates
                            break
                    drone.travel(warehouse_coordinates)
                    print(f"Started travelling to warehouse ({warehouse_coordinates}) at tick {tick}")
                    state = 3
    
    
    
    
    if solve_strategy == 1:
        # sort orders by the sum of the distances between the warehouse and the orders for each product type 
        # (the order with the smallest sum is processed first)
        def difficulty_score(order):
            weight_sum = sum(products_weight[i] for i in order.items)
            print(weight_sum)
        
        
        orders = list(orders_dict.values())
        orders_and_scores = [(order, difficulty_score(order)) for order in orders]
        
        # TODO: UNFINISHED
    if solve_strategy == 2:
        solution = strategy_1.solve(challenge_data)
        
        
        
    
    
    
    
    
    # TODO: implement other strategies by adding elif blocks
