```python
import collections

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def rightSideView(self, root: TreeNode) -> list[int]:
        """
        Given the root of a binary tree, imagine yourself standing on the right side of it,
        return the values of the nodes you can see ordered from top to bottom.

        This solution uses a Depth-First Search (DFS) approach. It traverses the tree
        prioritizing the right child first. When a node is encountered at a new level
        (one that hasn't been added to the result list yet), its value is guaranteed
        to be the rightmost visible node for that level, because we always visit
        the right child before the left child.
        """
        if not root:
            return []

        # result will store the rightmost node's value for each level.
        # Its index will correspond to the level depth.
        result = []

        def dfs(node: TreeNode, level: int):
            # Base case: if the node is None, stop recursion for this path.
            if not node:
                return

            # If the current level is equal to the length of the result list,
            # it means we are visiting a node at a new depth for the first time.
            # Since we traverse right first, this node is guaranteed to be the
            # rightmost node visible at this particular level.
            if level == len(result):
                result.append(node.val)
            
            # Recursively call for the right child first.
            # This ensures that for any given level, the rightmost node is processed
            # before any node further to its left at the same level.
            dfs(node.right, level + 1)

            # Then, recursively call for the left child.
            # If a right node was already added for this level, the left node
            # (if it's not farther right than the previously added node) will
            # not overwrite it due to the 'if level == len(result)' condition.
            dfs(node.left, level + 1)

        # Start the DFS traversal from the root at level 0.
        dfs(root, 0)
        
        return result

    def rightSideView_BFS(self, root: TreeNode) -> list[int]:
        """
        Alternative solution using Breadth-First Search (BFS) / Level Order Traversal.
        For each level, the last node processed in the queue will be the rightmost node.
        """
        if not root:
            return []

        result = []
        # Use a deque for efficient popping from the left and appending to the right.
        queue = collections.deque([root])

        while queue:
            level_size = len(queue)
            # This variable will store the value of the rightmost node for the current level.
            # It gets updated with each node popped, so the last update for a level
            # will be the actual rightmost node.
            current_level_rightmost_val = None

            for _ in range(level_size):
                node = queue.popleft()
                current_level_rightmost_val = node.val # Update with current node's value

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            # After processing all nodes at the current level, add the
            # rightmost value encountered to the result.
            result.append(current_level_rightmost_val)
        
        return result


# --- Time and Space Complexity ---
# For the DFS Solution:
# Time Complexity: O(N)
#   - Each node in the binary tree is visited exactly once during the DFS traversal.
#     N is the total number of nodes in the tree.
# Space Complexity: O(H)
#   - In the worst case, the recursion stack depth can be equal to the height (H) of the tree.
#   - For a skewed tree (e.g., a linked list), H can be N, leading to O(N) space.
#   - For a balanced tree, H is log N, leading to O(log N) space.

# For the BFS Solution:
# Time Complexity: O(N)
#   - Each node is enqueued and dequeued exactly once.
# Space Complexity: O(W)
#   - In the worst case, the queue can hold all nodes at the widest level of the tree.
#   - For a complete binary tree, the maximum width (W) can be N/2 (the last level),
#     leading to O(N) space.
#   - For a skewed tree, W is 1, leading to O(1) space.

# --- Test Cases ---

def build_tree(nodes: list[int | None]) -> TreeNode | None:
    """
    Helper function to build a binary tree from a list (level order traversal with nulls).
    Example: [1,2,3,null,5,null,4]
    """
    if not nodes:
        return None
    
    root = TreeNode(nodes[0])
    queue = collections.deque([root])
    i = 1
    while queue and i < len(nodes):
        current = queue.popleft()

        if nodes[i] is not None:
            current.left = TreeNode(nodes[i])
            queue.append(current.left)
        i += 1

        if i < len(nodes) and nodes[i] is not None:
            current.right = TreeNode(nodes[i])
            queue.append(current.right)
        i += 1
    return root

# Create an instance of the Solution class
s = Solution()

print("--- Test Cases (DFS Solution) ---")

# Test Case 1: Example from problem description
# Tree:
#      1
#     / \
#    2   3
#     \   \
#      5   4
root1 = build_tree([1, 2, 3, None, 5, None, 4])
print(f"Test Case 1: Tree: [1,2,3,null,5,null,4], Right Side View: {s.rightSideView(root1)}") # Expected: [1, 3, 4]

# Test Case 2: Simple tree
# Tree:
#      1
#     /
#    2
root2 = build_tree([1, 2])
print(f"Test Case 2: Tree: [1,2], Right Side View: {s.rightSideView(root2)}") # Expected: [1, 2]

# Test Case 3: Right-skewed tree
# Tree:
#      1
#       \
#        2
#         \
#          3
root3 = build_tree([1, None, 2, None, None, None, 3])
print(f"Test Case 3: Tree: [1,null,2,null,null,null,3], Right Side View: {s.rightSideView(root3)}") # Expected: [1, 2, 3]

# Test Case 4: Left-skewed tree
# Tree:
#      1
#     /
#    2
#   /
#  3
root4 = build_tree([1, 2, None, 3])
print(f"Test Case 4: Tree: [1,2,null,3], Right Side View: {s.rightSideView(root4)}") # Expected: [1, 2, 3]

# Test Case 5: Single node tree
# Tree:
#      1
root5 = build_tree([1])
print(f"Test Case 5: Tree: [1], Right Side View: {s.rightSideView(root5)}") # Expected: [1]

# Test Case 6: Empty tree
root6 = build_tree([])
print(f"Test Case 6: Tree: [], Right Side View: {s.rightSideView(root6)}") # Expected: []

# Test Case 7: Complex balanced tree
# Tree:
#        1
#       / \
#      2   3
#     / \ / \
#    4  5 6  7
root7 = build_tree([1, 2, 3, 4, 5, 6, 7])
print(f"Test Case 7: Tree: [1,2,3,4,5,6,7], Right Side View: {s.rightSideView(root7)}") # Expected: [1, 3, 7]

# Test Case 8: Tree with no right children except root
# Tree:
#      1
#     /
#    2
#   /
#  3
root8 = build_tree([1, 2, None, 3, None])
print(f"Test Case 8: Tree: [1,2,null,3,null], Right Side View: {s.rightSideView(root8)}") # Expected: [1, 2, 3]

# Test Case 9: Tree with only left children, but some levels have a rightmost view
# Tree:
#      1
#     / \
#    2   3
#   / \
#  4   5
root9 = build_tree([1, 2, 3, 4, 5])
print(f"Test Case 9: Tree: [1,2,3,4,5], Right Side View: {s.rightSideView(root9)}") # Expected: [1, 3, 5]


print("\n--- Test Cases (BFS Solution) ---")
# Re-run a few tests with BFS to ensure consistency

print(f"Test Case 1 BFS: Tree: [1,2,3,null,5,null,4], Right Side View: {s.rightSideView_BFS(root1)}") # Expected: [1, 3, 4]
print(f"Test Case 3 BFS: Tree: [1,null,2,null,null,null,3], Right Side View: {s.rightSideView_BFS(root3)}") # Expected: [1, 2, 3]
print(f"Test Case 7 BFS: Tree: [1,2,3,4,5,6,7], Right Side View: {s.rightSideView_BFS(root7)}") # Expected: [1, 3, 7]
print(f"Test Case 6 BFS: Tree: [], Right Side View: {s.rightSideView_BFS(root6)}") # Expected: []
```