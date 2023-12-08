# mathematiks.py
# stores mathematiks related functions


def dist(a: tuple[int, int], b: tuple[int, int]):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)


def items_total_weight(item_weights: list[int], items_list: dict[int]):
    somme = 0
    for item in items_list:
        quantity = items_list[item]
        somme += item_weights[item] * quantity
    return somme





def zones_chaudes():
    tableau_warehouse = []
    tableau_commande = []

    for i in range(len(warehouse_list)):
        tableau_warehouse.append(warehouse_list[i])
    for i in range(len(order_list)):
        tableau_warehouse.append(order_list[i])
    return
