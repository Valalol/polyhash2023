#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""

from classes import *


def solve(challenge_data: list, solve_strategy: int = 1):
    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = challenge_data
    
    if solve_strategy == 0:
        # Dumb brute force solution
        # starts with the first order and uses only one drone
        tick = 0
        order_index = 0
        orders = list(orders_dict.values())
        
        drone = Drone(list(warehouses_dict.keys())[0], max_load, products_weight)
        
        while tick < deadline and order_index < len(orders_dict):
            order = orders[order_index]
            product_type = order.items[0]
            # for product_type in order.items:
            drone.load({product_type: 1})
            print(f"Loaded product {product_type} at tick {tick}")
            # drone.deliver(order, product_type, 1)
            # drone.tick()
            # tick += 1
        
        
    
    
    if solve_strategy == 1:
        # sort orders by the sum of the distances between the warehouse and the orders for each product type 
        # (the order with the smallest sum is processed first)
        def difficulty_score(order):
            weight_sum = sum(products_weight[i] for i in order.items)
            print(weight_sum)
        
        
        orders = list(orders_dict.values())
        orders_and_scores = [(order, difficulty_score(order)) for order in orders]
        
        # TODO: UNFINISHED
    
    
    
    
    
    
    # TODO: implement other strategies by adding elif blocks
