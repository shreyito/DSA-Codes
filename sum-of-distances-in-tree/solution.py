```python
class Solution:
    """
    Problem: Sum of Distances in Tree

    An undirected tree with N nodes labeled 0 to N-1 is given.
    The tree is represented by an array of edges, where edges[i] = [u, v]
    means there is an edge between node u and node v.

    Return an array `ans` of length N, where `ans[i]` is the sum of
    distances between node `i` and all other nodes in the tree.

    Example 1:
    Input: n = 6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]
    Output: [8,12,6,10,10,10]
    Explanation: The tree is:
        0
       / \
      1   2
         /|\
        3 4 5
    For node 0: sum_dist = d(0,1)+d(0,2)+d(0,3)+d(0,4)+d(0,5) = 1+1+2+2+2 = 8
    For node 1: sum_dist = d(1,0)+d(1,2)+d(1,3)+d(1,4)+d(1,5) = 1+2+3+3+3 = 12
    And so on.

    Example 2:
    Input: n = 2, edges = [[0,1]]
    Output: [1,1]

    Example 3:
    Input: n = 1, edges = []
    Output: [0]
    """

    def sumOfDistancesInTree(self, n: int, edges: list[list[int]]) -> list[int]:
        """
        Calculates the sum of distances from each node to all other nodes in a tree.

        The solution uses two Depth First Searches (DFS):

        1.  DFS1 (Post-order traversal, from leaves up to root):
            -   Starts from an arbitrary root (e.g., node 0).
            -   For each node `u`, it calculates:
                -   `count[u]`: The total number of nodes in the subtree rooted at `u`
                                (including `u` itself).
                -   `ans[u]`: The sum of distances from `u` to all nodes *within its own subtree*.
                                (This `ans[u]` is temporary and only valid for the subtree).
            -   Formula for `count[u]`: `count[u] = 1 + sum(count[v] for v in children of u)`
            -   Formula for `ans[u]`: `ans[u] = sum(ans[v] + count[v] for v in children of u)`
                                        (Each node in `v`'s subtree is 1 step further from `u`
                                         than it is from `v`).

        2.  DFS2 (Pre-order traversal, from root down to leaves):
            -   Uses the `ans[root]` calculated in DFS1 (which is the correct total sum for the root).
            -   For any node `u` and its child `v`, it derives `ans[v]` from `ans[u]`.
            -   When moving the "root" from `u` to `v`:
                -   Nodes in `v`'s subtree (total `count[v]`) become 1 unit *closer* to `v`.
                    Their contribution to the total sum for `v` decreases by `count[v]`.
                -   Nodes *outside* `v`'s subtree (total `N - count[v]`) become 1 unit *further* from `v`.
                    Their contribution to the total sum for `v` increases by `N - count[v]`.
            -   Formula for `ans[v]`: `ans[v] = ans[u] - count[v] + (n - count[v])`

        Args:
            n: The number of nodes in the tree.
            edges: A list of lists representing the edges of the tree.

        Returns:
            A list of integers `ans` where `ans[i]` is the sum of
            distances from node `i` to all other nodes.
        """
        # 1. Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        # ans[i] will store the final sum of distances for node i
        ans = [0] * n
        # count[i] will store the number of nodes in the subtree rooted at i (including i)
        count = [0] * n

        # DFS1: Post-order traversal to calculate count[u] and initial ans[u]
        # (sum of distances to nodes in its own subtree).
        def dfs1(u, parent):
            count[u] = 1  # Node u itself counts for 1
            # ans[u] will accumulate sum of distances to nodes in its subtree
            for v in adj[u]:
                if v == parent:
                    continue
                dfs1(v, u)
                count[u] += count[v]
                # When moving from child v to parent u,
                # all nodes in v's subtree are 1 step further from u than from v.
                # So, the sum of distances from u to v's subtree is (ans[v] + count[v]).
                ans[u] += ans[v] + count[v]

        # DFS2: Pre-order traversal to propagate the sums of distances from parent to children.
        # This uses the already computed ans[0] (total sum for the root) and
        # count array from DFS1 to calculate the correct total sums for all other nodes.
        def dfs2(u, parent):
            for v in adj[u]:
                if v == parent:
                    continue
                # When moving the perspective from parent 'u' to child 'v':
                # 1. Nodes in 'v's subtree (total count[v]) become 1 unit *closer* to 'v'.
                #    So, their contribution to ans[v] decreases by count[v].
                # 2. Nodes NOT in 'v's subtree (total n - count[v]) become 1 unit *further* from 'v'.
                #    So, their contribution to ans[v] increases by (n - count[v]).
                ans[v] = ans[u] - count[v] + (n - count[v])
                dfs2(v, u)

        # Start the DFS traversals from node 0 (arbitrary root)
        # -1 is used as a placeholder for a non-existent parent for the root node.
        dfs1(0, -1)
        dfs2(0, -1)

        return ans

```
---
### Time and Space Complexity Analysis

*   **Time Complexity:**
    *   **Building the adjacency list:** We iterate through `n-1` edges, performing constant time operations for each. This takes `O(n)` time.
    *   **DFS1:** This is a standard Depth First Search. Each node is visited exactly once, and each edge is traversed twice (once down, once up). Therefore, DFS1 takes `O(n)` time.
    *   **DFS2:** Similar to DFS1, each node is visited exactly once, and each edge is traversed twice. Therefore, DFS2 takes `O(n)` time.
    *   **Total Time Complexity:** `O(n) + O(n) + O(n) = O(n)`. The solution scales linearly with the number of nodes in the tree.

*   **Space Complexity:**
    *   **Adjacency list (`adj`):** Stores `n` lists. In total, it stores `2 * (n-1)` entries for the edges (since each edge [u, v] is stored as `v` in `adj[u]` and `u` in `adj[v]`). This takes `O(n)` space.
    *   **`ans` array:** Stores `n` integers. This takes `O(n)` space.
    *   **`count` array:** Stores `n` integers. This takes `O(n)` space.
    *   **Recursion Stack:** In the worst-case scenario (a skewed tree, like a linked list), the recursion depth can go up to `n`. This takes `O(n)` space.
    *   **Total Space Complexity:** `O(n) + O(n) + O(n) + O(n) = O(n)`. The solution scales linearly with the number of nodes.

---
### Test Cases

```python
import unittest

class TestSumOfDistancesInTree(unittest.TestCase):

    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        # Example from problem description
        n = 6
        edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]
        expected = [8,12,6,10,10,10]
        self.assertEqual(self.solution.sumOfDistancesInTree(n, edges), expected)

    def test_example_2(self):
        # Example from problem description (simple path)
        n = 2
        edges = [[0,1]]
        expected = [1,1]
        self.assertEqual(self.solution.sumOfDistancesInTree(n, edges), expected)

    def test_example_3(self):
        # Single node tree
        n = 1
        edges = []
        expected = [0]
        self.assertEqual(self.solution.sumOfDistancesInTree(n, edges), expected)

    def test_path_graph_3_nodes(self):
        # Path graph: 0 - 1 - 2
        n = 3
        edges = [[0,1],[1,2]]
        # Node 0: d(0,1)+d(0,2) = 1+2 = 3
        # Node 1: d(1,0)+d(1,2) = 1+1 = 2
        # Node 2: d(2,0)+d(2,1) = 2+1 = 3
        expected = [3,2,3]
        self.assertEqual(self.solution.sumOfDistancesInTree(n, edges), expected)

    def test_star_graph_4_nodes(self):
        # Star graph: 1 is center, connected to 0, 2, 3
        #   0
        #   |
        # 3-1-2
        n = 4
        edges = [[1,0],[1,2],[1,3]]
        # Node 0: d(0,1)+d(0,2)+d(0,3) = 1+2+2 = 5
        # Node 1: d(1,0)+d(1,2)+d(1,3) = 1+1+1 = 3
        # Node 2: d(2,0)+d(2,1)+d(2,3) = 2+1+2 = 5
        # Node 3: d(3,0)+d(3,1)+d(3,2) = 2+1+2 = 5
        expected = [5,3,5,5]
        self.assertEqual(self.solution.sumOfDistancesInTree(n, edges), expected)

    def test_general_tree_5_nodes(self):
        # Tree:
        #   0
        #   |
        #   1
        #  / \
        # 2   3
        #     |
        #     4
        n = 5
        edges = [[0,1],[1,2],[1,3],[3,4]]
        # Node 0: d(0,1)+d(0,2)+d(0,3)+d(0,4) = 1+2+2+3 = 8
        # Node 1: d(1,0)+d(1,2)+d(1,3)+d(1,4) = 1+1+1+2 = 5
        # Node 2: d(2,0)+d(2,1)+d(2,3)+d(2,4) = 2+1+2+3 = 8
        # Node 3: d(3,0)+d(3,1)+d(3,2)+d(3,4) = 2+1+2+1 = 6
        # Node 4: d(4,0)+d(4,1)+d(4,2)+d(4,3) = 3+2+3+1 = 9
        expected = [8,5,8,6,9]
        self.assertEqual(self.solution.sumOfDistancesInTree(n, edges), expected)

# To run the tests, uncomment the following block:
# if __name__ == '__main__':
#     unittest.main(argv=['first-arg-is-ignored'], exit=False)

```