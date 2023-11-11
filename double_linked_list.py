

class Node:

    def __init__(self, left: Node | None, valeur: int | None, right: Node | None):
        self.left: Node | None = left
        self.valeur: int | None = valeur
        self.right: Node | None = right


class DoubleLinkedList:
    
    def __init__(self, value) -> DoubleLinkedList:

        head: Cell = Cell(None, value, None)
        self.head = head
        self.length = 1
    
    def add_right(self, node: Node, value: int):
        new_node : Node = Node(node, value, node.right)
        node.right.left = new_node
        node.right = new_node
        self.taille += 1

    def add_left(self, node: Node, value: int):
        new_node : Node = Node(node.left, value, node)
        node.left.right = new_node
        node.left = new_node
        self.taille += 1
    
    def find_value(value: int):
        node = self.head
        while node.value < value and node.right is not None:
            node = node.right
        
        return node
