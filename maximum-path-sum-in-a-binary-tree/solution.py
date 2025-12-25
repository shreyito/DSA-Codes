```python
import math

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Maximum Path Sum in a Binary Tree
    
    Problem Description:
    A path in a binary tree is defined as any sequence of nodes from some starting node 
    to any node in the tree along the parent-child connections. The path must contain 
    at least one node and does not need to pass through the root.
    
    Given the root of a binary tree, find the maximum path sum.
    
    Example 1:
          1
         / \
        2   3
    Input: root = [1,2,3]
    Output: 6
    Explanation: The optimal path is 2 -> 1 -> 3 with a sum of 2 + 1 + 3 = 6.
    
    Example 2:
         -10
         /   \
        9     20
             /   \
            15    7
    Input: root = [-10,9,20,null,null,15,7]
    Output: 42
    Explanation: The optimal path is 15 -> 20 -> 7 with a sum of 15 + 20 + 7 = 42.
    
    Constraints:
    The number of nodes in the tree is in the range [1, 3 * 10^4].
    -1000 <= Node.val <= 1000
    """

    def maxPathSum(self, root: TreeNode) -> int:
        # Initialize a variable to store the maximum path sum found so far.
        # We use -math.inf to ensure any valid path sum will be greater.
        self.max_sum = -math.inf

        # Helper function to compute the maximum "gain" a node can provide to its parent.
        # This gain is defined as the maximum path sum starting from the current node
        # and going downwards into one of its children (or just including the node itself).
        def max_gain(node: TreeNode) -> int:
            # Base case: If the node is null, it contributes 0 to any path.
            if not node:
                return 0

            # Recursively calculate the maximum gain from the left and right children.
            # We take max(0, ...) because if a child branch yields a negative sum,
            # it's better to not include that branch in the path extending upwards
            # from the current node.
            left_gain = max(0, max_gain(node.left))
            right_gain = max(0, max_gain(node.right))

            # Calculate the path sum *through* the current node that splits.
            # This path includes the current node's value and the maximum gains
            # from both its left and right children. This type of path *cannot*
            # be extended further up the tree (as it "splits" at the current node).
            # However, it is a candidate for the overall maximum path sum.
            current_path_sum_through_node = node.val + left_gain + right_gain
            
            # Update the global maximum path sum found so far.
            self.max_sum = max(self.max_sum, current_path_sum_through_node)

            # Return the maximum gain this node can provide to its parent.
            # This path *cannot* split, it must go up to the parent.
            # So, it's the node's value plus the maximum gain from *one* of its children.
            return node.val + max(left_gain, right_gain)

        # Start the recursion from the root.
        # The return value of max_gain(root) is not directly used for the final answer,
        # as the overall max_sum is updated side-effectually.
        max_gain(root)

        # The self.max_sum now holds the maximum path sum found across all nodes.
        return self.max_sum

    """
    Complexity Analysis:
    
    Time Complexity: O(N)
    - Each node in the tree is visited exactly once by the `max_gain` recursive function.
    - At each node, a constant amount of work is performed ( vài arithmetic operations, comparisons).
    - Therefore, the total time complexity is directly proportional to the number of nodes N in the tree.
    
    Space Complexity: O(H)
    - H is the height of the binary tree.
    - The space complexity is determined by the maximum depth of the recursion stack.
    - In the worst-case scenario (a skewed tree, e.g., a linked list), the height H can be equal to N, 
      leading to O(N) space complexity.
    - In the best-case scenario (a perfectly balanced tree), the height H is log N, 
      leading to O(log N) space complexity.
    """

# --- Test Cases ---
def build_tree(nodes):
    """
    Helper function to build a binary tree from a list representation.
    None in the list represents a null node.
    """
    if not nodes:
        return None
    
    root = TreeNode(nodes[0])
    queue = [root]
    i = 1
    while queue and i < len(nodes):
        current = queue.pop(0)
        
        if nodes[i] is not None:
            current.left = TreeNode(nodes[i])
            queue.append(current.left)
        i += 1
        
        if i < len(nodes) and nodes[i] is not None:
            current.right = TreeNode(nodes[i])
            queue.append(current.right)
        i += 1
    return root

if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Example from problem description
    # Tree:
    #       1
    #      / \
    #     2   3
    root1 = build_tree([1, 2, 3])
    print(f"Test Case 1: Max Path Sum = {solver.maxPathSum(root1)} (Expected: 6)")
    assert solver.maxPathSum(root1) == 6, "Test Case 1 Failed"

    # Test Case 2: Example from problem description
    # Tree:
    #        -10
    #        /   \
    #       9     20
    #            /   \
    #           15    7
    root2 = build_tree([-10, 9, 20, None, None, 15, 7])
    print(f"Test Case 2: Max Path Sum = {solver.maxPathSum(root2)} (Expected: 42)")
    assert solver.maxPathSum(root2) == 42, "Test Case 2 Failed"

    # Test Case 3: Single node tree
    # Tree:
    #       -3
    root3 = build_tree([-3])
    print(f"Test Case 3: Max Path Sum = {solver.maxPathSum(root3)} (Expected: -3)")
    assert solver.maxPathSum(root3) == -3, "Test Case 3 Failed"

    # Test Case 4: Tree with all negative values, max is the largest single node value
    # Tree:
    #       -1
    #      /  \
    #     -2  -3
    root4 = build_tree([-1, -2, -3])
    print(f"Test Case 4: Max Path Sum = {solver.maxPathSum(root4)} (Expected: -1)")
    assert solver.maxPathSum(root4) == -1, "Test Case 4 Failed"

    # Test Case 5: Complex tree with mixed positive and negative
    # Tree:
    #         5
    #        / \
    #       4   8
    #      /   / \
    #     11  13  4
    #    / \     / \
    #   7   2   1   -5
    root5 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    # The path 7->11->4->5->8->13 has sum 7+11+4+5+8+13 = 48
    # The path 2->11->4->5->8->13 has sum 2+11+4+5+8+13 = 43
    # The path 1->4->8->5 has sum 1+4+8+5 = 18
    # The path 7->11->4 (from left branch) gives 22
    # The path 13->8->4 (from right branch) gives 25
    # Longest: 7 -> 11 -> 4 -> 5 -> 8 -> 13 = 48
    print(f"Test Case 5: Max Path Sum = {solver.maxPathSum(root5)} (Expected: 48)")
    assert solver.maxPathSum(root5) == 48, "Test Case 5 Failed"
    
    # Test Case 6: Path not through root, entirely in one subtree
    # Tree:
    #          -5
    #         /   \
    #        -10   2
    #             / \
    #            3   4
    root6 = build_tree([-5, -10, 2, None, None, 3, 4])
    # Path 3 -> 2 -> 4 has sum 3+2+4 = 9
    print(f"Test Case 6: Max Path Sum = {solver.maxPathSum(root6)} (Expected: 9)")
    assert solver.maxPathSum(root6) == 9, "Test Case 6 Failed"
    
    # Test Case 7: Simple positive values
    # Tree:
    #      10
    #     /  \
    #    2    8
    root7 = build_tree([10, 2, 8])
    print(f"Test Case 7: Max Path Sum = {solver.maxPathSum(root7)} (Expected: 20)")
    assert solver.maxPathSum(root7) == 20, "Test Case 7 Failed"
    
    # Test Case 8: All zeroes
    # Tree:
    #      0
    #     / \
    #    0   0
    root8 = build_tree([0, 0, 0])
    print(f"Test Case 8: Max Path Sum = {solver.maxPathSum(root8)} (Expected: 0)")
    assert solver.maxPathSum(root8) == 0, "Test Case 8 Failed"
```