#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""

from classes import *
from polyparser import parse_challenge
import mesures_temps

@mesures_temps.time_measurement
def solve(challenge_data: list, solve_strategy: int = 1):
    """
    Solves the given challenge data using the specified strategy2.
    
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
    - solve_strategy (int): An integer representing the strategy2 to use for solving the challenge data.
    
    Returns:
    - solution (str): A text containing the solution to the challenge data.
    """
    
    if solve_strategy == 1:
        import strategies.strategy_1 as strategy_1
        solution = strategy_1.solve(challenge_data)
    
    elif solve_strategy == 3:
        import strategies.strategy_3 as strategy_3
        solution = strategy_3.solve(challenge_data)
    
    return solution

def save_solution(filename: str, solution: str):
    """
    Saves the given solution to the specified file.
    
    Args:
    - filename (str): The name of the file to save the solution to.
    - solution (str): A text containing the solution to the challenge data.
    """

    import os
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as f:
        f.write(solution)
    
    return None

if __name__ == "__main__":
    pass
