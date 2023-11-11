from __future__ import annotations

def dict_add(dict_original, dict_to_add):
    for key in dict_to_add.keys():
        if key in dict_original.keys():
            dict_original[key] += dict_to_add[key]
        else:
            dict_original[key] = dict_to_add[key]
    return dict_original

def dict_subtract(dict_original, dict_to_sub):
    for key in dict_to_sub.keys():
        if key not in dict_original.keys():
            raise Exception("1+ items are not available in stock")
        dict_original[key] -= dict_to_sub[key]
        if dict_original[key] < 0:
            raise Exception("1+ items are not available in stock")
    return dict_original
