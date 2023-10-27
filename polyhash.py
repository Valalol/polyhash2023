#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

from polyparser import parse_challenge
# from polysolver import solve, score_solution, save_solution
from visualizer import *



if __name__ == "__main__":
    debug = True
    
    if debug:
        args = type("Args", (object,), {"challenge": "challenges/d_mother_of_all_warehouses.in", "output": "output/out.txt"})
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
        parser.add_argument('challenge', type=str,
                            help='challenge definition filename',
                            metavar="challenge.txt")
        parser.add_argument('output', type=str, default=None,
                            help='output filename',
                            metavar="sortie.txt")
        args = parser.parse_args()

    rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict = parse_challenge(args.challenge)
    
    heatmap((rows, columns), warehouses_dict, orders_dict)
    
    
    
    # solution = solve()
    # if args.output is not None:
    #     # Sauvegarder le fichier généré
    #     save_solution(args.output, solution)
    #     print(f"Solution saved in {args.output}")
    # print(f"Score: {score_solution(solution)}")


# use : python polyhash.py challenges\a_example.in output\out.txt