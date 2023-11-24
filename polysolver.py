#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de résolution du projet Poly#.
"""

from classes import *
import strategies.strategy_0 as strategy_0
# import strategies.strategy1.strategy_1 as strategy_1
import strategy_1 as strategy_1
from polyparser import parse_challenge
#import mesures_temps

#@mesures_temps.time_measurement
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
    - solution (str): A text containing the solution to the challenge data.
    """
    
    if solve_strategy == 0:
        solution = strategy_0.solve(challenge_data)
    
    elif solve_strategy == 1:
        solution = strategy_1.solve(challenge_data)
    
    return solution

def score_solution(solution: str):
    """
    Scores the given solution.
    
    Args:
    - solution (str): A text containing the solution to the challenge data.
    
    Returns:
    - score (int): The score of the given solution.
    """
    score = 0
    
    for line in solution.split("\n"):
        pass
    
    return score

def save_solution(filename: str, solution: str):
    """
    Saves the given solution to the specified file.
    
    Args:
    - filename (str): The name of the file to save the solution to.
    - solution (str): A text containing the solution to the challenge data.
    """
    
    with open(filename, "w") as file:
        file.write(solution)
    
    return None

if __name__ == "__main__":
    challenge_data = parse_challenge("challenges/a_example.in")
    print(solve(challenge_data,1))

