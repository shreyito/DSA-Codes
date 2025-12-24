The problem "Minimum Spanning Tree with Dynamic Edge Weights" addresses a scenario where the cost of using an edge in a graph is not static but varies based on a global parameter `x`. Specifically, each edge `(u, v)` has a weight defined by a linear function `W_uv(x) = A_uv * x + B_uv`, where `A_uv` and `B_uv` are constant coefficients for that particular edge. The goal is to compute the total weight of the Minimum Spanning Tree (MST) for a series of given `x` values.

This problem requires calculating an MST for each `x` value independently, as the varying `x` can change the relative order of edge weights, potentially leading to a different MST structure for different `x`.

## Algorithm

The solution employs Kruskal's algorithm, which is well-suited for this problem due to its simplicity in handling edges sorted by weight. A Disjoint Set Union (DSU) data structure is used to efficiently detect cycles and merge connected components.

For each `x` value in the query list:

1.  **Calculate Edge Weights:** Iterate through all given edge parameters `(u, v, A, B)`. For each edge, compute its current weight using the formula `weight = A * x + B`. Store these as tuples `(weight, u, v)`.
2.  **Sort Edges:** Sort the newly calculated edges in non-decreasing order based on their `weight`.
3.  **Initialize DSU:** Create a Disjoint Set Union (DSU) instance for `N` vertices (where `N` is the number of vertices in the graph). The DSU will manage the connected components.
4.  **Build MST (Kruskal's):**
    *   Initialize `mst_weight = 0.0` and `edges_in_mst = 0`.
    *   Iterate through the sorted edges. For each edge `(current_weight, u, v)`:
        *   Check if vertices `u` and `v` are already in the same connected component using `dsu.find()`.
        *   If `u` and `v` are not connected, it means adding this edge will not form a cycle. Perform a `dsu.union()` operation to merge their components.
        *   Add `current_weight` to `mst_weight`.
        *   Increment `edges_in_mst`.
        *   If `edges_in_mst` reaches `N - 1` (the number of edges required for an MST spanning all `N` vertices in a connected graph), the MST has been formed. Break the loop.
5.  **Store Result:** Record the calculated `mst_weight` for the current `x`.

Finally, return the list of all computed MST weights.

## Time and Space Complexity

Let `N` be the number of vertices and `M` be the number of edges in the graph. Let `Q` be the number of `x` values for which the MST needs to be calculated.

*   **Time Complexity:**
    *   For each `x` query:
        *   Calculating edge weights: `O(M)`
        *   Sorting edges: `O(M log M)`
        *   Kruskal's algorithm with DSU: `O(M * α(N))`, where `α` is the inverse Ackermann function, which is practically a constant.
        *   The dominant factor for a single query is `O(M log M)`.
    *   **Total Time Complexity:** `O(Q * M log M)`

*   **Space Complexity:**
    *   DSU structure: `O(N)` for parent and rank arrays.
    *   Storing edge parameters: `O(M)`.
    *   Storing current edge weights for sorting: `O(M)`.
    *   Results list: `O(Q)`.
    *   **Total Space Complexity:** `O(N + M + Q)`

```python
class DSU:
    """
    Disjoint Set Union (DSU) data structure with path compression and union by rank.
    Used to efficiently manage sets of connected components.
    """
    def __init__(self, n):
        """
        Initializes the DSU structure for 'n' elements.
        Each element is initially in its own set.
        """
        self.parent = list(range(n))
        self.rank = [0] * n # For union by rank optimization

    def find(self, i):
        """
        Finds the representative (root) of the set containing element 'i'.
        Performs path compression to flatten the tree.
        """
        if self.parent[i] == i:
            return i
        # Path compression: make the representative the direct parent of i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Unites the sets containing elements 'i' and 'j'.
        Returns True if a union was performed (i.e., i and j were in different sets),
        False otherwise (i and j were already in the same set).
        Uses union by rank to keep the tree flat.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank: attach the smaller rank tree under the root of the larger rank tree
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                # If ranks are equal, pick one root and increment its rank
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True # Successfully merged
        return False # Already in the same set


def minimum_spanning_tree_dynamic_weights(num_vertices: int, edges_params: list[tuple[int, int, float, float]], x_values: list[float]) -> list[float]:
    """
    Calculates the Minimum Spanning Tree (MST) total weight for a graph
    with dynamic edge weights, for multiple given values of a parameter 'x'.

    Each edge (u, v) has a weight function W_uv(x) = A_uv * x + B_uv.

    Args:
        num_vertices (int): The number of vertices in the graph (0 to num_vertices-1).
        edges_params (list of tuple): A list where each tuple represents an edge
                                      and its weight parameters: (u, v, A_uv, B_uv).
                                      u, v are 0-indexed vertex identifiers.
                                      A_uv, B_uv are float coefficients for the
                                      linear weight function A*x + B.
        x_values (list of float): A list of global parameter x values for which
                                  to calculate the MST weight.

    Returns:
        list of float: A list of MST total weights, corresponding to each x value
                       in the input x_values list.
                       Returns 0.0 for a graph with 0 or 1 vertex.
                       Assumes the underlying graph structure is connected,
                       such that an MST spanning all vertices is always possible.
    """
    results = []

    # Handle edge cases for empty or single-vertex graphs
    if num_vertices == 0:
        return [0.0] * len(x_values)
    if num_vertices == 1:
        return [0.0] * len(x_values)

    for x in x_values:
        # Step 1: Calculate current edge weights based on the current x
        current_edges = []
        for u, v, A, B in edges_params:
            weight = A * x + B
            current_edges.append((weight, u, v))

        # Step 2: Sort edges by their current calculated weights
        # Kruskal's algorithm requires edges to be sorted by weight
        current_edges.sort()

        # Step 3: Initialize DSU structure for the current MST calculation
        dsu = DSU(num_vertices)
        mst_weight = 0.0
        edges_in_mst = 0

        # Step 4: Build MST using Kruskal's algorithm
        for weight, u, v in current_edges:
            # If adding this edge connects two previously disconnected components
            if dsu.union(u, v):
                mst_weight += weight
                edges_in_mst += 1
                # An MST for N vertices has exactly N-1 edges
                if edges_in_mst == num_vertices - 1:
                    break # MST fully formed

        # Check for connectivity (optional, based on problem requirements).
        # If the graph is not connected, edges_in_mst will be less than num_vertices - 1.
        # For this problem, we typically assume the graph structure allows for a connected MST.
        # The calculated mst_weight will be for a spanning forest if disconnected.
        # We return the calculated sum regardless, assuming it's for the overall MST.

        results.append(mst_weight)

    return results

# --- Test Cases ---

if __name__ == "__main__":
    print("--- Test Case 1: Simple Graph (Linear Weights) ---")
    num_vertices_1 = 3
    edges_params_1 = [
        (0, 1, 1.0, 0.0), # W(x) = x
        (1, 2, 2.0, 0.0), # W(x) = 2x
        (0, 2, 0.0, 10.0) # W(x) = 10
    ]
    x_values_1 = [1.0, 5.0, 10.0]
    # Expected Output Calculation:
    # x = 1: (0,1)=1, (1,2)=2, (0,2)=10. MST edges: (0,1), (1,2). Total = 1+2 = 3.0
    # x = 5: (0,1)=5, (1,2)=10, (0,2)=10. MST edges: (0,1), (1,2) or (0,2). Total = 5+10 = 15.0
    # x = 10: (0,1)=10, (1,2)=20, (0,2)=10. MST edges: (0,1), (0,2). Total = 10+10 = 20.0
    expected_1 = [3.0, 15.0, 20.0]
    result_1 = minimum_spanning_tree_dynamic_weights(num_vertices_1, edges_params_1, x_values_1)
    print(f"Input x_values: {x_values_1}")
    print(f"Calculated MST weights: {result_1}")
    print(f"Expected MST weights:   {expected_1}")
    assert result_1 == expected_1, f"Test Case 1 Failed: {result_1} != {expected_1}"
    print("Test Case 1 Passed!\n")

    print("--- Test Case 2: Edge Case (Single Vertex Graph) ---")
    num_vertices_2 = 1
    edges_params_2 = [] # No edges for a single vertex
    x_values_2 = [0.0, 10.0, -5.0]
    # Expected Output Calculation: For 1 vertex, MST weight is always 0.
    expected_2 = [0.0, 0.0, 0.0]
    result_2 = minimum_spanning_tree_dynamic_weights(num_vertices_2, edges_params_2, x_values_2)
    print(f"Input x_values: {x_values_2}")
    print(f"Calculated MST weights: {result_2}")
    print(f"Expected MST weights:   {expected_2}")
    assert result_2 == expected_2, f"Test Case 2 Failed: {result_2} != {expected_2}"
    print("Test Case 2 Passed!\n")

    print("--- Test Case 3: More Complex Graph ---")
    num_vertices_3 = 4
    edges_params_3 = [
        (0, 1, 1.0, 1.0),   # W(x) = x + 1
        (0, 2, 0.5, 5.0),   # W(x) = 0.5x + 5
        (0, 3, 0.0, 10.0),  # W(x) = 10
        (1, 2, 2.0, 0.0),   # W(x) = 2x
        (2, 3, 0.1, 12.0)   # W(x) = 0.1x + 12
    ]
    x_values_3 = [2.0, 20.0]
    # Expected Output Calculation:
    # x = 2:
    #   (0,1)=3, (0,2)=6, (0,3)=10, (1,2)=4, (2,3)=12.2
    #   Sorted: (0,1,3), (1,2,4), (0,2,6), ...
    #   MST: (0,1) weight 3, (1,2) weight 4, (0,3) weight 10. Total = 3+4+10 = 17.0
    # x = 20:
    #   (0,1)=21, (0,2)=15, (0,3)=10, (1,2)=40, (2,3)=14
    #   Sorted: (0,3,10), (2,3,14), (0,2,15), (0,1,21), (1,2,40)
    #   MST: (0,3) weight 10, (2,3) weight 14, (0,2) is already covered, (0,1) weight 21. Total = 10+14+21 = 45.0
    expected_3 = [17.0, 45.0]
    result_3 = minimum_spanning_tree_dynamic_weights(num_vertices_3, edges_params_3, x_values_3)
    print(f"Input x_values: {x_values_3}")
    print(f"Calculated MST weights: {result_3}")
    print(f"Expected MST weights:   {expected_3}")
    assert result_3 == expected_3, f"Test Case 3 Failed: {result_3} != {expected_3}"
    print("Test Case 3 Passed!\n")

    print("--- Test Case 4: Zero Vertices ---")
    num_vertices_4 = 0
    edges_params_4 = []
    x_values_4 = [5.0]
    expected_4 = [0.0]
    result_4 = minimum_spanning_tree_dynamic_weights(num_vertices_4, edges_params_4, x_values_4)
    print(f"Input x_values: {x_values_4}")
    print(f"Calculated MST weights: {result_4}")
    print(f"Expected MST weights:   {expected_4}")
    assert result_4 == expected_4, f"Test Case 4 Failed: {result_4} != {expected_4}"
    print("Test Case 4 Passed!\n")

    print("--- All test cases passed! ---")
```