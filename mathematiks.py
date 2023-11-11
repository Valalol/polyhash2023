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

