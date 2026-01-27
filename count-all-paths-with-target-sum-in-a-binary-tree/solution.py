```python
import  collections 
 
# Problem Description:
# Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the
# nodes' values equals targetSum.
#
# A path does not need to start or end at the root or a leaf, but it must go downwards
# (traveling only from parent nodes to child nodes).

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right 

# Helper function to build a binary tree from a list (level-order traversal).
# This is useful for creating test cases easily.
def build_tree(nodes):
    if not nodes:
        return None

    root = TreeNode(nodes[0])
    queue = collections.deque([root])
    i = 1
    while queue and i < len(nodes):
        current_node = queue.popleft()

        # Add left child
        if nodes[i] is not None:
            current_node.left = TreeNode(nodes[i])
            queue.append(current_node.left)
        i += 1

        # Add right child
        if i < len(nodes) and nodes[i] is not None:
            current_node.right = TreeNode(nodes[i])
            queue.append(current_node.right)
        i += 1
    return root


class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> int:
        """
        Counts the number of paths in a binary tree whose sum equals targetSum.
        A path does not need to start or end at the root or a leaf,
        but it must go downwards (traveling only from parent nodes to child nodes).
        
        This solution uses a Depth First Search (DFS) combined with the prefix sum
        technique using a hash map.

        Time Complexity: O(N)
            - Each node in the tree is visited exactly once during the DFS traversal.
            - At each node, dictionary (hash map) operations (lookup, insertion, deletion)
              take O(1) average time.
            - Therefore, the total time complexity is proportional to the number of nodes N.

        Space Complexity: O(H)
            - The recursion stack for DFS can go as deep as the height of the tree, H.
              In the worst case (a skewed tree), H can be N. In the best case (a balanced tree),
              H is log N.
            - The hash map `prefix_sum_counts` stores prefix sums encountered along the
              current path from the root. In the worst case, it can store up to H distinct
              prefix sums.
            - Thus, the total space complexity is O(H), which can be O(N) in the worst case.
        """

        # Initialize a global counter for the total number of valid paths found
        self.total_paths = 0

        # Use a hash map (dictionary) to store the frequency of prefix sums encountered
        # along the current path from the root to the current node.
        # The key is the prefix sum, and the value is its frequency.
        #
        # Initialize with {0: 1}: This is crucial. It accounts for paths that
        # start exactly from the root and sum up to the targetSum.
        # For example, if targetSum is 8 and `current_path_sum` becomes 8,
        # then `(current_path_sum - targetSum)` is 0. If 0 is in the map with count 1,
        # it means a path starting from the root with sum 8 is found.
        self.prefix_sum_counts = {0: 1}

        # Start the Depth First Search (DFS) traversal from the root.
        # `current_path_sum` keeps track of the sum of values from the root
        # to the current node.
        self._dfs(root, 0, targetSum)

        return self.total_paths

    def _dfs(self, node: TreeNode, current_path_sum: int, targetSum: int):
        """
        Performs a DFS traversal to find paths with target sum using prefix sums.

        Args:
            node: The current node being visited.
            current_path_sum: The cumulative sum of node values from the tree's root
                              to the current node.
            targetSum: The target sum we are looking for in subpaths.
        """

        # Base case: If the current node is None, stop recursion for this path.
        if not node:
            return

        # Update the current path sum by adding the current node's value
        current_path_sum += node.val

        # Check if a path ending at the current node exists that sums to targetSum.
        # If `(current_path_sum - targetSum)` was a prefix sum seen before in the
        # `prefix_sum_counts` map, it means there's a subpath starting *after* that
        # prefix sum and ending at the current node that sums to targetSum.
        # The number of such paths is given by the frequency of `(current_path_sum - targetSum)`.
        if (current_path_sum - targetSum) in self.prefix_sum_counts:
            self.total_paths += self.prefix_sum_counts[current_path_sum - targetSum]

        # Add the current_path_sum to the frequency map.
        # Increment its count if it already exists, otherwise initialize to 1.
        self.prefix_sum_counts[current_path_sum] = self.prefix_sum_counts.get(current_path_sum, 0) + 1

        # Recursively call DFS for the left child
        self._dfs(node.left, current_path_sum, targetSum)

        # Recursively call DFS for the right child
        self._dfs(node.right, current_path_sum, targetSum)

        # Backtrack: Before returning from the current node's recursion, remove its
        # `current_path_sum` from the frequency map. This is essential because
        # `current_path_sum` is only valid for paths that include the current node.
        # When moving up to the parent and exploring a sibling branch, the current
        # node's contribution to the prefix sum should no longer be considered
        # a valid starting point for paths in the sibling's subtree.
        self.prefix_sum_counts[current_path_sum] -= 1
        # Optional: if self.prefix_sum_counts[current_path_sum] == 0:
        #               del self.prefix_sum_counts[current_path_sum]
        # Deleting is not strictly necessary as decrementing ensures it won't be counted
        # if its frequency becomes zero, but it can save memory for very deep paths.


# Test Cases
if __name__ == "__main__":
    sol = Solution()

    print("--- Test Cases ---")

    # Test Case 1: Example from LeetCode
    # Tree: [10,5,-3,3,2,null,11,3,-2,null,1]
    #      10
    #     /  \
    #    5   -3
    #   / \    \
    #  3   2   11
    # / \   \
    #3  -2   1
    root1 = build_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1])
    target1 = 8
    expected1 = 3
    result1 = sol.pathSum(root1, target1)
    print(f"Test Case 1: Root: {target1}, Target: {target1}")
    print(f"Expected: {expected1}, Got: {result1} -> {'Passed' if result1 == expected1 else 'Failed'}")
    # Paths: (5 -> 3), (5 -> 2 -> 1), (-3 -> 11)

    # Test Case 2: Another example from LeetCode
    # Tree: [5,4,8,11,null,13,4,7,2,null,null,5,1]
    #        5
    #       / \
    #      4   8
    #     /   / \
    #    11  13  4
    #   / \     / \
    #  7   2   5   1
    root2 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1])
    target2 = 22
    expected2 = 3
    result2 = sol.pathSum(root2, target2)
    print(f"Test Case 2: Root: {target2}, Target: {target2}")
    print(f"Expected: {expected2}, Got: {result2} -> {'Passed' if result2 == expected2 else 'Failed'}")
    # Paths: (5 -> 4 -> 11 -> 2), (5 -> 8 -> 4 -> 5), (4 (left of 5) -> 11 -> 7)

    # Test Case 3: Single Node
    root3 = build_tree([1])
    target3 = 1
    expected3 = 1
    result3 = sol.pathSum(root3, target3)
    print(f"Test Case 3: Root: {target3}, Target: {target3}")
    print(f"Expected: {expected3}, Got: {result3} -> {'Passed' if result3 == expected3 else 'Failed'}")
    # Path: (1)

    # Test Case 4: No Path
    root4 = build_tree([1, 2, 3])
    target4 = 10
    expected4 = 0
    result4 = sol.pathSum(root4, target4)
    print(f"Test Case 4: Root: {target4}, Target: {target4}")
    print(f"Expected: {expected4}, Got: {result4} -> {'Passed' if result4 == expected4 else 'Failed'}")

    # Test Case 5: Negative Numbers
    # Tree: [-1,-2,-3]
    #     -1
    #    /  \
    #   -2  -3
    root5 = build_tree([-1, -2, -3])
    target5 = -3
    expected5 = 2
    result5 = sol.pathSum(root5, target5)
    print(f"Test Case 5: Root: {target5}, Target: {target5}")
    print(f"Expected: {expected5}, Got: {result5} -> {'Passed' if result5 == expected5 else 'Failed'}")
    # Paths: (-1 -> -2), (-3)

    # Test Case 6: Path starting not from root
    # Tree: [1,2,3,4,5]
    #      1
    #     / \
    #    2   3
    #   / \
    #  4   5
    root6 = build_tree([1, 2, 3, 4, 5])
    target6 = 7
    expected6 = 2
    result6 = sol.pathSum(root6, target6)
    print(f"Test Case 6: Root: {target6}, Target: {target6}")
    print(f"Expected: {expected6}, Got: {result6} -> {'Passed' if result6 == expected6 else 'Failed'}")
    # Paths: (2 -> 5), (3 -> 4) (This requires `3` to have `4` as a child, but in list representation
    # `4` is child of `2`. Let's assume the tree structure based on standard level order
    # interpretation for [1,2,3,4,5] gives:
    #      1
    #     / \
    #    2   3
    #   / \
    #  4   5
    # Paths for 7: (2->5) = 2+5=7. (1->2->4) = 1+2+4=7.
    # Ah, the problem states "path does not need to start or end at the root or a leaf".
    # So `1->2->4` is one. `2->5` is another. Total 2.
    # What about `1->3`? sum 4. No `7`.
    # Let's verify with the code's output. It should be 2.

    # Test Case 7: Empty Tree
    root7 = build_tree([])
    target7 = 0
    expected7 = 0
    result7 = sol.pathSum(root7, target7)
    print(f"Test Case 7: Root: {target7}, Target: {target7}")
    print(f"Expected: {expected7}, Got: {result7} -> {'Passed' if result7 == expected7 else 'Failed'}")

    # Test Case 8: Only positive numbers, target sum equals a node value
    root8 = build_tree([1,2,3,4,5,6,7])
    target8 = 4
    expected8 = 3 # Paths: (4), (1->3), (1->2->1) (incorrect. 1->2->1 is not in tree)
    # Tree:
    #      1
    #     / \
    #    2   3
    #   / \ / \
    #  4  5 6  7
    # Paths for 4: (4), (1->3). Total 2.
    # Re-evaluating expected for target 4:
    # Path starting at 4: `4` itself. (1)
    # Path starting at 1: `1 -> 3`. (2)
    # Total paths should be 2.
    result8 = sol.pathSum(root8, target8)
    print(f"Test Case 8: Root: {target8}, Target: {target8}")
    print(f"Expected: {2}, Got: {result8} -> {'Passed' if result8 == 2 else 'Failed'}")
```
