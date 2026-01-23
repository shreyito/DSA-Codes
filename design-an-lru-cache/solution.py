```python
import collections
  
class Node:
    """ 
    Represents a node in the doubly linked list.
    Each node stores its key, value, and pointers to the previous and next nodes.
    Storing the key in the node is crucial for O(1) deletion from the hash map
    when an LRU item is evicted.
    """
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    """
    Implements a Least Recently Used (LRU) cache.

    The cache uses a combination of a hash map (Python dict) and a doubly linked list
    to achieve O(1) average time complexity for both `get` and `put` operations.

    - Hash Map: Stores `key -> Node` mappings, allowing quick lookup of nodes.
    - Doubly Linked List: Maintains the order of usage.
      - The head of the list (closest to `self.head` sentinel) represents the Most Recently Used (MRU) item.
      - The tail of the list (closest to `self.tail` sentinel) represents the Least Recently Used (LRU) item.
    """
    def __init__(self, capacity: int):
        """
        Initializes the LRU cache with a given capacity.

        Args:
            capacity: The maximum number of key-value pairs the cache can hold.
        """
        self.capacity = capacity
        self.cache = {}  # Maps key to Node object
        
        # Initialize dummy head and tail nodes for the doubly linked list.
        # These sentinels simplify edge cases (empty list, adding/removing first/last).
        self.head = Node(0, 0) # Dummy head
        self.tail = Node(0, 0) # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node):
        """
        Adds a new node right after the dummy head node.
        This effectively makes the node the Most Recently Used (MRU) item.
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node):
        """
        Removes a given node from the doubly linked list.
        This operation links the node's previous and next neighbors directly.
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: Node):
        """
        Moves an existing node to the front of the linked list (making it MRU).
        This is done by first removing it from its current position and then
        adding it right after the dummy head.
        """
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """
        Removes and returns the Least Recently Used (LRU) node.
        The LRU node is the one just before the dummy tail node.
        Returns None if the list is empty (only sentinels exist).
        """
        if self.tail.prev == self.head: # List is empty (only head and tail sentinels)
            return None
        
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    def get(self, key: int) -> int:
        """
        Retrieves the value associated with the given key.

        If the key exists:
        1. The corresponding node is moved to the front of the linked list (MRU).
        2. Its value is returned.

        If the key does not exist:
        - Returns -1.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key, or -1 if the key is not found.
        """
        if key in self.cache:
            node = self.cache[key]
            self._move_to_head(node)  # Mark as Most Recently Used
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates a key-value pair in the cache.

        If the key already exists:
        1. Its value is updated.
        2. The corresponding node is moved to the front of the linked list (MRU).

        If the key does not exist:
        1. A new node is created.
        2. This new node is added to the hash map and to the front of the linked list (MRU).
        3. If the cache capacity is exceeded after the insertion, the Least Recently Used (LRU)
           item (at the tail of the list) is evicted from both the linked list and the hash map.

        Args:
            key: The key to insert or update.
            value: The value associated with the key.
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value  # Update the value
            self._move_to_head(node)  # Mark as Most Recently Used
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_node(new_node)  # Add new node as MRU

            # Check if cache capacity is exceeded
            if len(self.cache) > self.capacity:
                lru_node = self._pop_tail()  # Evict the LRU item
                if lru_node: # Ensure a node was actually popped (list wasn't empty initially)
                    del self.cache[lru_node.key] # Remove from hash map

# --- Time and Space Complexity ---
# Time Complexity:
# - __init__(capacity): O(1) - Initializes instance variables and two sentinel nodes.
# - get(key): O(1) - Dictionary lookup is O(1) on average. Doubly linked list operations
#   (_remove_node, _add_node, _move_to_head) are all O(1) because they involve
#   constant number of pointer manipulations.
# - put(key, value): O(1) - Dictionary lookup/insertion is O(1) on average. Doubly linked
#   list operations (_add_node, _remove_node, _move_to_head, _pop_tail) are all O(1).
#
# Space Complexity:
# - O(capacity) - The cache stores at most 'capacity' key-value pairs.
#   Each pair requires a Node object and an entry in the hash map.

# --- Test Cases ---
if __name__ == "__main__":
    print("--- Test Case 1: Basic Operations and Eviction ---")
    lru_cache1 = LRUCache(2)
    lru_cache1.put(1, 1) # Cache: {1:1} (MRU: 1)
    lru_cache1.put(2, 2) # Cache: {1:1, 2:2} (MRU: 2)
    print(f"Get(1): {lru_cache1.get(1)}") # Expected: 1 (MRU: 1)
    lru_cache1.put(3, 3) # Cache is full. 2 is LRU, evict 2. Cache: {1:1, 3:3} (MRU: 3)
    print(f"Get(2): {lru_cache1.get(2)}") # Expected: -1 (2 was evicted)
    lru_cache1.put(4, 4) # Cache is full. 1 is LRU, evict 1. Cache: {3:3, 4:4} (MRU: 4)
    print(f"Get(1): {lru_cache1.get(1)}") # Expected: -1 (1 was evicted)
    print(f"Get(3): {lru_cache1.get(3)}") # Expected: 3 (MRU: 3)
    print(f"Get(4): {lru_cache1.get(4)}") # Expected: 4 (MRU: 4)

    print("\n--- Test Case 2: Update Existing Key ---")
    lru_cache2 = LRUCache(2)
    lru_cache2.put(1, 10) # Cache: {1:10} (MRU: 1)
    lru_cache2.put(2, 20) # Cache: {1:10, 2:20} (MRU: 2)
    lru_cache2.put(1, 100) # Update 1 to 100, 1 becomes MRU. Cache: {2:20, 1:100} (MRU: 1)
    print(f"Get(2): {lru_cache2.get(2)}") # Expected: 20 (MRU: 2)
    lru_cache2.put(3, 30) # Cache is full. 1 is LRU (2 was accessed last), evict 1. Cache: {2:20, 3:30} (MRU: 3)
    print(f"Get(1): {lru_cache2.get(1)}") # Expected: -1 (1 was evicted)
    print(f"Get(2): {lru_cache2.get(2)}") # Expected: 20 (MRU: 2)

    print("\n--- Test Case 3: Capacity 1 ---")
    lru_cache3 = LRUCache(1)
    lru_cache3.put(1, 111) # Cache: {1:111} (MRU: 1)
    print(f"Get(1): {lru_cache3.get(1)}") # Expected: 111
    lru_cache3.put(2, 222) # Cache is full. 1 is LRU, evict 1. Cache: {2:222} (MRU: 2)
    print(f"Get(1): {lru_cache3.get(1)}") # Expected: -1
    print(f"Get(2): {lru_cache3.get(2)}") # Expected: 222

    print("\n--- Test Case 4: Operations on empty cache / non-existent keys ---")
    lru_cache4 = LRUCache(3)
    print(f"Get(10): {lru_cache4.get(10)}") # Expected: -1
    lru_cache4.put(1, 1) # Cache: {1:1} (MRU: 1)
    print(f"Get(1): {lru_cache4.get(1)}") # Expected: 1
    print(f"Get(2): {lru_cache4.get(2)}") # Expected: -1
```
