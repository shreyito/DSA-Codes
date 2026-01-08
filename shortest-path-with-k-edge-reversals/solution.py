```python
import heapq
import math

class Solution:
    def shortestPathWithKReversals(self, n: int, edges: list[tuple[int, int, int]], source: int, target: int, k: int) -> int:
        """
        Finds the shortest path from a source node to a target node in a directed graph
        with the allowance of reversing at most K edges.

        Each edge reversal costs one unit from the K budget but does not change the
        traversal cost (weight) of that edge.

        Args:
            n: The number of nodes in the graph (0-indexed).
            edges: A list of tuples, where each tuple (u, v, w) represents a directed edge
                   from u to v with weight w.
            source: The starting node.
            target: The destination node.
            k: The maximum number of edge reversals allowed.

        Returns:
            The minimum cost to reach the target node from the source node with at most
            k reversals. Returns -1 if the target is unreachable.

        Time Complexity:
            O(M * K * log(N * K))
            Where N is the number of nodes, M is the number of original edges, and K is
            the maximum number of reversals.
            The state space for Dijkstra's is (node, reversals_used), which has N * (K+1) states.
            Each original edge (u, v) can be traversed in two ways for each reversal count:
            1. Normally: u -> v, costing 0 reversals. This adds (K+1) edges to the state graph.
            2. Reversed: v -> u, costing 1 reversal. This adds K edges to the state graph.
            So, the total number of edges in the state graph (E') is approximately 2 * M * K.
            Dijkstra's complexity is O(E' * log(V')), where V' is the number of states.
            V' = N * (K+1), E' = 2 * M * K.
            Thus, O(M * K * log(N * K)).

        Space Complexity:
            O(N * K + M)
            The `dist` array takes O(N * K) space.
            The adjacency lists (`adj` and `rev_adj`) take O(N + M) space.
            The priority queue stores at most O(N * K) elements in the worst case.
            Overall, dominated by O(N * K + M).
        """

        # 1. Build adjacency lists for the graph and its reverse.
        #    adj[u] stores (v, weight) for original edges u -> v.
        #    rev_adj[u] stores (v, weight) for original edges x -> u. This helps
        #    identify edges that can be reversed to become u -> x.
        adj = [[] for _ in range(n)]
        rev_adj = [[] for _ in range(n)]

        for u, v, w in edges:
            adj[u].append((v, w))
            # If there's an edge u -> v, it means we can potentially reverse it
            # to travel from v -> u. So, v's 'reverse neighbor' is u.
            # However, the problem formulation implies we consider reversing edge (x,u)
            # to traverse (u,x). So `rev_adj[u]` should store `(x, weight)` for an edge `x -> u`.
            rev_adj[v].append((u, w))

        # 2. Initialize distance array.
        #    dist[node][reversals_used] stores the minimum cost to reach 'node'
        #    using 'reversals_used' reversals so far.
        #    Initialize all distances to infinity.
        dist = [[math.inf] * (k + 1) for _ in range(n)]

        # 3. Priority Queue for Dijkstra's.
        #    Stores tuples: (current_cost, current_node, reversals_used).
        #    Start from the source node with 0 cost and 0 reversals.
        pq = [(0, source, 0)]
        dist[source][0] = 0

        # 4. Dijkstra's Algorithm
        while pq:
            current_cost, u, reversals_used = heapq.heappop(pq)

            # If we've already found a shorter path to this state, skip.
            if current_cost > dist[u][reversals_used]:
                continue

            # Option 1: Traverse existing edges normally (0 reversal cost).
            # Iterate over all original outgoing edges from 'u'.
            for v, weight in adj[u]:
                if current_cost + weight < dist[v][reversals_used]:
                    dist[v][reversals_used] = current_cost + weight
                    heapq.heappush(pq, (dist[v][reversals_used], v, reversals_used))

            # Option 2: Reverse an edge and traverse it (costs 1 reversal budget).
            # This is only possible if we have reversal budget left.
            if reversals_used < k:
                # Iterate over edges (x, u) that can be reversed to become (u, x).
                # `rev_adj[u]` contains all `x` such that an edge `x -> u` exists.
                for x, weight in rev_adj[u]:
                    # If we reverse x -> u to u -> x, we reach node x.
                    # The cost is the original weight, and we use one reversal.
                    if current_cost + weight < dist[x][reversals_used + 1]:
                        dist[x][reversals_used + 1] = current_cost + weight
                        heapq.heappush(pq, (dist[x][reversals_used + 1], x, reversals_used + 1))

        # 5. Find the minimum cost to reach the target across all possible reversal counts (0 to k).
        min_cost = math.inf
        for r in range(k + 1):
            min_cost = min(min_cost, dist[target][r])

        # If min_cost is still infinity, the target is unreachable.
        return min_cost if min_cost != math.inf else -1

# Test Cases
if __name__ == '__main__':
    sol = Solution()

    # Test Case 1: Basic - no reversals needed
    # Path: 0 -> 1 -> 2 (cost 1+1=2)
    n1, edges1, s1, t1, k1 = 3, [(0, 1, 1), (1, 2, 1)], 0, 2, 0
    print(f"Test Case 1: Expected: 2, Got: {sol.shortestPathWithKReversals(n1, edges1, s1, t1, k1)}")
    assert sol.shortestPathWithKReversals(n1, edges1, s1, t1, k1) == 2

    # Test Case 2: Reversal makes a path possible/shorter
    # Path: 0 -> 1 (cost 10)
    # Reverse (2,1) to (1,2) (cost 1, 1 reversal)
    # Total cost: 10 + 1 = 11
    n2, edges2, s2, t2, k2 = 3, [(0, 1, 10), (2, 1, 1)], 0, 2, 1
    print(f"Test Case 2: Expected: 11, Got: {sol.shortestPathWithKReversals(n2, edges2, s2, t2, k2)}")
    assert sol.shortestPathWithKReversals(n2, edges2, s2, t2, k2) == 11

    # Test Case 3: Reversal makes a much shorter path (compared to direct/normal path)
    # Goal: reach node 2 from 0 with k=1.
    # Normal path 0 -> 1 -> 2: cost 100+100 = 200 (0 reversals).
    # Path with reversal: 0 -> 3 (cost 1, 0 rev) -> 4 (cost 1, 0 rev) -> 2 (by reversing 2->4, cost 5, 1 rev).
    # Total cost: 1 + 1 + 5 = 7.
    n3, edges3, s3, t3, k3 = 5, [(0, 1, 100), (1, 2, 100), (2, 4, 5), (0, 3, 1), (3, 4, 1)], 0, 2, 1
    print(f"Test Case 3: Expected: 7, Got: {sol.shortestPathWithKReversals(n3, edges3, s3, t3, k3)}")
    assert sol.shortestPathWithKReversals(n3, edges3, s3, t3, k3) == 7

    # Test Case 4: Insufficient budget for reversal, target unreachable
    # To go 0 -> 1 -> 2, edge (2,1) needs to be reversed. Budget k=0.
    n4, edges4, s4, t4, k4 = 3, [(0, 1, 10), (2, 1, 1)], 0, 2, 0
    print(f"Test Case 4: Expected: -1, Got: {sol.shortestPathWithKReversals(n4, edges4, s4, t4, k4)}")
    assert sol.shortestPathWithKReKversals(n4, edges4, s4, t4, k4) == -1

    # Test Case 5: Target is source
    n5, edges5, s5, t5, k5 = 3, [(0, 1, 5)], 0, 0, 1
    print(f"Test Case 5: Expected: 0, Got: {sol.shortestPathWithKReversals(n5, edges5, s5, t5, k5)}")
    assert sol.shortestPathWithKReversals(n5, edges5, s5, t5, k5) == 0

    # Test Case 6: Multiple paths, no reversals optimal
    # Path 1 (normal): 0 -> 3 -> 4. Cost = 1 + 1 = 2. (0 reversals)
    # Path 2 (normal): 0 -> 1 -> 2 -> 4. Cost = 10 + 20 + 5 = 35. (0 reversals)
    n6, edges6, s6, t6, k6 = 5, [(0, 1, 10), (1, 2, 20), (2, 4, 5), (0, 3, 1), (3, 4, 1)], 0, 4, 1
    print(f"Test Case 6: Expected: 2, Got: {sol.shortestPathWithKReversals(n6, edges6, s6, t6, k6)}")
    assert sol.shortestPathWithKReversals(n6, edges6, s6, t6, k6) == 2

    # Test Case 7: Complex scenario, direct path is optimal with 0 reversals
    # From 0 to 3:
    # Option 1: 0 -> 3 (direct). Cost 100. Reversals 0.
    # Option 2: 0 -> 1 (cost 10) -> 2 (by reversing 2->1, cost 1, 1 reversal) -> 3 (cost 1).
    # Total cost = 10 + 1 + 1 = 12.
    n7, edges7, s7, t7, k7 = 4, [(0, 1, 10), (0, 3, 100), (2, 1, 1), (2, 3, 1)], 0, 3, 1
    print(f"Test Case 7: Expected: 12, Got: {sol.shortestPathWithKReversals(n7, edges7, s7, t7, k7)}")
    assert sol.shortestPathWithKReversals(n7, edges7, s7, t7, k7) == 12

    print("\nAll test cases passed!")
```