```python
class Solution:
    """
    Problem: Longest Increasing Path in a Matrix

    Given an m x n integers matrix, return the length of the longest increasing path in the matrix.

    From each cell, you can either move in four directions: left, right, up, or down.
    You cannot move diagonally or move outside the boundary (i.e., wrap around the edges).
    An increasing path means each subsequent cell in the path must have a strictly greater value than the current cell.

    This problem can be effectively solved using Depth-First Search (DFS) combined with memoization (dynamic programming).
    Each cell in the matrix can be the start of a potential longest increasing path.
    We can compute the length of the longest increasing path starting from each cell using DFS.
    To avoid redundant computations, we store the result for each cell in a memoization table.
    """

    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        # Handle edge cases for empty or malformed matrix
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])

        # memo[r][c] will store the length of the longest increasing path
        # starting from cell (r, c). Initialize with 0 to indicate not computed.
        memo = [[0] * n for _ in range(m)]

        # Define possible directions for movement: (row_offset, col_offset)
        # Up, Down, Left, Right
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def dfs(r: int, c: int) -> int:
            """
            Performs Depth-First Search to find the length of the longest increasing path
            starting from cell (r, c). Memoizes results to avoid recomputation.

            Args:
                r: The current row index.
                c: The current column index.

            Returns:
                The length of the longest increasing path starting from (r, c).
            """
            # If the result for (r, c) is already computed, return it directly
            if memo[r][c] != 0:
                return memo[r][c]

            # The path starting from (r, c) itself has a length of at least 1
            max_current_path = 1

            # Explore all four possible directions (neighbors)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc  # Calculate coordinates of the neighbor

                # Check if the neighbor (nr, nc) is within the matrix bounds
                if 0 <= nr < m and 0 <= nc < n:
                    # Check if the neighbor's value is strictly greater than the current cell's value.
                    # This is the increasing path condition.
                    if matrix[nr][nc] > matrix[r][c]:
                        # If the condition is met, recursively call DFS for the neighbor.
                        # The path length through this neighbor would be 1 (for current cell)
                        # plus the longest increasing path starting from the neighbor.
                        max_current_path = max(max_current_path, 1 + dfs(nr, nc))
            
            # Store the computed result in the memoization table before returning
            memo[r][c] = max_current_path
            return max_current_path

        overall_max_path_length = 0

        # Iterate through every cell in the matrix.
        # For each cell, perform DFS to find the longest increasing path starting from it.
        # The overall maximum will be the maximum of all such paths found across all starting cells.
        for r in range(m):
            for c in range(n):
                overall_max_path_length = max(overall_max_path_length, dfs(r, c))

        return overall_max_path_length


# --- Time and Space Complexity ---
"""
Time Complexity: O(m * n)
- The algorithm iterates through each cell of the matrix once in the outer loops (m * n cells).
- For each cell (r, c), the `dfs(r, c)` function is called.
- Due to memoization, `dfs(r, c)` computes its result only once for any given cell. Subsequent calls for the same cell
  will return the memoized value in O(1) time.
- Inside `dfs`, for a cell that hasn't been computed, we check its 4 neighbors. This involves constant work (bounds check, value comparison)
  and recursive calls that eventually hit memoized values or base cases.
- Therefore, each cell's computation contributes a constant amount of work after its initial visit, making the total time
  complexity proportional to the number of cells in the matrix.

Space Complexity: O(m * n)
- `memo` table: An `m x n` matrix is used to store the results of subproblems, contributing O(m * n) space.
- Recursion Stack: In the worst-case scenario, the longest increasing path could visit every cell in the matrix (e.g., a "snake" path through all cells),
  leading to a recursion depth of O(m * n). This stack space contributes O(m * n).
- Total space complexity is dominated by these two factors, resulting in O(m * n).
"""

# --- Test Cases ---
if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Example from problem description
    matrix1 = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
    expected1 = 4  # Path: 1 -> 2 -> 6 -> 9
    result1 = solver.longestIncreasingPath(matrix1)
    print(f"Matrix: {matrix1}")
    print(f"Longest Increasing Path: {result1}")
    print(f"Expected: {expected1}")
    assert result1 == expected1
    print("-" * 30)

    # Test Case 2: Another example from problem description
    matrix2 = [[3, 4, 5], [3, 2, 6], [2, 2, 1]]
    expected2 = 4  # Path: 2 -> 3 -> 4 -> 5 or 3 -> 4 -> 5 -> 6
    result2 = solver.longestIncreasingPath(matrix2)
    print(f"Matrix: {matrix2}")
    print(f"Longest Increasing Path: {result2}")
    print(f"Expected: {expected2}")
    assert result2 == expected2
    print("-" * 30)

    # Test Case 3: Single cell matrix
    matrix3 = [[1]]
    expected3 = 1
    result3 = solver.longestIncreasingPath(matrix3)
    print(f"Matrix: {matrix3}")
    print(f"Longest Increasing Path: {result3}")
    print(f"Expected: {expected3}")
    assert result3 == expected3
    print("-" * 30)

    # Test Case 4: Matrix with all same elements
    matrix4 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    expected4 = 1
    result4 = solver.longestIncreasingPath(matrix4)
    print(f"Matrix: {matrix4}")
    print(f"Longest Increasing Path: {result4}")
    print(f"Expected: {expected4}")
    assert result4 == expected4
    print("-" * 30)

    # Test Case 5: Matrix with strictly increasing diagonal path
    matrix5 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected5 = 9  # Path: 1 -> 2 -> 3 -> 6 -> 9 etc. (any path of length 9)
    result5 = solver.longestIncreasingPath(matrix5)
    print(f"Matrix: {matrix5}")
    print(f"Longest Increasing Path: {result5}")
    print(f"Expected: {expected5}")
    assert result5 == expected5
    print("-" * 30)

    # Test Case 6: Empty matrix
    matrix6 = []
    expected6 = 0
    result6 = solver.longestIncreasingPath(matrix6)
    print(f"Matrix: {matrix6}")
    print(f"Longest Increasing Path: {result6}")
    print(f"Expected: {expected6}")
    assert result6 == expected6
    print("-" * 30)

    # Test Case 7: Matrix with empty row
    matrix7 = [[]]
    expected7 = 0
    result7 = solver.longestIncreasingPath(matrix7)
    print(f"Matrix: {matrix7}")
    print(f"Longest Increasing Path: {result7}")
    print(f"Expected: {expected7}")
    assert result7 == expected7
    print("-" * 30)

    # Test Case 8: Larger matrix with complex path
    matrix8 = [
        [7, 8, 9],
        [9, 7, 6],
        [2, 3, 4],
        [1, 5, 3]
    ]
    # One possible path: 1 -> 2 -> 3 -> 4 -> 6 -> 7 -> 8 -> 9 (length 8)
    expected8 = 8
    result8 = solver.longestIncreasingPath(matrix8)
    print(f"Matrix: {matrix8}")
    print(f"Longest Increasing Path: {result8}")
    print(f"Expected: {expected8}")
    assert result8 == expected8
    print("-" * 30)

    print("\nAll test cases passed!")
```