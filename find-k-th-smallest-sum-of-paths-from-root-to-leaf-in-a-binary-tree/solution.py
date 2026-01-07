The problem asks us to find the K-th smallest sum among all possible root-to-leaf paths in a binary tree. A root-to-leaf path is a sequence of nodes starting from the root and ending at any leaf node. The sum of a path is the sum of the values of all nodes along that path.

## Problem Description

Given the `root` of a binary tree and an integer `k`, return the `k`-th smallest sum of a root-to-leaf path.

A root-to-leaf path is defined as any path from the root node to any leaf node. A leaf node is a node with no children.

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7], k = 2
Output: 26
Explanation:
Path 1: 3 -> 9. Sum = 3 + 9 = 12
Path 2: 3 -> 20 -> 15. Sum = 3 + 20 + 15 = 38
Path 3: 3 -> 20 -> 7. Sum = 3 + 20 + 7 = 30
The sorted path sums are [12, 30, 38]. The 2nd smallest sum is 30.
Wait, my example explanation is wrong with the given tree structure for Path 2.
Let's fix the tree structure based on standard representation:
      3
     / \
    9  20
      /  \
     15   7

Paths:
1. 3 -> 9. Sum = 12
2. 3 -> 20 -> 15. Sum = 38
3. 3 -> 20 -> 7. Sum = 30
Sorted sums: [12, 30, 38].
The 2nd smallest sum is 30.
```

**Example 2:**

```
Input: root = [1], k = 1
Output: 1
Explanation:
Path 1: 1. Sum = 1
Sorted sums: [1].
The 1st smallest sum is 1.
```

**Constraints:**

*   The number of nodes in the tree is between 1 and 10,000.
*   `-100 <= Node.val <= 100`
*   `1 <= k <= Number of root-to-leaf paths.`

## Approach

The most straightforward approach would be to:
1.  Perform a Depth-First Search (DFS) traversal to find all root-to-leaf path sums.
2.  Store all these sums in a list.
3.  Sort the list.
4.  Return the `(k-1)`-th element from the sorted list.

This approach works but can be inefficient if the number of paths is very large, as sorting takes `O(P log P)` time where `P` is the number of paths. Since `P` can be up to `O(N)` (in a skewed tree), this could be `O(N log N)`.

A more optimized approach, especially when `k` is much smaller than the total number of paths, involves using a min-priority queue (min-heap) of limited size.

**Optimized Approach (using a Max-Heap of size K):**

To find the K-th smallest element efficiently, we can use a max-heap of size `k`.
1.  Initialize an empty max-heap.
2.  Perform a DFS traversal to explore all root-to-leaf paths:
    *   Maintain `current_sum` as we traverse down the tree.
    *   When a leaf node is reached:
        *   If the max-heap's size is less than `k`, push the `current_sum` into the heap.
        *   If the max-heap's size is equal to `k`:
            *   If the `current_sum` is *smaller* than the largest element currently in the heap (the heap's root), then remove the largest element from the heap and push the `current_sum`.
            *   Otherwise (if `current_sum` is greater than or equal to the largest element in the heap), ignore `current_sum` because it's not among the `k` smallest sums.
3.  After the DFS completes, the root of the max-heap will contain the `k`-th smallest path sum.

**Implementing a Max-Heap with Python's `heapq`:**

Python's `heapq` module implements a min-heap. To simulate a max-heap of size `k` for finding the K-th smallest element:
We will store the *negated* path sums in our `heapq` (which is a min-heap).
By pushing `-current_sum` into the min-heap:
*   The `heapq.heappop()` operation will always remove the *smallest negative number* (i.e., the one with the largest absolute value, e.g., `-30` is smaller than `-10`). This corresponds to removing the *largest positive sum*.
*   Therefore, if we push `-current_sum` and ensure the heap's size doesn't exceed `k` by popping, the `k` elements remaining in the min-heap (when converted back to positive) will be the `k` smallest path sums.
*   The smallest element in this min-heap (which is `heap[0]`, the root) will be the *largest negative value* among the `k` elements. When we negate it back (`-heap[0]`), it gives us the *smallest positive value* among the `k` smallest sums, which is exactly the `k`-th smallest sum.

Let's trace:
To find the 3rd smallest sum with `sums = [10, 20, 5, 30, 15]` and `k=3`.
`max_heap_of_k_smallest = []` (Python `heapq` used as min-heap, storing negated values)

1.  `sum = 10`. Push `-10`. Heap: `[-10]`
2.  `sum = 20`. Push `-20`. Heap: `[-20, -10]`
3.  `sum = 5`. Push `-5`. Heap: `[-20, -10, -5]` (Heap size is now `k=3`)
4.  `sum = 30`. Push `-30`. Heap: `[-30, -20, -10, -5]`. Size > `k`. Pop smallest (most negative) which is `-30`. Heap: `[-20, -10, -5]`
5.  `sum = 15`. Push `-15`. Heap: `[-20, -15, -10, -5]`. Size > `k`. Pop smallest (most negative) which is `-20`. Heap: `[-15, -10, -5]`

After all sums processed, `max_heap_of_k_smallest = [-15, -10, -5]`.
The smallest element (root of min-heap) is `max_heap_of_k_smallest[0] = -15`.
The 3rd smallest sum is `-(-15) = 15`. This is correct.

### Time and Space Complexity

*   **Time Complexity:**
    *   The DFS traversal visits each node in the tree exactly once: `O(N)` where `N` is the number of nodes.
    *   For each root-to-leaf path found (let `P` be the number of paths), we perform a `heapq.heappush` and potentially a `heapq.heappop`. These operations take `O(log k)` time because the heap's size is capped at `k`.
    *   In the worst case (a skewed tree), the number of paths `P` can be `O(N)`.
    *   Therefore, the total time complexity is `O(N + P log k)`. Since `P <= N`, this simplifies to `O(N log k)`.
*   **Space Complexity:**
    *   The recursion stack for the DFS traversal can go up to the height of the tree: `O(H)`. In the worst case (skewed tree), `H` can be `O(N)`.
    *   The min-heap stores up to `k` elements: `O(k)`.
    *   Therefore, the total space complexity is `O(H + k)`. In the worst case, this is `O(N + k)`.

```python
import heapq

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def findKthSmallestPathSum(self, root: TreeNode, k: int) -> int:
        if not root:
            # According to constraints, N is between 1 and 10,000, so root will not be None.
            # But it's good practice to handle.
            # If the tree is empty, there are no paths.
            # If k=1 and tree is empty, it's undefined.
            raise ValueError("The tree is empty, no root-to-leaf paths exist.")

        # This min-heap will store negated path sums.
        # By storing negated values, we effectively turn it into a max-heap
        # for positive values. We will limit its size to 'k'.
        # The goal is to keep track of the 'k' smallest path sums seen so far.
        # The largest among these 'k' smallest (which will be the k-th smallest)
        # will be at the root of our max-heap.
        # With a min-heap storing negated values, the element at `heap[0]` will be
        # the largest negative value (closest to zero), which corresponds to the
        # smallest positive value among the 'k' largest negative values we've kept.
        # This is the Kth smallest element logic.
        max_heap_of_k_smallest = [] 

        def dfs(node: TreeNode, current_sum: int):
            if not node:
                return

            current_sum += node.val

            # If it's a leaf node, we have a complete path sum
            if not node.left and not node.right:
                # If the heap size is less than k, just add the path sum.
                # We add the negative sum to simulate a max-heap behavior
                # with Python's min-heap (heapq).
                if len(max_heap_of_k_smallest) < k:
                    heapq.heappush(max_heap_of_k_smallest, -current_sum)
                # If the heap size is k, check if the current_sum is smaller
                # than the current k-th smallest (which is -max_heap_of_k_smallest[0]).
                # If current_sum is smaller, it means -current_sum is larger (less negative)
                # than -max_heap_of_k_smallest[0].
                # This logic is for finding Kth largest.
                # For Kth smallest:
                # We want to keep the k smallest sums.
                # So if new_sum is smaller than the largest in our current k sums (which is -heap[0]),
                # then we replace it.
                # The correct logic for Kth smallest using a min-heap storing negated values:
                # Push -current_sum. If heap size > k, pop the smallest (most negative) element.
                # This removes the largest positive value, thus retaining the k smallest.
                else: # len(max_heap_of_k_smallest) == k
                    # If the current path sum is smaller than the largest of the k sums
                    # we are currently tracking, we replace the largest with the current one.
                    # In our min-heap storing negated values, max_heap_of_k_smallest[0]
                    # is the largest negative value (e.g., -5 if others are -10, -15).
                    # This corresponds to the smallest positive value (5).
                    # To find the Kth smallest:
                    # We compare `current_sum` with `-max_heap_of_k_smallest[0]`.
                    # If `current_sum` is smaller than `-max_heap_of_k_smallest[0]`,
                    # it means `-current_sum` is *larger* than `max_heap_of_k_smallest[0]`.
                    # Then we push `-current_sum` and pop `max_heap_of_k_smallest[0]`.
                    # This is exactly what `heapq.heappushpop` does.
                    if current_sum < -max_heap_of_k_smallest[0]:
                        heapq.heappushpop(max_heap_of_k_smallest, -current_sum)
            else:
                # Continue DFS for left and right children
                dfs(node.left, current_sum)
                dfs(node.right, current_sum)

        dfs(root, 0)

        # After traversing all paths, the heap contains the k largest negative sums.
        # The smallest element in this min-heap (max_heap_of_k_smallest[0])
        # will be the largest negative value (e.g., -5 in [-15, -10, -5]).
        # This largest negative value corresponds to the Kth smallest positive sum.
        if len(max_heap_of_k_smallest) < k:
            # This case means k is larger than the actual number of root-to-leaf paths.
            # Constraints usually guarantee 1 <= k <= number of paths.
            raise ValueError("k is larger than the number of root-to-leaf paths.")

        return -max_heap_of_k_smallest[0]

# --- Test Cases ---
if __name__ == "__main__":
    s = Solution()

    # Helper function to build a tree from a list (level-order traversal)
    def build_tree(nodes):
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

    # Test Case 1: Example from problem description
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    # Paths: (3+9=12), (3+20+15=38), (3+20+7=30)
    # Sorted: [12, 30, 38]
    print(f"Test Case 1 (k=1): {s.findKthSmallestPathSum(root1, 1)}") # Expected: 12
    print(f"Test Case 1 (k=2): {s.findKthSmallestPathSum(root1, 2)}") # Expected: 30
    print(f"Test Case 1 (k=3): {s.findKthSmallestPathSum(root1, 3)}") # Expected: 38

    # Test Case 2: Single node tree
    root2 = build_tree([1])
    # Paths: (1=1)
    # Sorted: [1]
    print(f"Test Case 2 (k=1): {s.findKthSmallestPathSum(root2, 1)}") # Expected: 1

    # Test Case 3: Skewed tree (right)
    root3 = build_tree([1, None, 2, None, None, None, 3, None, None, None, None, None, None, None, 4])
    # Paths: (1+2+3+4=10)
    # Sorted: [10]
    print(f"Test Case 3 (k=1): {s.findKthSmallestPathSum(root3, 1)}") # Expected: 10

    # Test Case 4: Tree with negative values
    root4 = build_tree([10, 5, -3, 3, 2, None, 1])
    # Tree:
    #       10
    #      /  \
    #     5   -3
    #    / \    \
    #   3   2    1
    # Paths:
    # 10 -> 5 -> 3. Sum = 10 + 5 + 3 = 18
    # 10 -> 5 -> 2. Sum = 10 + 5 + 2 = 17
    # 10 -> -3 -> 1. Sum = 10 - 3 + 1 = 8
    # Sorted: [8, 17, 18]
    print(f"Test Case 4 (k=1): {s.findKthSmallestPathSum(root4, 1)}") # Expected: 8
    print(f"Test Case 4 (k=2): {s.findKthSmallestPathSum(root4, 2)}") # Expected: 17
    print(f"Test Case 4 (k=3): {s.findKthSmallestPathSum(root4, 3)}") # Expected: 18

    # Test Case 5: More complex tree
    root5 = build_tree([1,2,3,4,5,6,7])
    # Tree:
    #       1
    #      / \
    #     2   3
    #    / \ / \
    #   4  5 6  7
    # Paths:
    # 1->2->4: 7
    # 1->2->5: 8
    # 1->3->6: 10
    # 1->3->7: 11
    # Sorted: [7, 8, 10, 11]
    print(f"Test Case 5 (k=1): {s.findKthSmallestPathSum(root5, 1)}") # Expected: 7
    print(f"Test Case 5 (k=2): {s.findKthSmallestPathSum(root5, 2)}") # Expected: 8
    print(f"Test Case 5 (k=3): {s.findKthSmallestPathSum(root5, 3)}") # Expected: 10
    print(f"Test Case 5 (k=4): {s.findKthSmallestPathSum(root5, 4)}") # Expected: 11

    # Test Case 6: Tree with only one path, k=1
    root6 = build_tree([5,4,8,11,None,13,4,7,2,None,None,None,1])
    # Path: 5->4->11->7: 27
    # Path: 5->4->11->2: 22
    # Path: 5->8->13: 26
    # Path: 5->8->4->1: 18
    # Sorted: [18, 22, 26, 27]
    print(f"Test Case 6 (k=1): {s.findKthSmallestPathSum(root6, 1)}") # Expected: 18
    print(f"Test Case 6 (k=2): {s.findKthSmallestPathSum(root6, 2)}") # Expected: 22
    print(f"Test Case 6 (k=3): {s.findKthSmallestPathSum(root6, 3)}") # Expected: 26
    print(f"Test Case 6 (k=4): {s.findKthSmallestPathSum(root6, 4)}") # Expected: 27

    # Test Case 7: Minimal value nodes
    root7 = build_tree([-100, -100, -100])
    # Paths: (-100 + -100 = -200), (-100 + -100 = -200)
    # Sorted: [-200, -200]
    print(f"Test Case 7 (k=1): {s.findKthSmallestPathSum(root7, 1)}") # Expected: -200
    print(f"Test Case 7 (k=2): {s.findKthSmallestPathSum(root7, 2)}") # Expected: -200

    # Test Case 8: Max value nodes
    root8 = build_tree([100, 100, 100])
    # Paths: (100+100=200), (100+100=200)
    # Sorted: [200, 200]
    print(f"Test Case 8 (k=1): {s.findKthSmallestPathSum(root8, 1)}") # Expected: 200
    print(f"Test Case 8 (k=2): {s.findKthSmallestPathSum(root8, 2)}") # Expected: 200
```