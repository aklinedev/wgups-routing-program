# This is used to represent a chain node. Each node
# will have a key, value, and a reference to the next node.

class ChainNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None