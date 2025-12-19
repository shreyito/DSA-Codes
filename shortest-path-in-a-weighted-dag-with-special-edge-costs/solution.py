```python
import collections
import math

class ShortestPathWeightedDAGSpecial:
    """
    Finds the shortest path in a weighted Directed Acyclic Graph (DAG) with special edge costs.

    Problem Description:
    You are given a directed acyclic graph (DAG) with `N` nodes (0-indexed) and `M` weighted edges.
    Each edge `(u, v)` has a base weight `w`. Additionally, some edges are designated
    as 'special'. Traversing a special edge incurs an *additional fixed penalty `P`*
    on top of its base weight.

    Your task is to find the minimum total cost of a path from a given source node `S`
    to a destination node `D`. The total cost of a path is the sum of base weights
    of all edges on the path plus `P` times the count of special edges on that path.

    Example: If a path has edges (e1, e2, e3), and e1, e3 are special with base weights w1, w3,
    and e2 is regular with base weight w2, the total cost is (w1 + w2 + w3) + 2 * P.
    """

    def find_shortest_path(self, N: int, edges: list[tuple[int, int, int, bool]], 
                           special_penalty: int, S: int, D: int) -> int:
        """
        Calculates the minimum cost of a path from S to D in the DAG.

        Args:
            N (int): The number of nodes in the graph. Nodes are 0-indexed.
            edges (list[tuple[int, int, int, bool]]): A list of edges.
                Each tuple represents (u, v, weight, is_special), where:
                - u, v (int): Start and end nodes of the edge.
                - weight (int): The base weight of the edge.
                - is_special (bool): True if the edge is special, False otherwise.
            special_penalty (int): The additional cost incurred for each special edge.
            S (int): The source node.
            D (int): The destination node.

        Returns:
            int: The minimum total cost from S to D. Returns -1 if D is unreachable.
        """

        # Edge case: If source and destination are the same, cost is 0.
        if S == D:
            return 0

        # Build adjacency list and calculate in-degrees for topological sort
        # adj[u] = list of (v, weight, is_special)
        adj = [[] for _ in range(N)]
        in_degree = [0] * N
        for u, v, weight, is_special in edges:
            adj[u].append((v, weight, is_special))
            in_degree[v] += 1

        # Perform Topological Sort (Kahn's algorithm)
        # We need the topological order to process nodes in a way that guarantees
        # all predecessors of a node are processed before the node itself.
        q = collections.deque()
        for i in range(N):
            if in_degree[i] == 0:
                q.append(i)
        
        topological_order = []
        while q:
            u = q.popleft()
            topological_order.append(u)
            for v, _, _ in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    q.append(v)
        
        # A check for cycles could be placed here: if len(topological_order) != N, it's not a DAG.
        # However, the problem statement guarantees a DAG.

        # Dynamic Programming approach for shortest path
        # dist[u][k] = minimum cost to reach node u having used exactly k special edges.
        # A simple path in a graph with N nodes can have at most N-1 edges.
        # Therefore, the maximum number of special edges (k) is N-1.
        # We use `N` as the size for `k` dimension (indices 0 to N-1).
        max_special_edges_count = N 
        dist = [[math.inf] * max_special_edges_count for _ in range(N)]

        # Initialize the source node: cost 0 with 0 special edges
        dist[S][0] = 0

        # Process nodes in topological order
        # This ensures that when we process node `u`, all shortest paths to `u` from `S`
        # (for all possible `k` values) have been finalized from `u`'s predecessors.
        for u in topological_order:
            for k in range(max_special_edges_count): # Iterate through all possible `k` counts for node `u`
                if dist[u][k] == math.inf:
                    continue # This state (node `u`, with `k` special edges) is unreachable

                # Relax outgoing edges from `u`
                for v, weight, is_special in adj[u]:
                    current_path_cost = dist[u][k] + weight
                    
                    if is_special:
                        # If the edge (u, v) is special, increment the special edge count `k`
                        # and add the special penalty.
                        new_k = k + 1
                        # Ensure the new_k count is within the valid range (0 to N-1)
                        if new_k < max_special_edges_count:
                            new_cost = current_path_cost + special_penalty
                            dist[v][new_k] = min(dist[v][new_k], new_cost)
                    else:
                        # If the edge (u, v) is regular, the special edge count `k` remains the same.
                        new_k = k
                        new_cost = current_path_cost
                        dist[v][new_k] = min(dist[v][new_k], new_cost)
        
        # After processing all nodes, find the minimum cost to the destination node `D`
        # across all possible counts of special edges.
        min_cost_to_D = math.inf
        for k in range(max_special_edges_count):
            min_cost_to_D = min(min_cost_to_D, dist[D][k])

        # Return the minimum cost, or -1 if the destination is unreachable.
        return min_cost_to_D if min_cost_to_D != math.inf else -1

    """
    Time Complexity:
    - Building adjacency list and in-degrees: O(N + M), where N is the number of nodes
      and M is the number of edges.
    - Topological Sort (Kahn's algorithm): O(N + M). Each node is enqueued/dequeued once,
      and each edge is processed once.
    - Dynamic Programming iteration:
        - We iterate through N nodes in topological order.
        - For each node `u`, we iterate through `N` possible counts of special edges `k`.
        - For each state `(u, k)`, we iterate through its outgoing edges. The sum of
          outgoing degrees for all nodes is M.
        - Total DP iteration: O(N * N_possible_k * average_degree) = O(N * N * (M/N)) = O(N * M).
    - Finding minimum cost to D: O(N).

    Overall Time Complexity: O(N + M + N*M) which simplifies to O(N * M).

    Space Complexity:
    - Adjacency list: O(N + M)
    - In-degree array: O(N)
    - Topological sort queue and list: O(N)
    - Distance table `dist[N][N]`: O(N^2)

    Overall Space Complexity: O(N^2 + M).
    """


# Test cases for the ShortestPathWeightedDAGSpecial class
if __name__ == "__main__":
    solver = ShortestPathWeightedDAGSpecial()

    tests = [
        {
            "name": "Test 1: Simple path, no special edges",
            "N": 4,
            "edges": [(0, 1, 10, False), (1, 2, 5, False), (2, 3, 3, False)],
            "special_penalty": 100,
            "S": 0, "D": 3,
            "expected": 18 # Path 0->1->2->3: 10 + 5 + 3 = 18
        },
        {
            "name": "Test 2: Simple path, one special edge",
            "N": 4,
            "edges": [(0, 1, 10, True), (1, 2, 5, False), (2, 3, 3, False)],
            "special_penalty": 10,
            "S": 0, "D": 3,
            "expected": 28 # Path 0->1(S)->2->3: (10 + P) + 5 + 3 = (10+10) + 5 + 3 = 28
        },
        {
            "name": "Test 3: Multiple paths, penalty makes regular better",
            "N": 3,
            "edges": [(0, 1, 5, False), (0, 2, 1, True), (1, 2, 1, False)],
            "special_penalty": 10,
            "S": 0, "D": 2,
            "expected": 6 # Path 0->1->2: (5 + 1) = 6. Path 0->2(S): (1 + P) = 11. Choose 6.
        },
        {
            "name": "Test 4: Multiple paths, penalty makes special better",
            "N": 3,
            "edges": [(0, 1, 5, False), (0, 2, 1, True), (1, 2, 1, False)],
            "special_penalty": 2,
            "S": 0, "D": 2,
            "expected": 3 # Path 0->1->2: (5 + 1) = 6. Path 0->2(S): (1 + P) = 3. Choose 3.
        },
        {
            "name": "Test 5: Path with multiple special edges",
            "N": 4,
            "edges": [(0, 1, 1, True), (1, 2, 1, True), (2, 3, 10, False), (0, 3, 20, False)],
            "special_penalty": 3,
            "S": 0, "D": 3,
            "expected": 18 # Path 0->1(S)->2(S)->3: (1+P) + (1+P) + 10 = (1+3) + (1+3) + 10 = 4 + 4 + 10 = 18. Path 0->3: 20. Choose 18.
        },
        {
            "name": "Test 6: Unreachable destination",
            "N": 3,
            "edges": [(0, 1, 1, False)],
            "special_penalty": 1,
            "S": 0, "D": 2,
            "expected": -1
        },
        {
            "name": "Test 7: Source is Destination",
            "N": 3,
            "edges": [(0, 1, 1, False)], # Edges irrelevant if S=D
            "special_penalty": 1,
            "S": 0, "D": 0,
            "expected": 0
        },
        {
            "name": "Test 8: Complex graph with mixed edges",
            "N": 5,
            "edges": [
                (0, 1, 10, False), (0, 2, 2, True),
                (1, 3, 5, False), (1, 4, 10, True),
                (2, 3, 1, False), (2, 4, 8, True),
                (3, 4, 3, False)
            ],
            "special_penalty": 5,
            "S": 0, "D": 4,
            "expected": 11 
            # Path 1: 0->2(S)->3->4
            #   0->2: (2 + P=5) = 7 (k=1)
            #   2->3: (1) = 1 (k=1)
            #   3->4: (3) = 3 (k=1)
            # Total Path 1 cost: 7 + 1 + 3 = 11.
            #
            # Path 2: 0->2(S)->4(S)
            #   0->2: (2 + P=5) = 7 (k=1)
            #   2->4: (8 + P=5) = 13 (k=2)
            # Total Path 2 cost: 7 + 13 = 20.
            #
            # Path 3: 0->1->3->4
            #   0->1: (10) = 10 (k=0)
            #   1->3: (5) = 5 (k=0)
            #   3->4: (3) = 3 (k=0)
            # Total Path 3 cost: 10 + 5 + 3 = 18.
            #
            # Path 4: 0->1->4(S)
            #   0->1: (10) = 10 (k=0)
            #   1->4: (10 + P=5) = 15 (k=1)
            # Total Path 4 cost: 10 + 15 = 25.
            # Minimum is 11.
        },
        {
            "name": "Test 9: Larger N, multiple paths with many special edges",
            "N": 6,
            "edges": [
                (0, 1, 1, True), (0, 2, 1, False),
                (1, 3, 1, True), (1, 4, 10, False),
                (2, 3, 10, False), (2, 4, 1, True),
                (3, 5, 1, True), (4, 5, 10, False)
            ],
            "special_penalty": 2,
            "S": 0, "D": 5,
            "expected": 9 
            # Path 1: 0->1(S)->3(S)->5(S)
            #   (1+P) + (1+P) + (1+P) = (1+2) + (1+2) + (1+2) = 3 + 3 + 3 = 9 (k=3)
            # Other paths lead to higher costs. E.g.
            # Path 2: 0->2(R)->4(S)->5(R)
            #   1 + (1+P) + 10 = 1 + (1+2) + 10 = 1 + 3 + 10 = 14 (k=1)
        }
    ]

    print("Running tests for ShortestPathWeightedDAGSpecial...\n")
    for i, test in enumerate(tests):
        result = solver.find_shortest_path(
            test["N"], test["edges"], test["special_penalty"], test["S"], test["D"]
        )
        print(f"--- {test['name']} ---")
        print(f"  Input: N={test['N']}, Edges={test['edges']}, Penalty={test['special_penalty']}, S={test['S']}, D={test['D']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        assert result == test["expected"], f"Test {i+1} Failed: {test['name']}. Expected {test['expected']}, Got {result}"
        print("  Status: Passed\n")
    
    print("All test cases passed!\n")
    print("--- Complexity Analysis ---")
    print("Time Complexity: O(N * M)")
    print("Space Complexity: O(N^2 + M)")

```