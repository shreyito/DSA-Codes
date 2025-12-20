The "Minimum Spanning Tree with Edge Weight Modification" problem asks us to find the minimum possible total weight of a Minimum Spanning Tree (MST) in a given undirected, connected graph. We are allowed to modify the weights of a limited number of edges: specifically, we can choose up to `K` edges and reduce their weight by a fixed amount `D`. An edge's weight cannot become negative; it is capped at 0 if `original_weight - D < 0`.

This problem can be effectively solved using a modified Kruskal's algorithm combined with a priority queue to manage the discount budget.

**Algorithm Breakdown:**

1.  **Edge Preprocessing:**
    *   For each edge `(u, v, weight)` in the input graph, calculate its potential "discounted weight": `w_disc = max(0, weight - D)`.
    *   Store these edges as tuples: `(w_disc, weight, u, v)`. This allows us to access both the discounted and original weights, as well as the connected vertices.

2.  **Sort Edges:**
    *   Sort the `processed_edges` list primarily by `w_disc` in ascending order. This ensures that when we iterate through edges, we always consider the "cheapest" options first, assuming we apply a discount.

3.  **Modified Kruskal's with Discount Management:**
    *   Initialize a Disjoint Set Union (DSU) structure for `N` vertices to keep track of connected components.
    *   Initialize `mst_cost = 0`.
    *   Initialize `edges_in_mst_count = 0`. This counter tracks how many edges have been added to form the MST. We stop when it reaches `N-1`.
    *   Initialize a min-priority queue `pq_savings`. This priority queue will store the *saving amounts* (`original_weight - discounted_weight`) for all edges that are *currently part of our provisional MST and are assumed to be discounted*. The size of this priority queue effectively tracks the number of discounts currently used.

4.  **Iterate and Build MST:**
    *   Iterate through the `processed_edges` (sorted by `w_disc`):
        *   For each edge `(w_disc, w_orig, u, v)`:
            *   If `u` and `v` are already in the same connected component (checked using `dsu.find(u) == dsu.find(v)`), skip this edge as it would form a cycle.
            *   If `u` and `v` are in different components:
                *   We must include this edge in our MST to connect the components.
                *   Perform `dsu.union(u, v)`.
                *   Add `w_disc` to `mst_cost`. This is a provisional cost, assuming we discount this edge.
                *   Calculate the saving for this edge: `saving = w_orig - w_disc`.
                *   Push this `saving` onto `pq_savings`.
                *   **Manage Discount Budget:** If `len(pq_savings)` (the number of provisionally discounted edges) becomes greater than `K`:
                    *   We have exceeded our discount limit. We must "revoke" a discount.
                    *   To minimize the overall MST cost, we revoke the discount that provides the *smallest saving*. This means we effectively pay the original weight for that edge instead of its discounted weight.
                    *   Pop the smallest `saving_amount` from `pq_savings`.
                    *   Add this `smallest_saving_amount` back to `mst_cost`. (Because `mst_cost` currently includes `w_disc`, and `w_disc + saving_amount = w_orig`).
                *   Increment `edges_in_mst_count`.
                *   If `edges_in_mst_count == N - 1`, the MST is complete, so break the loop.

5.  **Return `mst_cost`**: This will be the minimum total weight of the MST after optimal discount application.

**Time and Space Complexity:**

*   **Time Complexity:**
    *   Preprocessing edges: `O(M)`
    *   Sorting edges: `O(M log M)`
    *   DSU operations: Each `find` and `union` takes nearly constant time `O(α(N))`, where `α` is the inverse Ackermann function. There are `O(M)` DSU operations.
    *   Priority Queue operations: Each `heappush` and `heappop` takes `O(log P)` time, where `P` is the size of the priority queue. In the worst case, `P` can be up to `N-1`. There are `O(M)` priority queue operations.
    *   Overall: `O(M log M + M log N)`. Since `M` can be up to `N^2`, `log N < log M`. Thus, the dominant factor is `O(M log M)`.

*   **Space Complexity:**
    *   DSU structure: `O(N)` for parent array.
    *   `processed_edges` list: `O(M)` to store the edge tuples.
    *   `pq_savings`: In the worst case, it can store up to `min(K, N-1)` elements. So, `O(min(K, N))`, which simplifies to `O(N)` for practical purposes.
    *   Overall: `O(N + M)`.

This approach ensures optimality by always considering the cheapest available options (discounted edges) first, and then efficiently managing the discount budget by revoking the least beneficial discounts if the budget is exceeded.

```python
import heapq

class DSU:
    """
    Disjoint Set Union (DSU) with path compression.
    Allows efficient tracking of connected components in a graph.
    """
    def __init__(self, n):
        """
        Initializes the DSU structure for n elements.
        Each element is initially in its own set.
        """
        self.parent = list(range(n))

    def find(self, i):
        """
        Finds the representative (root) of the set containing element i.
        Applies path compression to flatten the tree.
        """
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Merges the sets containing elements i and j.
        Returns True if a merge happened, False if i and j were already in the same set.
        """
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_j] = root_i
            return True
        return False

def min_spanning_tree_with_discount(n, edges, k, d):
    """
    Calculates the minimum spanning tree weight of a graph where up to K edges
    can have their weights reduced by a fixed amount D. An edge's weight cannot
    become negative (capped at 0).

    The algorithm uses a modified Kruskal's approach:
    1. Each edge is considered with its potential discounted weight (max(0, original_weight - D)).
    2. Edges are sorted by these discounted weights.
    3. Kruskal's algorithm proceeds, always trying to add the cheapest (discounted) edge.
    4. A min-priority queue tracks the 'savings' (original_weight - discounted_weight)
       of all edges currently chosen and discounted in the provisional MST.
    5. If the number of provisionally discounted edges exceeds K, the discount
       that yielded the smallest saving is 'revoked' (its original weight is
       added back to the MST cost), ensuring only K discounts are used optimally.

    Args:
        n (int): The number of vertices in the graph (0-indexed).
        edges (list): A list of tuples, where each tuple is (u, v, weight)
                      representing an edge between vertex u and vertex v with
                      the given weight. Vertices are assumed to be 0-indexed.
        k (int): The maximum number of edges that can be discounted.
        d (int): The fixed discount amount applied to chosen edges.

    Returns:
        int: The minimum total weight of the MST.
    """
    if n <= 1:
        return 0 # MST cost for 0 or 1 vertex is 0

    # Step 1: Prepare edges with their discounted weights and original weights.
    # Store as (discounted_weight, original_weight, u, v).
    processed_edges = []
    for u, v, weight in edges:
        discounted_weight = max(0, weight - d)
        processed_edges.append((discounted_weight, weight, u, v))

    # Step 2: Sort edges primarily by their discounted weight in ascending order.
    # This ensures that when we consider edges, we prioritize those that are
    # cheapest when discounted.
    processed_edges.sort()

    dsu = DSU(n)
    mst_cost = 0
    edges_in_mst_count = 0
    
    # Step 3: Initialize a min-priority queue to store the saving amounts
    # for edges that are currently part of the MST and are provisionally discounted.
    # The size of this PQ indirectly tracks the number of discounted edges used.
    pq_savings = [] # Stores (saving_amount)

    # Step 4: Iterate through the sorted edges, applying a modified Kruskal's logic.
    for w_disc, w_orig, u, v in processed_edges:
        if dsu.find(u) != dsu.find(v):
            # If this edge connects two previously disconnected components,
            # it must be included in our MST.

            dsu.union(u, v)
            mst_cost += w_disc # Provisionally add the discounted weight to the total cost

            # Calculate the potential saving if this edge is discounted.
            saving = w_orig - w_disc
            heapq.heappush(pq_savings, saving) # Add this saving to the priority queue

            # Step 5: Check if we have exceeded our discount budget (K).
            # If len(pq_savings) > K, it means we have provisionally discounted
            # K+1 edges. We must revert one of them to its original price.
            # To minimize the overall MST cost, we revoke the discount that
            # offered the smallest saving.
            if len(pq_savings) > k:
                smallest_saving_to_revoke = heapq.heappop(pq_savings)
                mst_cost += smallest_saving_to_revoke # Add back the saving amount to mst_cost.
                                                     # This effectively changes the cost of that
                                                     # specific edge from w_disc back to w_orig.

            edges_in_mst_count += 1
            # An MST for a connected graph with N vertices always has N-1 edges.
            if edges_in_mst_count == n - 1:
                break # MST is complete, no need to process further edges

    return mst_cost

# --- Test Cases ---

if __name__ == "__main__":
    def run_test(test_name, n, edges, k, d, expected):
        result = min_spanning_tree_with_discount(n, edges, k, d)
        print(f"--- {test_name} ---")
        print(f"N={n}, Edges={edges}, K={k}, D={d}")
        print(f"Expected: {expected}, Got: {result}")
        assert result == expected, f"Test Failed: Expected {expected}, Got {result}"
        print("Status: Passed\n")

    # Test Case 1: Basic functionality (Example from problem description)
    # Graph: 0--1(10), 1--2(12), 0--2(100)
    # K=1, D=5
    # Edges sorted by w_disc: (0,1,10)->(5), (1,2,12)->(7), (0,2,100)->(95)
    # 1. Add (0,1) with cost 5. PQ=[5].
    # 2. Add (1,2) with cost 7. PQ=[5,5]. (len=2 > K=1). Pop 5. Cost = 5+7+5 = 17. PQ=[5].
    # MST complete (2 edges).
    run_test(
        "Test Case 1: Basic functionality",
        n=3,
        edges=[(0, 1, 10), (1, 2, 12), (0, 2, 100)],
        k=1,
        d=5,
        expected=17
    )

    # Test Case 2: K = 0 (No discounts allowed) - Should behave like standard Kruskal's
    # Graph: 0--1(10), 1--2(20), 2--3(5)
    # Standard MST: (2,3,5), (0,1,10), (1,2,20). Total = 5+10+20 = 35.
    run_test(
        "Test Case 2: K=0 (No discounts)",
        n=4,
        edges=[(0, 1, 10), (1, 2, 20), (2, 3, 5)],
        k=0,
        d=100, # Large D, but K=0 means no actual discount
        expected=35
    )

    # Test Case 3: K is large enough to discount all MST edges to 0
    # Graph: 0--1(10), 1--2(20), 2--3(5)
    # All edges become 0 with D=100. K=3 means all 3 MST edges can be discounted.
    run_test(
        "Test Case 3: K allows all MST edges discounted to 0",
        n=4,
        edges=[(0, 1, 10), (1, 2, 20), (2, 3, 5)],
        k=3,
        d=100,
        expected=0
    )

    # Test Case 4: Discount is small, some edges might not be fully discounted
    # Graph: 0--1(10), 0--2(6), 1--2(3), 1--3(15), 2--3(8)
    # Standard MST: (1,2,3), (0,2,6), (2,3,8). Total = 3+6+8 = 17.
    # D=5, K=1.
    # Edges with (w_disc, w_orig, u, v) and saving:
    # (1,2,3) -> (0,3,1,2) s=3
    # (0,2,6) -> (1,6,0,2) s=5
    # (2,3,8) -> (3,8,2,3) s=5
    # (0,1,10) -> (5,10,0,1) s=5
    # (1,3,15) -> (10,15,1,3) s=5
    # Optimal MST with 1 discount: discount (0,2,6) to (0,2,1). Cost = 3+1+8 = 12.
    # Or discount (2,3,8) to (2,3,3). Cost = 3+6+3 = 12.
    run_test(
        "Test Case 4: Small discount, partial discounts",
        n=4,
        edges=[(0, 1, 10), (0, 2, 6), (1, 2, 3), (1, 3, 15), (2, 3, 8)],
        k=1,
        d=5,
        expected=12
    )

    # Test Case 5: Disconnected graph (should return MST for connected components if not assumed connected)
    # Problem states graph is connected, so this is an invalid input per strict problem definition.
    # However, if it were allowed, the code would implicitly build an MST spanning a single component.
    # Assuming the input guarantees connectivity (e.g., this MST will have N-1 edges).
    run_test(
        "Test Case 5: All edges expensive, high discount but K limited",
        n=5,
        edges=[(0,1,100), (0,2,100), (0,3,100), (0,4,100)],
        k=2,
        d=90,
        expected=220 # 2 edges discounted (100->10), 2 edges at original 100. 2*10 + 2*100 = 220.
    )

    # Test Case 6: Empty graph or single node
    run_test(
        "Test Case 6: N=0",
        n=0,
        edges=[],
        k=0,
        d=10,
        expected=0
    )
    run_test(
        "Test Case 7: N=1",
        n=1,
        edges=[],
        k=0,
        d=10,
        expected=0
    )

    # Test Case 8: All edges have weight 0 or very low, D doesn't matter much
    run_test(
        "Test Case 8: Low edge weights",
        n=4,
        edges=[(0,1,1), (1,2,1), (2,3,1)],
        k=1,
        d=10,
        expected=2 # One edge becomes 0, two remain 1.
    )

    print("All test cases passed!")

```