# mathematiks.py
# stores mathematiks related functions
Weights: dict[int]


def dista(a: tuple[int, int], b: tuple[int, int]):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2)


def items_total_weight(items_list: dict[int]):
    total_weight:  int = 0
    for item_id, number in items_list.keys(), items_list.values():
        total_weight += Weights[item_id] * number
    return total_weight


