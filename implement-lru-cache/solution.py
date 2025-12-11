```python
import collections

# Problem Description:
# Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
#
# Implement the LRUCache class:
#
# LRUCache(int capacity) initializes the LRU cache with the given positive integer capacity.
# int get(int key) returns the value of the key if the key exists, otherwise returns -1.
# void put(int key, int value) updates the value of the key if the key exists.
# Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity
# from this operation, evict the least recently used key.
#
# The functions get and put must each run in O(1) average time complexity.

# Node class for the Doubly Linked List
class Node:
    """
    Represents a node in the doubly linked list.
    Each node stores a key-value pair and pointers to the previous and next nodes.
    """
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    Implements an LRU Cache using a combination of a hash map (dictionary)
    and a doubly linked list.
    - The hash map allows O(1) access to nodes by key.
    - The doubly linked list maintains the order of usage (most recently used at the head,
      least recently used at the tail) and allows O(1) operations for moving nodes
      and removing the LRU node.
    """

    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.
        """
        self.capacity = capacity
        self.cache = {}  # Dictionary to store key -> Node mapping
        
        # Dummy head and tail nodes to simplify edge cases (e.g., empty list, single node)
        # The most recently used items are near the head.
        # The least recently used items are near the tail.
        self.head = Node(0, 0) # Dummy head node
        self.tail = Node(0, 0) # Dummy tail node
        
        # Link head and tail initially
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- Helper methods for Doubly Linked List operations ---

    def _add_node(self, node: Node):
        """
        Adds a new node right after the head. This makes it the most recently used.
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        """
        Removes a given node from its current position in the linked list.
        """
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node):
        """
        Removes a node from its current position and moves it to the head
        (making it the most recently used).
        """
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """
        Removes and returns the least recently used node (the one just before the dummy tail).
        """
        # The LRU node is always the one just before the dummy tail
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    def get(self, key: int) -> int:
        """
        Retrieves the value for a given key.
        If the key exists, its corresponding node is moved to the front of the list
        (marking it as recently used) and its value is returned.
        Otherwise, -1 is returned.

        Time Complexity: O(1)
            - Dictionary lookup is O(1) on average.
            - Linked list `_move_to_head` involves constant number of pointer manipulations (O(1)).
        """
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._move_to_head(node) # Mark as most recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates a key-value pair in the cache.
        If the key already exists:
            Its value is updated, and its node is moved to the front (most recently used).
        If the key does not exist:
            A new node is created, added to the cache, and placed at the front of the list.
            If the cache size now exceeds its capacity, the least recently used item (at the tail)
            is evicted from both the linked list and the dictionary.

        Time Complexity: O(1)
            - Dictionary lookup/insert/delete is O(1) on average.
            - Linked list operations (`_add_node`, `_move_to_head`, `_pop_tail`)
              involve constant number of pointer manipulations (O(1)).
        """
        if key in self.cache:
            # Key already exists: update value and move to head
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Key does not exist: create new node
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)
            
            # Check if cache capacity is exceeded
            if len(self.cache) > self.capacity:
                # Evict the least recently used item (from the tail)
                lru_node = self._pop_tail()
                del self.cache[lru_node.key]

# --- Complexity Analysis ---
#
# Time Complexity:
# - __init__: O(1) - Initializes instance variables and dummy nodes.
# - get(key): O(1) - Dictionary lookup is average O(1), and all linked list operations
#   (_remove_node, _add_node, _move_to_head) involve a constant number of pointer updates,
#   making them O(1).
# - put(key, value): O(1) - Similar to get, dictionary operations and linked list operations
#   are all O(1) on average.
#
# Space Complexity:
# - O(capacity) - In the worst case, the cache stores `capacity` key-value pairs.
#   Each key-value pair is stored once in the hash map and once as a Node object in the
#   doubly linked list.

# --- Test Cases ---

if __name__ == "__main__":
    print("--- Test Case 1: Basic Operations and Eviction ---")
    lru_cache = LRUCache(2)
    lru_cache.put(1, 1)  # cache is {1=1}
    lru_cache.put(2, 2)  # cache is {1=1, 2=2}
    print(f"get(1): {lru_cache.get(1)}") # returns 1 (1 is now MRU)
                                        # cache state: {2=2, 1=1} (LRU->MRU)
    lru_cache.put(3, 3)  # evicts key 2 (LRU), cache is {1=1, 3=3}
    print(f"get(2): {lru_cache.get(2)}") # returns -1 (key 2 not found)
    lru_cache.put(4, 4)  # evicts key 1 (LRU), cache is {3=3, 4=4}
    print(f"get(1): {lru_cache.get(1)}") # returns -1 (key 1 not found)
    print(f"get(3): {lru_cache.get(3)}") # returns 3 (3 is now MRU)
                                        # cache state: {4=4, 3=3}
    print(f"get(4): {lru_cache.get(4)}") # returns 4 (4 is now MRU)
                                        # cache state: {3=3, 4=4}

    print("\n--- Test Case 2: Update Existing Key ---")
    lru_cache2 = LRUCache(2)
    lru_cache2.put(1, 10) # cache is {1=10}
    lru_cache2.put(2, 20) # cache is {1=10, 2=20}
    print(f"get(1): {lru_cache2.get(1)}") # returns 10 (1 is MRU)
                                         # cache state: {2=20, 1=10}
    lru_cache2.put(1, 15) # update key 1, value is 15, 1 is MRU
                         # cache state: {2=20, 1=15}
    print(f"get(1): {lru_cache2.get(1)}") # returns 15 (1 is MRU)
    print(f"get(2): {lru_cache2.get(2)}") # returns 20 (2 is MRU)
                                         # cache state: {1=15, 2=20}
    lru_cache2.put(3, 30) # evicts key 1 (LRU), cache is {2=20, 3=30}
    print(f"get(1): {lru_cache2.get(1)}") # returns -1

    print("\n--- Test Case 3: Capacity 1 ---")
    lru_cache3 = LRUCache(1)
    lru_cache3.put(1, 100) # cache is {1=100}
    print(f"get(1): {lru_cache3.get(1)}") # returns 100
    lru_cache3.put(2, 200) # evicts key 1, cache is {2=200}
    print(f"get(1): {lru_cache3.get(1)}") # returns -1
    print(f"get(2): {lru_cache3.get(2)}") # returns 200

    print("\n--- Test Case 4: Operations resulting in same cache content ---")
    lru_cache4 = LRUCache(3)
    lru_cache4.put(1, 1) # {1:1}
    lru_cache4.put(2, 2) # {1:1, 2:2}
    lru_cache4.put(3, 3) # {1:1, 2:2, 3:3}
    print(f"get(1): {lru_cache4.get(1)}") # {2:2, 3:3, 1:1}
    print(f"get(2): {lru_cache4.get(2)}") # {3:3, 1:1, 2:2}
    lru_cache4.put(4, 4) # evicts 3. {1:1, 2:2, 4:4}
    print(f"get(3): {lru_cache4.get(3)}") # -1
    print(f"get(4): {lru_cache4.get(4)}") # 4. {1:1, 2:2, 4:4} (4 MRU)
    print(f"get(1): {lru_cache4.get(1)}") # 1. {2:2, 4:4, 1:1} (1 MRU)
```