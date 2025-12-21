The "K-th Smallest Element in a Dynamically Updating Range" problem requires finding the K-th smallest element within a specified range `[L, R]` of an array, where the elements of the array can also be updated.

This is a challenging problem in competitive programming and typically solved using advanced data structures. A common and efficient approach is a **Segment Tree where each node stores a Fenwick Tree (Binary Indexed Tree) over compressed values**.

### Problem Description

We are given an initial array of `N` integers. We need to support two types of operations:
1.  **`query(L, R, K)`**: Find the K-th smallest element (1-indexed) in the subarray `nums[L...R]`.
2.  **`update(index, new_value)`**: Change the value at `nums[index]` to `new_value`.

The indices `L`, `R`, and `index` are 0-based.

### Approach: Segment Tree of Fenwick Trees with Coordinate Compression

1.  **Coordinate Compression**: Since the values in the array can be large (e.g., up to 10^9), directly using them as indices for a Fenwick Tree is infeasible. We collect all distinct values that can ever appear in the array (initial values + all possible update values) and map them to a smaller range of ranks (e.g., `0` to `M-1`, where `M` is the number of distinct values). This reduces the effective range of values, allowing Fenwick Trees to be built over these ranks.
    *   **Limitation**: For this to work in an "online" fashion (where `update` values are arbitrary and unknown beforehand), all possible values must be added to the compression set before building the segment tree. If truly arbitrary new values can appear during updates, dynamic coordinate compression (which involves rebuilding parts of the tree) is too slow, and a different data structure like a Segment Tree of Balanced BSTs or a Wavelet Tree would be required. This solution assumes values are either from the initial set or added as `candidate` values.

2.  **Segment Tree Structure**:
    *   The primary Segment Tree is built over the **indices** of the original array `nums` (from `0` to `N-1`).
    *   Each node in this Segment Tree represents a range of indices `[start_idx, end_idx]` in the `nums` array.
    *   Crucially, each node in the Segment Tree does *not* store a simple value or sum. Instead, it stores a **Fenwick Tree (BIT)**. This internal Fenwick Tree operates on the **compressed ranks** of the values. The BIT at a Segment Tree node `v` stores the frequency counts of *value ranks* that are present in `nums[range_of_v]`.

3.  **Operations**:

    *   **Build (`__init__` of `SegmentTree`)**:
        *   The Segment Tree is initialized with `4*N` empty Fenwick Trees.
        *   Then, for each element `nums[i]` in the initial array, we effectively perform an "add" operation: the rank of `nums[i]` is added to the Fenwick Trees of all Segment Tree nodes on the path from the root to the leaf representing index `i`.
        *   Time Complexity: `O(N * log N * log M)`, where `N` is array size and `M` is number of distinct ranks.

    *   **Update (`update`)**:
        *   When `nums[index]` changes from `old_value` to `new_value`:
        *   Convert `old_value` and `new_value` to `old_rank` and `new_rank` using coordinate compression maps.
        *   Traverse the Segment Tree from the root down to the leaf representing `index`.
        *   At each Segment Tree node along this path, update its internal Fenwick Tree: decrement the count for `old_rank` and increment the count for `new_rank`.
        *   Time Complexity: `O(log N * log M)` (`log N` for segment tree path, `log M` for each Fenwick Tree update).

    *   **Query K-th Smallest (`query_kth_smallest`)**:
        *   To find the K-th smallest element in `nums[L...R]`, we perform a binary search on the `rank` domain `[0, M-1]`.
        *   For a candidate `mid_rank`, we need to efficiently count how many elements in `nums[L...R]` have ranks less than or equal to `mid_rank`.
        *   This `count_le(mid_rank, L, R)` function works by traversing the Segment Tree. For each Segment Tree node whose range is *fully contained* within `[L, R]`, we query its internal Fenwick Tree for the prefix sum up to `mid_rank`. Summing these results gives the total count.
        *   Time Complexity for `count_le`: `O(log N * log M)` (`log N` for segment tree traversal, `log M` for each Fenwick Tree prefix sum query).
        *   The binary search adds another `log M` factor.
        *   Total Query Time: `O(log M * log N * log M) = O(log^2 M * log N)`.

### Complexity Analysis

*   **`N`**: Size of the initial array.
*   **`Q`**: Number of update/query operations.
*   **`V`**: Total number of distinct values across initial array and all updates (after `add_value_candidate` calls). `V <= N + Q`.
*   **`M`**: Number of distinct compressed ranks. `M = V`.

*   **Time Complexity**:
    *   **Coordinate Compression (`add_value_candidate`, `finalize_compression_and_build`):** `O(V log V)`.
    *   **Segment Tree Build (`finalize_compression_and_build`):** `O(N log N log M)`.
    *   **Update (`update`):** `O(log N log M)`.
    *   **Query (`query`):** `O(log^2 M log N)`.

*   **Space Complexity**:
    *   `current_nums`: `O(N)`.
    *   `val_to_rank`, `rank_to_val`: `O(M)`.
    *   Segment Tree `self.tree`: `O(N)` nodes, each storing a Fenwick Tree of size `M`.
        *   Total Space: `O(N * M)`.

**Important Note on Space Complexity (O(N*M))**:
For `N, Q` up to `10^5`, if `M` is also in the order of `N` (e.g., if all initial values are distinct), then `O(N*M)` space becomes `O(N^2)`, which is `(10^5)^2 = 10^{10}`. This is **prohibitive** for typical memory limits (e.g., 256MB).
This approach is practical only if `M` is relatively small (e.g., a small constant, or `log N`, `sqrt N`). For large `N` and `M ~ N`, a **Persistent Segment Tree** (with `O((N+Q) log M)` space) or a **Wavelet Tree** (with `O(N log MAX_VAL)` space) is required for optimal space. The current solution provides a direct implementation of the Segment Tree of Fenwick Trees as it's a common (though sometimes memory-limited) approach.

### Python Code

```python
import collections

# --- Fenwick Tree (BIT) Implementation ---
class FenwickTree:
    """
    A Fenwick Tree (Binary Indexed Tree) for point updates and prefix sum queries.
    Uses 1-based indexing internally for Fenwick Tree array logic.
    User input for index (e.g., during update/query) should be 0-based,
    and will be converted to 1-based internally.
    """
    def __init__(self, size):
        self.size = size # The maximum value rank + 1
        self.tree = [0] * (size + 1) # Internal tree array is 1-indexed

    def update(self, index_0_based, delta):
        """
        Adds `delta` to the element at `index_0_based`.
        index_0_based: 0-based index of the element to update.
        delta: Value to add.
        Time: O(log self.size)
        """
        index_1_based = index_0_based + 1 # Convert to 1-based
        while index_1_based <= self.size:
            self.tree[index_1_based] += delta
            index_1_based += index_1_based & (-index_1_based)

    def query(self, index_0_based):
        """
        Returns the prefix sum from 0 up to `index_0_based` (inclusive).
        index_0_based: 0-based index defining the end of the prefix sum range.
        Time: O(log self.size)
        """
        index_1_based = index_0_based + 1 # Convert to 1-based
        s = 0
        while index_1_based > 0:
            s += self.tree[index_1_based]
            index_1_based -= index_1_based & (-index_1_based)
        return s

# --- Segment Tree of Fenwick Trees Implementation ---
class SegmentTree:
    """
    A Segment Tree where each node stores a Fenwick Tree.
    Used for range K-th smallest queries with point updates.
    """
    def __init__(self, initial_nums, val_to_rank_map, M):
        """
        Initializes the Segment Tree.
        initial_nums: The initial array of numbers.
        val_to_rank_map: A dictionary mapping original values to their compressed ranks.
        M: The total number of distinct compressed ranks (size for Fenwick Trees).
        """
        self.n = len(initial_nums)
        self.val_to_rank = val_to_rank_map
        self.M = M # Size of the value domain for Fenwick Trees

        # The segment tree array, each element is a FenwickTree object
        # We need 4*N nodes for a segment tree
        self.tree = [None] * (4 * self.n) 
        
        # Initialize each node with an empty Fenwick Tree
        for i in range(len(self.tree)):
            self.tree[i] = FenwickTree(M)
        
        # Build the segment tree by effectively 'updating' each initial element
        # This propagates the initial values up to the Fenwick Trees of ancestor nodes.
        # Time: O(N * log N * log M)
        for i in range(self.n):
            rank = self.val_to_rank[initial_nums[i]]
            self._update_recursive(1, 0, self.n - 1, i, rank, 1)

    def _update_recursive(self, node_idx, start_idx, end_idx, target_idx, rank, delta):
        """
        Recursively updates the Fenwick Trees in the path from root to leaf `target_idx`.
        node_idx: Current segment tree node index.
        start_idx, end_idx: Range covered by the current segment tree node.
        target_idx: The index in the original array that is being updated.
        rank: The compressed rank of the value being updated.
        delta: +1 for addition, -1 for removal.
        Time: O(log N * log M) (log N for path, log M for each BIT update)
        """
        # Update the Fenwick Tree at the current segment tree node
        self.tree[node_idx].update(rank, delta)

        if start_idx == end_idx:
            return

        mid_idx = (start_idx + end_idx) // 2
        if target_idx <= mid_idx:
            self._update_recursive(2 * node_idx, start_idx, mid_idx, target_idx, rank, delta)
        else:
            self._update_recursive(2 * node_idx + 1, mid_idx + 1, end_idx, target_idx, rank, delta)

    def update(self, index, old_rank, new_rank):
        """
        Updates the value at a specific `index` in the original array.
        This function handles the ranks; the wrapper `DynamicKthSmallest` handles value to rank conversion.
        index: 0-based index in the original array to update.
        old_rank: The rank of the old value at `index`.
        new_rank: The rank of the new value to place at `index`.
        Time: O(log N * log M)
        """
        self._update_recursive(1, 0, self.n - 1, index, old_rank, -1) # Remove old value
        self._update_recursive(1, 0, self.n - 1, index, new_rank, 1)  # Add new value

    def _query_count_le(self, node_idx, seg_start, seg_end, query_L, query_R, target_rank):
        """
        Helper for `query_kth_smallest`: counts elements with rank <= `target_rank` in range [query_L, query_R].
        node_idx: Current segment tree node index.
        seg_start, seg_end: Range covered by the current segment tree node.
        query_L, query_R: The query range for the original array.
        target_rank: The maximum rank to count.
        Time: O(log N * log M) (log N for segment tree traversal, log M for each BIT query)
        """
        # No overlap
        if query_R < seg_start or query_L > seg_end:
            return 0
        
        # Full overlap
        if query_L <= seg_start and seg_end <= query_R:
            return self.tree[node_idx].query(target_rank)
        
        # Partial overlap: recurse
        mid_idx = (seg_start + seg_end) // 2
        left_count = self._query_count_le(2 * node_idx, seg_start, mid_idx, query_L, query_R, target_rank)
        right_count = self._query_count_le(2 * node_idx + 1, mid_idx + 1, seg_end, query_L, query_R, target_rank)
        return left_count + right_count
    
    def query_kth_smallest(self, query_L, query_R, K, rank_to_val_map):
        """
        Finds the K-th smallest element in the range [query_L, query_R].
        query_L, query_R: 0-based indices defining the query range.
        K: The 1-based order statistic to find (e.g., K=1 for smallest).
        rank_to_val_map: A list/array mapping ranks back to original values.
        Time: O(log M * log N * log M) = O(log^2 M * log N)
        """
        # Binary search for the rank of the K-th smallest element
        low_rank = 0
        high_rank = self.M - 1 # Ranks are 0 to M-1
        ans_rank = -1

        while low_rank <= high_rank:
            mid_rank = low_rank + (high_rank - low_rank) // 2
            # Count elements <= mid_rank in the query range
            count = self._query_count_le(1, 0, self.n - 1, query_L, query_R, mid_rank)

            if count >= K:
                ans_rank = mid_rank
                high_rank = mid_rank - 1 # Try to find a smaller value
            else:
                low_rank = mid_rank + 1 # Need a larger value
        
        # If ans_rank is -1, it means K was out of bounds or no elements,
        # but K is validated in the wrapper, so this shouldn't happen for valid inputs.
        return rank_to_val_map[ans_rank]

# --- Wrapper Class for Dynamic K-th Smallest Problem ---
class DynamicKthSmallest:
    """
    Manages the overall problem, including coordinate compression and
    interacting with the Segment Tree.
    """
    def __init__(self, initial_nums):
        self.n = len(initial_nums)
        self._initial_elements = list(initial_nums) # Snapshot for tree building
        self.current_nums = list(initial_nums)      # Mutable array reflecting updates

        self._all_possible_values = set(initial_nums) # Collects all values for compression
        
        self.val_to_rank = {}
        self.rank_to_val = [] # Inverse map for coordinate compression
        self.M = 0            # Number of distinct ranks (size of value domain)
        self.seg_tree = None

    def add_value_candidate(self, val):
        """
        Adds a value to the set of values that will be compressed.
        Useful for update values that are not in the initial array.
        This must be called BEFORE `finalize_compression_and_build`.
        """
        self._all_possible_values.add(val)

    def finalize_compression_and_build(self):
        """
        Performs coordinate compression based on all collected values
        and then builds the Segment Tree.
        Must be called once after all initial and potential update values
        have been registered.
        """
        if not self._all_possible_values:
            # Handle empty initial array or no candidates added.
            if self.n > 0:
                raise ValueError("No values available for compression; initial_nums might be empty, or no candidates added.")
            # If n == 0, then the tree will remain None, which is fine.
            self.seg_tree = None
            return

        sorted_distinct_values = sorted(list(self._all_possible_values))
        self.rank_to_val = sorted_distinct_values
        self.val_to_rank = {val: i for i, val in enumerate(sorted_distinct_values)}
        self.M = len(sorted_distinct_values)

        if self.n == 0: # If the initial array was empty, no segment tree needed
            self.seg_tree = None
            return

        self.seg_tree = SegmentTree(self._initial_elements, self.val_to_rank, self.M)
        # Link the mutable current_nums array for the SegmentTree to reference for old values
        self.seg_tree.current_nums = self.current_nums 

    def update(self, index, new_value):
        """
        Updates the element at `index` to `new_value`.
        index: 0-based index.
        new_value: The new value for the element.
        Time: O(log N * log M)
        """
        if self.seg_tree is None:
            if self.n == 0: return # Empty array, no update possible
            raise RuntimeError("Segment tree not built. Call finalize_compression_and_build first.")

        if not (0 <= index < self.n):
            raise IndexError(f"Index {index} out of bounds for array of size {self.n}")
        
        if new_value not in self.val_to_rank:
            raise ValueError(f"New value {new_value} not found in preprocessed values. "
                             f"Add it as a candidate via `add_value_candidate` before "
                             f"`finalize_compression_and_build` to handle it.")
        
        old_value = self.current_nums[index]
        old_rank = self.val_to_rank[old_value]
        new_rank = self.val_to_rank[new_value]

        self.current_nums[index] = new_value # Update the conceptual array
        self.seg_tree.update(index, old_rank, new_rank)
    
    def query(self, L, R, K):
        """
        Finds the K-th smallest element in the range [L, R].
        L, R: 0-based start and end indices of the range.
        K: 1-based K-th smallest (e.g., K=1 for the smallest).
        Time: O(log^2 M * log N)
        """
        if self.seg_tree is None:
            if self.n == 0: return -1 # No elements to query from
            raise RuntimeError("Segment tree not built. Call finalize_compression_and_build first.")

        if not (0 <= L <= R < self.n):
            raise IndexError(f"Query range [{L}, {R}] out of bounds for array of size {self.n}")
        if not (1 <= K <= (R - L + 1)):
            raise ValueError(f"K={K} is out of bounds for the given range [{L}, {R}] (size {R-L+1})")
        
        return self.seg_tree.query_kth_smallest(L, R, K, self.rank_to_val)


# --- Test Cases ---
if __name__ == "__main__":
    # Test Case 1: Basic operations
    initial_array1 = [10, 20, 30, 40, 50]
    solver1 = DynamicKthSmallest(initial_array1)

    # Add candidate update values. In a real scenario, you'd collect all values
    # from initial_nums and all planned updates before calling finalize.
    solver1.add_value_candidate(15)
    solver1.add_value_candidate(5)
    solver1.add_value_candidate(30) # Already present but good to list
    solver1.add_value_candidate(100) # Future possible value

    solver1.finalize_compression_and_build()

    print("Test Case 1:")
    print(f"Initial array: {initial_array1}")

    # Query 1: K=3rd smallest in [10, 20, 30, 40, 50] (indices 0 to 4)
    result = solver1.query(0, 4, 3)
    print(f"Query(0, 4, 3) -> Expected: 30, Got: {result}")
    assert result == 30

    # Update 1: Change element at index 1 (20) to 15
    solver1.update(1, 15)
    print(f"Array after update(1, 15): {solver1.current_nums}") # [10, 15, 30, 40, 50]

    # Query 2: K=2nd smallest in [10, 15, 30] (indices 0 to 2)
    result = solver1.query(0, 2, 2)
    print(f"Query(0, 2, 2) -> Expected: 15, Got: {result}")
    assert result == 15

    # Update 2: Change element at index 3 (40) to 5
    solver1.update(3, 5)
    print(f"Array after update(3, 5): {solver1.current_nums}") # [10, 15, 30, 5, 50]

    # Query 3: K=1st smallest in [10, 15, 30, 5, 50] (indices 0 to 4)
    result = solver1.query(0, 4, 1)
    print(f"Query(0, 4, 1) -> Expected: 5, Got: {result}")
    assert result == 5

    # Query 4: K=5th smallest in [10, 15, 30, 5, 50] (indices 0 to 4)
    result = solver1.query(0, 4, 5)
    print(f"Query(0, 4, 5) -> Expected: 50, Got: {result}")
    assert result == 50

    # Query 5: K=3rd smallest in [15, 30, 5] (indices 1 to 3)
    result = solver1.query(1, 3, 3)
    print(f"Query(1, 3, 3) -> Expected: 30, Got: {result}")
    assert result == 30


    # Test Case 2: Edge cases - single element, identical elements
    print("\nTest Case 2:")
    initial_array2 = [7]
    solver2 = DynamicKthSmallest(initial_array2)
    solver2.add_value_candidate(10) # For potential update
    solver2.finalize_compression_and_build()
    
    result = solver2.query(0, 0, 1)
    print(f"Query(0, 0, 1) -> Expected: 7, Got: {result}")
    assert result == 7

    solver2.update(0, 10)
    result = solver2.query(0, 0, 1)
    print(f"Array after update(0, 10): {solver2.current_nums}")
    print(f"Query(0, 0, 1) -> Expected: 10, Got: {result}")
    assert result == 10

    print("\nTest Case 3: All identical elements")
    initial_array3 = [5, 5, 5, 5]
    solver3 = DynamicKthSmallest(initial_array3)
    solver3.add_value_candidate(10)
    solver3.finalize_compression_and_build()

    result = solver3.query(0, 3, 1)
    print(f"Query(0, 3, 1) -> Expected: 5, Got: {result}")
    assert result == 5
    result = solver3.query(0, 3, 4)
    print(f"Query(0, 3, 4) -> Expected: 5, Got: {result}")
    assert result == 5
    
    solver3.update(1, 10)
    print(f"Array after update(1, 10): {solver3.current_nums}") # [5, 10, 5, 5]
    result = solver3.query(0, 3, 1)
    print(f"Query(0, 3, 1) -> Expected: 5, Got: {result}")
    assert result == 5
    result = solver3.query(0, 3, 4)
    print(f"Query(0, 3, 4) -> Expected: 10, Got: {result}")
    assert result == 10

    print("\nTest Case 4: Empty array")
    initial_array4 = []
    solver4 = DynamicKthSmallest(initial_array4)
    solver4.finalize_compression_and_build()
    
    try:
        solver4.query(0, 0, 1)
    except RuntimeError as e:
        print(f"Expected error for empty array query: {e}")
    except IndexError as e:
        print(f"Expected error for empty array query: {e}") # Depends on error path
    
    # Empty array should return -1 if K is invalid, or raise error.
    # Current implementation for empty array: if N==0, seg_tree is None.
    # query/update on None seg_tree raises RuntimeError.
    # You could adjust query to return a default value like -1 for N=0.
    assert solver4.query(0,0,1) == -1 # Assuming `query` can handle empty range and returns -1

    # Test Case 5: Values not in compression set (expected error)
    print("\nTest Case 5:")
    initial_array5 = [1, 2, 3]
    solver5 = DynamicKthSmallest(initial_array5)
    solver5.finalize_compression_and_build() # Only 1, 2, 3 are compressed

    try:
        solver5.update(0, 99) # 99 was not added as a candidate
    except ValueError as e:
        print(f"Caught expected error for uncompressed value update: {e}")
    assert solver5.current_nums == [1, 2, 3] # Array should not have changed

    print("\nAll test cases passed!")

```