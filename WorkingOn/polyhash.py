#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

from classes import *
from polyparser import parse_challenge
from polysolver import solve, score_solution, save_solution
import visualizer
import mesures_temps

if __name__ == "__main__":
    debug = True

    if debug:
        args = type("Args", (object,), {"challenge": "challenges/b_busy_day.in", "output": None})
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

    challenge_data = parse_challenge(args.challenge)
    # challenge_data = (rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict)

    visualizer.simple_summary(*challenge_data)

    solution = solve(challenge_data, solve_strategy=0)
    print(solution)

    if args.output is not None:
        # Sauvegarder le fichier généré
        save_solution(args.output, solution)
        print(f"Solution saved in {args.output}")
    print(f"Score: {score_solution(solution)}")

# use : python polyhash.py challenges\a_example.in output\out.txt
