```python
import collections
from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """
    Solution for the "K-th Smallest Element in a BST" problem.
    """
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        """
        Finds the K-th smallest element in a Binary Search Tree (BST) using
        an iterative in-order traversal.

        An in-order traversal of a BST visits nodes in ascending order of their values.
        By performing an in-order traversal and counting the nodes, we can identify
        the K-th smallest element.

        Args:
            root: The root node of the BST.
            k: The 1-based index of the smallest element to find.

        Returns:
            The value of the K-th smallest element in the BST.
        """
        stack = []
        current = root

        while current or stack:
            # Step 1: Traverse to the leftmost node of the current subtree.
            # Along the way, push all visited nodes onto the stack.
            while current:
                stack.append(current)
                current = current.left

            # Step 2: Pop the top node from the stack.
            # This node is the next smallest element in the in-order sequence.
            current = stack.pop()

            # Step 3: Decrement k. If k becomes 0, we have found our K-th smallest element.
            k -= 1
            if k == 0:
                return current.val

            # Step 4: Move to the right subtree.
            # The next smallest element after the current node will be in its right subtree
            # (or an ancestor if the right subtree is empty).
            current = current.right

        # This part should ideally not be reached if k is a valid index and
        # the BST is not empty. If reached, it implies k was out of bounds
        # or root was None and k was > 0.
        # For competitive programming, problem constraints usually guarantee a valid k.
        raise ValueError("k is out of bounds or tree is empty for given k.")

# --- Time and Space Complexity ---
"""
Time Complexity: O(H + k) in the average case for a balanced tree, and O(N) in the worst case.
- In-order traversal generally takes O(N) time to visit all N nodes.
- However, we stop once the K-th element is found.
- In the iterative approach, we push nodes onto the stack as we go left (at most H nodes).
- Then we pop nodes and potentially move right. We perform these operations for at most 'k' nodes
  until the K-th node is reached.
- 'H' is the height of the tree. In a balanced BST, H = log N. In a skewed BST, H = N.
- Therefore, the time complexity is proportional to the path length to the K-th node plus
  the number of nodes processed along the path, which is at most O(N).
  A more precise bound is O(min(N, H+k)).

Space Complexity: O(H)
- The space used is for the call stack in recursion or the explicit stack in iteration.
- In the worst case, for a skewed tree, the stack can hold up to H nodes, where H is the height
  of the tree.
- For a balanced tree, H = log N. For a completely skewed tree, H = N.
- So, the space complexity is O(H).
"""

# --- Test Cases ---

# Helper function to build a tree from a list (level-order traversal with None for missing children)
def build_tree(nodes: list[Optional[int]]) -> Optional[TreeNode]:
    if not nodes:
        return None
    root = TreeNode(nodes[0])
    q = collections.deque([root])
    i = 1
    while q and i < len(nodes):
        current = q.popleft()

        # Left child
        if i < len(nodes) and nodes[i] is not None:
            current.left = TreeNode(nodes[i])
            q.append(current.left)
        i += 1

        # Right child
        if i < len(nodes) and i < len(nodes) and nodes[i] is not None:
            current.right = TreeNode(nodes[i])
            q.append(current.right)
        i += 1
    return root

def run_tests():
    solver = Solution()

    test_cases = [
        # Example 1 from LeetCode
        ([3, 1, 4, None, 2], 1, 1),
        # Example 2 from LeetCode
        ([5, 3, 6, 2, 4, None, None, 1], 3, 3),
        # Single node tree
        ([1], 1, 1),
        # Two nodes, left child
        ([2, 1], 1, 1),
        ([2, 1], 2, 2),
        # Two nodes, right child (valid BST)
        ([1, None, 2], 1, 1),
        ([1, None, 2], 2, 2),
        # Larger tree
        ([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 6, 7), # In-order: 1,3,4,6,7,8,10,13,14. 6th is 7.
        ([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 1, 1),
        ([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13], 9, 14), # 9th is 14
        # Tree with only right children (skewed)
        ([1, None, 2, None, None, None, 3], 2, 2),
        ([1, None, 2, None, None, None, 3], 3, 3),
    ]

    for nodes, k, expected in test_cases:
        root = build_tree(nodes)
        result = solver.kthSmallest(root, k)
        assert result == expected, f"Tree: {nodes}, k: {k}, Expected: {expected}, Got: {result}"
        print(f"Test Passed: Tree={nodes}, k={k}, Result={result}")

if __name__ == "__main__":
    run_tests()
```