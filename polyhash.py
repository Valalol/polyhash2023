#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

def main():
    from polyparser import parse_challenge
    from polysolver import solve, save_solution
    import visualizer
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

    # visualizer.simple_summary(*challenge_data)

    solution = solve(challenge_data, solve_strategy=3)

    if args.output is not None:
        # Sauvegarder le fichier généré
        save_solution(args.output, solution)
        print(f"Solution saved in {args.output}")


if __name__ == "__main__":
    main()

# use : python polyhash.py challenges\a_example.in output\out.txt
