#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""
from classes import *


def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    with open(filename, 'r') as f:
        data_raw = f.read()

    data = []
    for l in data_raw.split("\n"):
        data.append([int(i) for i in l.split(" ")])

    rows, columns, drone_count, deadline, max_load = data[0]
    products_weight = data[2]
    warehouse_number = data[3][0]
    index = 4

    warehouses_dict = {}
    for i in range(warehouse_number):
        x, y = data[index]
        products_info = data[index + 1]
        index += 2
        warehouse = Warehouse(coordinates=(x, y), products_info=products_info, warehouse_id=i)
        warehouses_dict[(x, y)] = warehouse

    order_number = data[index][0]
    index += 1

    orders_dict = {}
    for i in range(order_number):
        x, y = data[index]
        order_info: list[int] = data[index + 2]
        index += 3
        order = Order(coordinates=(x, y), items=order_info, order_id=i)
        orders_dict[(x, y)] = order

    return rows, columns, drone_count, deadline, max_load, products_weight, warehouses_dict, orders_dict


if __name__ == "__main__":
    parse_challenge("challenges/a_example.in")
