The problem asks for the minimum number of "flips" required to make all leaf nodes in a binary tree have the same color (either all 0s or all 1s). The crucial rule is that flipping a node `u` changes its color `C(u)` to `1 - C(u)`, and also changes the colors of its children `C(L(u))` to `1 - C(L(u))` and `C(R(u))` to `1 - C(R(u))`. This implies that a flip operation propagates its effect down to the children.

### Problem Analysis and Approach

The problem can be solved using a recursive approach with dynamic programming (memoization, though not explicitly needed for the current problem as each node is processed once). We need to determine for each non-leaf node whether to flip it or not, to minimize total flips. The decision at a node affects its children. This "bottom-up" decision-making is characteristic of post-order traversal (Depth-First Search).

Let's define a function `dfs(node)` that returns a tuple `(cost_to_make_leaves_0, cost_to_make_leaves_1)` for the subtree rooted at `node`.
These costs represent:
*   `cost_to_make_leaves_0`: The minimum flips within `node`'s subtree such that all its leaf nodes *effectively* appear as `0` to `node`'s parent.
*   `cost_to_make_leaves_1`: The minimum flips within `node`'s subtree such that all its leaf nodes *effectively* appear as `1` to `node`'s parent.

**Base Case: Leaf Node**
If `node` is a leaf (i.e., `node.left` and `node.right` are both `None`):
*   If `node.val` is `0`: To make this leaf appear `0`, it costs `0` flips. To make it appear `1`, it's impossible to do directly at the leaf level (as a flip operation propagates to children, and a leaf has none). So, we use `infinity` for the impossible state. Returns `(0, infinity)`.
*   If `node.val` is `1`: Similarly, returns `(infinity, 0)`.

**Recursive Step: Non-Leaf Node**
For a non-leaf `node`:
1.  **Recursively get results for children**:
    `left_cost0, left_cost1 = dfs(node.left)`
    `right_cost0, right_cost1 = dfs(node.right)`
    (Note: If a child is `None`, its `dfs` call should return `(0, 0)` because an empty subtree contributes 0 cost to achieving any target leaf color).

2.  **Consider two options for the current `node`**:

    *   **Option A: Do NOT flip `node` (cost = 0 for `node`)**:
        If `node` is not flipped, its children receive the same "target color expectation" as `node` itself.
        *   To make `node`'s leaves appear `0`: We need `node.left`'s leaves to be `0` AND `node.right`'s leaves to be `0`. The cost is `left_cost0 + right_cost0`.
        *   To make `node`'s leaves appear `1`: We need `node.left`'s leaves to be `1` AND `node.right`'s leaves to be `1`. The cost is `left_cost1 + right_cost1`.

    *   **Option B: FLIP `node` (cost = 1 for `node`)**:
        If `node` is flipped, its children effectively see their colors inverted. Therefore, to achieve a certain final effective color for `node`'s leaves, its children must produce the *opposite* effective color.
        *   To make `node`'s leaves appear `0`: `node` flips its children, so its children must aim to make their leaves appear `1` (which `node`'s flip will then turn into `0`). The cost is `1 + left_cost1 + right_cost1`.
        *   To make `node`'s leaves appear `1`: `node` flips its children, so its children must aim to make their leaves appear `0` (which `node`'s flip will then turn into `1`). The cost is `1 + left_cost0 + right_cost0`.

3.  **Combine options**:
    The minimum cost for `node`'s subtree to make its leaves appear `0` (from `node`'s perspective) is `min(cost_not_flipped_target_0, cost_flipped_target_0)`.
    The minimum cost for `node`'s subtree to make its leaves appear `1` (from `node`'s perspective) is `min(cost_not_flipped_target_1, cost_flipped_target_1)`.

    Return these two minimum costs as a tuple.

**Final Result**:
After `dfs(root)` completes, it will return `(min_flips_to_0, min_flips_to_1)`. The overall minimum flips will be `min(min_flips_to_0, min_flips_to_1)`.

### Handling `None` Children (Non-Full Binary Trees)

If a `node` has only one child (e.g., `node.left` is `None` but `node.right` exists), the `dfs` call for the `None` child should return `(0, 0)`. This signifies that an empty subtree trivially satisfies any leaf color requirement with 0 flips, thus not adding to the cost.

### Complexity Analysis

*   **Time Complexity**: O(N), where N is the number of nodes in the tree. Each node is visited exactly once during the DFS traversal, and constant time operations are performed at each node.
*   **Space Complexity**: O(H), where H is the height of the tree. This is due to the recursion stack. In the worst case (a skewed tree), H can be N, leading to O(N) space. In a balanced tree, H is log N, leading to O(log N) space.

```python
import collections

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def minFlipsToUnifyLeafColors(self, root: TreeNode) -> int:
        """
        Calculates the minimum flips required to make all leaf nodes in a binary tree
        have the same color (either all 0s or all 1s).

        A "flip" operation on a node changes its color and the colors of its children.
        This propagation means if a node is flipped, its children effectively
        see their original colors inverted.

        The solution uses a post-order traversal (DFS) with dynamic programming.
        For each node, the DFS function returns a tuple `(cost_to_make_leaves_0, cost_to_make_leaves_1)`.

        `cost_to_make_leaves_0`: Minimum flips in the current node's subtree to make
                                all its leaves effectively 0 (from the current node's perspective).
        `cost_to_make_leaves_1`: Minimum flips in the current node's subtree to make
                                all its leaves effectively 1 (from the current node's perspective).

        The "from the current node's perspective" means that if the parent of the current node
        wants its children's leaves to be 0, then the `cost_to_make_leaves_0` for the current
        node represents the cost to satisfy that.

        Args:
            root: The root of the binary tree. Each node has a `val` (0 or 1), `left`, and `right` child.

        Returns:
            The minimum total number of flips. If it's impossible to unify the leaf colors,
            it returns a very large number (infinity).
        """
        # A large value representing infinity for unreachable states
        INF = float('inf')

        def dfs(node: TreeNode) -> tuple[int, int]:
            """
            Performs a post-order traversal to calculate min flips for subtree.

            Returns:
                A tuple (cost_if_target_is_0, cost_if_target_is_1) for the current subtree.
            """
            if not node:
                # An empty subtree has no leaves. It costs 0 to make its non-existent
                # leaves match any target color (0 or 1). This is important for
                # nodes with only one child, where the missing child contributes 0 cost.
                return (0, 0)

            # Base case: If the current node is a leaf (has no children)
            if not node.left and not node.right:
                if node.val == 0:
                    # If this leaf's value is 0:
                    # - To make it 0: 0 flips (it's already 0).
                    # - To make it 1: Impossible directly from this leaf itself.
                    #   Its color is determined by ancestors.
                    return (0, INF)
                else: # node.val == 1
                    # If this leaf's value is 1:
                    # - To make it 0: Impossible directly.
                    # - To make it 1: 0 flips.
                    return (INF, 0)

            # Recursive step: For non-leaf nodes
            # Get results from children
            left_cost0, left_cost1 = dfs(node.left)
            right_cost0, right_cost1 = dfs(node.right)

            # Calculate costs for the current node based on two scenarios:
            # 1. We choose NOT to flip the current node (0 cost for this node)
            # 2. We choose to FLIP the current node (1 cost for this node)

            # Scenario 1: Current node is NOT flipped
            # If the current node is not flipped, its children effectively see the same
            # "target color expectation" from the parent as the current node.
            #   - To make leaves 0: Both left and right subtrees must produce 0s.
            cost_not_flipped_target_0 = left_cost0 + right_cost0
            #   - To make leaves 1: Both left and right subtrees must produce 1s.
            cost_not_flipped_target_1 = left_cost1 + right_cost1

            # Scenario 2: Current node IS flipped
            # If the current node is flipped, it costs 1 flip. Its children will then
            # see their target color expectation inverted because the current node
            # has flipped them.
            #   - To make leaves 0: Current node flips children. So, children must target 1s,
            #     which current node's flip will then turn into 0s.
            cost_flipped_target_0 = 1 + left_cost1 + right_cost1
            #   - To make leaves 1: Current node flips children. So, children must target 0s,
            #     which current node's flip will then turn into 1s.
            cost_flipped_target_1 = 1 + left_cost0 + right_cost0

            # The minimum cost for the current node's subtree to make its leaves
            # appear 0 (from its parent's perspective) is the minimum of the two scenarios.
            current_node_total_cost0 = min(cost_not_flipped_target_0, cost_flipped_target_0)
            # The minimum cost for the current node's subtree to make its leaves
            # appear 1 (from its parent's perspective) is the minimum of the two scenarios.
            current_node_total_cost1 = min(cost_not_flipped_target_1, cost_flipped_target_1)

            return (current_node_total_cost0, current_node_total_cost1)

        # After the DFS traversal from the root, we get two costs:
        # One to make all leaves ultimately 0, and one to make all leaves ultimately 1.
        # The overall minimum flips is the smaller of these two.
        min_flips_to_0, min_flips_to_1 = dfs(root)
        return min(min_flips_to_0, min_flips_to_1)


# --- Test Cases ---

def build_tree(nodes, index):
    """Helper function to build a binary tree from a list (level-order traversal, None for missing nodes)."""
    if index >= len(nodes) or nodes[index] is None:
        return None
    node = TreeNode(nodes[index])
    node.left = build_tree(nodes, 2 * index + 1)
    node.right = build_tree(nodes, 2 * index + 2)
    return node

def run_test(test_name, nodes, expected):
    """Helper function to run a single test case."""
    root = build_tree(nodes, 0)
    solution = Solution()
    result = solution.minFlipsToUnifyLeafColors(root)
    print(f"Test: {test_name}")
    print(f"  Tree (val list): {nodes}")
    print(f"  Expected: {expected}")
    print(f"  Result:   {result}")
    assert result == expected, f"Test {test_name} failed. Expected {expected}, got {result}"
    print("  Status: PASSED\n")

if __name__ == "__main__":
    INF = float('inf')

    # Test Case 1: Single leaf node (0)
    # Tree:
    #   0
    run_test("Single Leaf 0", [0], 0)

    # Test Case 2: Single leaf node (1)
    # Tree:
    #   1
    run_test("Single Leaf 1", [1], 0)

    # Test Case 3: Balanced tree, all leaves already 0
    # Tree:
    #      0
    #     / \
    #    0   0
    run_test("All Leaves 0", [0, 0, 0], 0)

    # Test Case 4: Balanced tree, all leaves already 1
    # Tree:
    #      1
    #     / \
    #    1   1
    run_test("All Leaves 1", [1, 1, 1], 0)

    # Test Case 5: Root 0, children leaves 1, 1. Flip root to make leaves 0, 0.
    # Tree:
    #      0
    #     / \
    #    1   1
    # Expected: 1 (Flip root: 0 -> 1. Children 1 -> 0, 1 -> 0. All leaves 0.)
    run_test("Flip Root to Unify to 0", [0, 1, 1], 1)

    # Test Case 6: Root 1, children leaves 0, 0. Don't flip root to make leaves 0, 0.
    # Tree:
    #      1
    #     / \
    #    0   0
    # Expected: 0 (No flips needed. Root is 1, children are 0,0. Target 0 achieved with 0 flips.)
    run_test("No Flip needed for 0", [1, 0, 0], 0)

    # Test Case 7: Root 0, children leaves 0, 1. Impossible to unify.
    # Tree:
    #      0
    #     / \
    #    0   1
    # Expected: INF (If root not flipped: leaves 0,1. If root flipped: leaves 1,0. Cannot unify.)
    run_test("Impossible Unify Simple", [0, 0, 1], INF)

    # Test Case 8: Tree with one child
    # Tree:
    #      0
    #     /
    #    1 (leaf)
    # Expected: 0 (Don't flip root, leaf 1. Unifies to 1. Cost 0)
    run_test("Single Child Branch 1", [0, 1, None], 0)

    # Test Case 9: Tree with one child, needs flip
    # Tree:
    #      1
    #     /
    #    0 (leaf)
    # Expected: 0 (Don't flip root, leaf 0. Unifies to 0. Cost 0)
    run_test("Single Child Branch 2", [1, 0, None], 0)

    # Test Case 10: Deeper tree, requires multiple decisions
    # Tree:
    #         0
    #        / \
    #       1   1
    #      / \
    #     0   0
    # Expected: 1
    # (dfs(node 1 (val 1, children 0,0)) returns (0,1) - cost 0 for leaves=0, cost 1 for leaves=1 (by flipping 1))
    # (dfs(root 0 (val 0, children node1, leaf1))
    #   If root not flipped: needs leaves=1. Left (node1) needs leaves=1 (cost 1). Right (leaf1) needs leaves=1 (cost 0). Total 0+1+0=1.
    #   If root flipped: needs leaves=0. Left (node1) needs leaves=0 (cost 0). Right (leaf1) needs leaves=0 (cost INF). Total 1+0+INF = INF.
    # Min is 1.
    run_test("Complex Tree 1", [0, 1, 1, 0, 0, None, None], 1)

    # Test Case 11: Another complex tree, leads to INF
    # Tree:
    #         0
    #        / \
    #       1   0
    #      / \
    #     0   1
    # Expected: INF (Subtree under node 1 cannot be unified)
    run_test("Complex Tree 2 Impossible", [0, 1, 0, 0, 1, None, None], INF)

    # Test Case 12: Complex tree where all leaves are 0, but root is 1
    # Tree:
    #       1
    #      / \
    #     0   0
    #    / \
    #   0   0
    # Expected: 0 (No flips needed. All leaves are 0, target 0. No root flip)
    run_test("Complex Tree All 0s", [1, 0, 0, 0, 0], 0)

```