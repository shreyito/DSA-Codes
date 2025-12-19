The problem asks for the minimum number of jumps to reach the end of an array, starting from the first element (index 0). We can make three types of jumps:
1.  **Jump to `i + 1`**: Move to the next index.
2.  **Jump to `i - 1`**: Move to the previous index.
3.  **Teleportation**: If `arr[i]` is a teleportation device, we can jump to any other index `j` where `arr[j]` has the *same value* as `arr[i]`.

We also have **obstacles**: `arr[i] = -1` denotes an obstacle. We cannot land on an obstacle or start a jump from one.

**Interpretation of array values:**
*   `arr[i] = -1`: This is an obstacle. No jumps can be made to or from this index.
*   `arr[i] >= 0`: This is a valid cell.
    *   From `arr[i]`, we can always try to jump to `i+1` and `i-1` (if within bounds and not an obstacle).
    *   Additionally, if `arr[i]` has the same value as `arr[j]` (where `i != j`), it acts as a "teleportation device", allowing a jump to `j`. This applies to all non-negative values, including `0`.

This problem is a classic shortest path on an unweighted graph, which is best solved using **Breadth-First Search (BFS)**.

## Algorithm Breakdown

1.  **Graph Representation (Implicit):**
    *   Each index `i` in the array `arr` represents a node in our graph.
    *   Edges exist between `i` and `i+1`, `i` and `i-1`, and `i` and `j` (if `arr[i] == arr[j]`).
    *   Obstacles (`-1`) are effectively non-existent nodes or blocked paths.

2.  **BFS Initialization:**
    *   `queue`: A `collections.deque` to store `(current_index, jumps_so_far)`. We start with `(0, 0)`.
    *   `visited`: A `set` to keep track of indices already added to the queue, preventing cycles and redundant work. Initialize with `{0}`.
    *   **Edge Cases:** If `n <= 1` (array length 0 or 1), we are already at the end, so 0 jumps. If the start (`arr[0]`) or end (`arr[n-1]`) is an obstacle, it's impossible, return -1.

3.  **Optimize Teleportation Jumps:**
    *   A naive approach for teleportation (iterating through the entire array to find matching values for each `arr[i]`) would be `O(N)` for each teleporting jump, leading to `O(N^2)` worst-case time complexity, which might be too slow for large `N`.
    *   **Preprocessing:** Create a dictionary `value_to_indices = {value: [list of indices with that value]}`. This maps each unique non-obstacle value to all indices where it appears.
    *   **Key Optimization:** When we process an index `current_idx` that has value `val`:
        1.  We retrieve all `tele_idx` from `value_to_indices[val]`.
        2.  For each `tele_idx` not yet visited, we add `(tele_idx, jumps + 1)` to the queue and mark `tele_idx` as visited.
        3.  **Crucially**, after processing all teleport links for `val`, we **remove `val` from `value_to_indices` (e.g., using `pop(val)` or `clear()`)**. This ensures that if we later encounter another `current_idx_2` with the *same value `val`*, we don't re-explore the same set of teleport links. Since BFS guarantees the shortest path, if an index `j` is reachable via `val`, it will be reached optimally the first time `val` is processed from any source. This optimization effectively processes each "teleport group" only once.

4.  **BFS Loop:**
    *   Dequeue `(current_idx, jumps)`.
    *   If `current_idx` is `n - 1`, we've reached the end, return `jumps`.
    *   **Explore Neighbors:**
        *   Add `(current_idx + 1, jumps + 1)` to the queue if `current_idx + 1` is valid (within bounds, not an obstacle, and not visited).
        *   Add `(current_idx - 1, jumps + 1)` to the queue if `current_idx - 1` is valid.
        *   If `current_idx` is a non-obstacle, get its value `val = arr[current_idx]`. If `val` is still in `value_to_indices`, iterate through all `tele_idx` in `value_to_indices[val]`. Add `(tele_idx, jumps + 1)` to the queue if valid and not visited. Then `pop(val)` from `value_to_indices`.

5.  **Unreachable End:** If the queue becomes empty and `n - 1` was never reached, it means the end is unreachable. Return -1.

## Complexity Analysis

*   **Time Complexity: O(N)**
    *   **Preprocessing `value_to_indices`:** Iterating through the array once takes `O(N)`.
    *   **BFS Loop:** Each index `i` is added to the queue and processed at most once.
        *   When an `current_idx` is processed:
            *   Checking `current_idx + 1` and `current_idx - 1` takes `O(1)`.
            *   For teleportation, we iterate through `value_to_indices[val]`. Due to the optimization (`value_to_indices.pop(val)`), each *unique value* `val` leads to its list of indices being iterated over *only once in total* across the entire BFS. The sum of lengths of all lists in `value_to_indices` is `O(N)`. Therefore, the total work for all teleportation jumps combined over the entire BFS is `O(N)`.
    *   Total time complexity is `O(N)`.

*   **Space Complexity: O(N)**
    *   `value_to_indices`: In the worst case, all `N` indices could have unique values or all could have the same value. It stores up to `N` indices, so `O(N)`.
    *   `queue`: In the worst case, could store up to `O(N)` elements (e.g., if all cells are valid and reachable in one jump).
    *   `visited`: Stores up to `N` indices, so `O(N)`.
    *   Total space complexity is `O(N)`.

```python
import collections

class Solution:
    def minJumps(self, arr: list[int]) -> int:
        n = len(arr)

        # Edge case: If the array has 0 or 1 elements, we are already at the end.
        if n <= 1:
            return 0

        # Check for starting or ending on an obstacle.
        # If the start or end is an obstacle, it's impossible to reach.
        if arr[0] == -1 or arr[n-1] == -1:
            return -1 

        # Pre-process: Group indices by their value for efficient teleportation.
        # This dictionary will store {value: [list of indices with that value]}
        # Any non-obstacle cell (value >= 0) can potentially be a teleport source/target.
        value_to_indices = collections.defaultdict(list)
        for i in range(n):
            if arr[i] != -1: # Only non-obstacle cells can be part of teleportation groups
                value_to_indices[arr[i]].append(i)

        # Initialize BFS queue: (current_index, jumps_so_far)
        # Start at index 0 with 0 jumps.
        queue = collections.deque([(0, 0)])

        # Keep track of visited indices to avoid cycles and redundant work.
        visited = {0}

        while queue:
            current_idx, jumps = queue.popleft()

            # If we reached the last index, return the number of jumps.
            if current_idx == n - 1:
                return jumps

            # Explore possible next jumps:
            # 1. Jump to current_idx + 1
            # 2. Jump to current_idx - 1
            # 3. Teleportation (if arr[current_idx] is part of a teleport group)

            # --- 1. Jump to current_idx + 1 ---
            next_idx_plus_1 = current_idx + 1
            if 0 <= next_idx_plus_1 < n and arr[next_idx_plus_1] != -1 and next_idx_plus_1 not in visited:
                visited.add(next_idx_plus_1)
                queue.append((next_idx_plus_1, jumps + 1))

            # --- 2. Jump to current_idx - 1 ---
            prev_idx_minus_1 = current_idx - 1
            if 0 <= prev_idx_minus_1 < n and arr[prev_idx_minus_1] != -1 and prev_idx_minus_1 not in visited:
                visited.add(prev_idx_minus_1)
                queue.append((prev_idx_minus_1, jumps + 1))

            # --- 3. Teleportation ---
            # Get the value of the current cell.
            val = arr[current_idx]
            
            # If this value exists in our pre-processed map (meaning there are other
            # cells with this value, and this group hasn't been fully processed yet).
            if val in value_to_indices: 
                for tele_idx in value_to_indices[val]:
                    # Ensure we don't jump to an already visited index.
                    # arr[tele_idx] != -1 is implicitly true because only non-obstacles
                    # are added to value_to_indices in the first place.
                    if tele_idx not in visited:
                        visited.add(tele_idx)
                        queue.append((tele_idx, jumps + 1))
                
                # CRITICAL OPTIMIZATION: After using a teleport value to explore all its linked indices,
                # remove its entry from value_to_indices. This prevents redundant exploration of
                # these teleport links if we later encounter another cell with the same value.
                # Each 'teleport value group' needs to be processed only once efficiently.
                value_to_indices.pop(val)

        # If the queue becomes empty and we haven't reached the end, it's unreachable.
        return -1

```