```python
class DSU:
    """
    Disjoint Set Union (DSU) data structure with path compression and union by rank.
    Optimized for efficient find and union operations.
    """
    def __init__(self, n):
        # parent[i] stores the parent of element i.
        # Initially, each element is its own parent (representative of its own set).
        self.parent = list(range(n))
        # rank[i] stores the rank (height) of the tree rooted at i.
        # Used to optimize union operations (union by rank).
        self.rank = [0] * n
        # num_components stores the current count of disjoint sets.
        self.num_components = n

    def find(self, i):
        """
        Finds the representative (root) of the set containing element i.
        Implements path compression: Flattens the tree by making all nodes
        on the path from i to its root point directly to the root.
        """
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """
        Merges the sets containing i and j.
        Returns True if i and j were in different sets and were merged, False otherwise.
        Implements union by rank: Attaches the smaller rank tree under the root of the higher rank tree.
        This keeps the tree flatter, reducing the depth of future finds.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_j] < self.rank[root_i]:
                self.parent[root_j] = root_i
            else:
                # If ranks are equal, pick one as root and increment its rank.
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            self.num_components -= 1  # One less component after merging
            return True
        return False

class Solution:
    def minCostConnectComponents(self, n: int, connections: list[list[int]]) -> int:
        """
        Problem Description:
        Given n nodes labeled from 1 to n, and a list of connections,
        where each connection is represented as [u, v, cost], indicating that
        connecting node u and node v costs 'cost'.
        The goal is to find the minimum cost to connect all nodes such that
        they all belong to the same connected component. If it's impossible
        to connect all nodes, return -1.

        This problem is a classic Minimum Spanning Tree (MST) problem.
        Kruskal's algorithm is used here, which works by sorting all available
        edges by their cost in ascending order and then iteratively adding
        the cheapest edge that connects two previously disconnected components,
        without forming a cycle. A Disjoint Set Union (DSU) data structure
        is used to efficiently manage component connectivity.

        Args:
            n: The number of nodes in the graph, labeled from 1 to n.
            connections: A list of connections, where each connection is [u, v, cost].
                         u and v are 1-indexed node labels, and cost is the cost to connect them.

        Returns:
            The minimum cost to connect all components. Returns -1 if it's impossible
            to connect all components.

        Time Complexity:
        - Sorting `connections`: O(E log E), where E is the number of connections.
        - DSU operations: There are E calls to `find` and `union`. Each operation
          takes nearly constant time amortized O(alpha(N)), where N is the number of nodes
          and alpha is the inverse Ackermann function (which is practically <= 5).
        - Total Time Complexity: O(E log E + E * alpha(N)), effectively O(E log E)
          due to the dominance of the sorting step for typical problem constraints.

        Space Complexity:
        - DSU `parent` array: O(N)
        - DSU `rank` array: O(N)
        - Sorting `connections` (if a copy is made or auxiliary space is used by sort): O(E) for auxiliary space, or O(1) if in-place.
        - Total Space Complexity: O(N + E).
        """

        # Edge case: If there's only one node, it's already connected. No cost is needed.
        if n == 1:
            return 0

        # Kruskal's algorithm requires sorting all edges by their cost in ascending order.
        # This ensures we always consider the cheapest available connections first.
        connections.sort(key=lambda x: x[2])

        # Initialize the Disjoint Set Union (DSU) data structure for n nodes.
        # Each node initially belongs to its own component (set).
        dsu = DSU(n)

        min_total_cost = 0
        
        # Iterate through the sorted connections.
        # We need to add n-1 edges to connect n nodes into a single component.
        # The `dsu.num_components` tracker simplifies checking this condition.
        for u, v, cost in connections:
            # Node labels in the problem are 1-indexed (1 to n),
            # so convert them to 0-indexed (0 to n-1) for array access in DSU.
            u_0_indexed = u - 1
            v_0_indexed = v - 1

            # Attempt to union the sets containing u and v.
            # If dsu.union() returns True, it means u and v were in different components
            # and this edge successfully connected them, thus contributing to the MST
            # without forming a cycle with already chosen edges.
            if dsu.union(u_0_indexed, v_0_indexed):
                min_total_cost += cost
                
                # If all nodes are now connected into a single component (i.e., dsu.num_components == 1),
                # we have found the Minimum Spanning Tree.
                # We can stop early and return the accumulated cost.
                if dsu.num_components == 1:
                    return min_total_cost
        
        # After processing all connections:
        # If `dsu.num_components` is 1, it means all nodes were successfully connected.
        # In this scenario, the `if dsu.num_components == 1` check inside the loop
        # would have already returned `min_total_cost`.
        # If we reach this point, it implies `dsu.num_components > 1`, meaning it's impossible
        # to connect all nodes into a single component using the given connections.
        return -1

```