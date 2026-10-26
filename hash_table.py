from chain_node import Chain_Node

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table =  [None] * size

    # The hash function is used to map objects based
    # on there key, then MOD the size of the table. Ideally this
    # is a prime number to help even distribution.

    def custom_hash(self, key):
        hashed_key = key % self.size
        return hashed_key

    def insert(self, key, value):
        index = self.custom_hash(key)
        head_node = self.table[index]

        # Check if a node with the same key exist. If it does
        # we will update its value.

        current = head_node
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        new_chain_node = Chain_Node(key, value)
        new_chain_node.next = head_node
        self.table[index] = new_chain_node


    def get(self, key):
        index = self.custom_hash(key)
        head_node = self.table[index]

        current = head_node
        while current:
            if current.key == key:
                # Returns the value associated with the key.
                return current.value
            current = current.next

        return None

    def remove(self, key):
        index = self.custom_hash(key)
        head_node = self.table[index]
        previous = None

        current = head_node
        while current:
            if current.key == key:
                # If the node to remove is the head, we remove it
                # by assigning the head to point to head.next.
                if previous is None:
                    self.table[index] = current.next
                # Otherwise, we assign the previous node to point
                # at the current nodes next reference.
                else:
                    previous.next = current.next
                return

            previous = current
            current = current.next

    def resize(self):
        old_table = self.table

        new_size = self.size * 2
        self.size = new_size
        self.table = [None] * self.size

        for bucket in old_table:
            current = bucket
            while current:
                self.insert(current.key, current.value)
                current = current.next
                


        
        
        