from __future__ import annotations


class Itemdict(dict):

    def add(self, dict_to_add: Itemdict):
        for key in dict_to_add.keys():
            if key in self.keys():
                self[key] += dict_to_add[key]
            else:
                self[key] = dict_to_add[key]

    def subtract(self, dict_to_sub: Itemdict):
        for key in dict_to_sub.keys():
            if key not in self.keys():
                raise Exception("1+ items are not available in stock")
            self[key] -= dict_to_sub[key]
            if self[key] < 0:
                raise Exception("1+ items are not available in stock")
