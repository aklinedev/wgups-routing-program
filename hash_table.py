from chain_node import ChainNode

# For my custom hash table, I chose to use chaining for handling 
# collisions ; which is why im using it to store my custom chain nodes.
class HashTable:
    def __init__(self, size):
        # The bucket count scales with the expected number of entries.
        # I intentionally use fewer buckets than entries so collisions occur
        # and the separate-chaining strategy is exercised for this coursework.
        self.size = max(10, size // 2)
        self.table =  [None] * self.size

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

        # Node with same key does not exist, so we add it to the table.
        new_chain_node = ChainNode(key, value)
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
        # Create the reference to the table before making it 
        # bigger. Then we will re-distribute the objects to the new
        # sized hash table.
        old_table = self.table

        new_size = self.size * 2
        self.size = new_size
        self.table = [None] * self.size

        for bucket in old_table:
            current = bucket
            while current:
                self.insert(current.key, current.value)
                current = current.next
                
    def __iter__(self):
        for bucket in self.table:
            current = bucket

            while current:
                # Yield is used here to allow returning multiple values rather
                # then the function ending after it returns only one value
                # so that way we can use "for x in hashtable"
                yield current.value
                current = current.next

        
        
        