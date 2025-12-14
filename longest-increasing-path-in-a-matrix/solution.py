```python
class Solution:
    """
    Problem: Longest Increasing Path in a Matrix

    Given an m x n integers matrix, return the length of the longest increasing path in the matrix.

    From each cell, you can either move in four directions: left, right, up, or down.
    You **cannot** move diagonally or move outside the boundary (i.e., no wrap-around).

    Example 1:
    Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
    Output: 4
    Explanation: The longest increasing path is [1, 2, 6, 9].

    Example 2:
    Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
    Output: 4
    Explanation: The longest increasing path is [3, 4, 5, 6]. Moving diagonally is not allowed.

    Example 3:
    Input: matrix = [[1]]
    Output: 1

    Constraints:
    m == matrix.length
    n == matrix[i].length
    1 <= m, n <= 200
    0 <= matrix[i][j] <= 10^9
    """

    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        """
        Calculates the length of the longest increasing path in the given matrix.

        The problem can be modeled as finding the longest path in a Directed Acyclic Graph (DAG).
        Each cell (r, c) is a node. A directed edge exists from (r1, c1) to (r2, c2)
        if matrix[r2][c2] > matrix[r1][c1] and (r2, c2) is an adjacent cell to (r1, c1).
        Since we are always moving to strictly larger values, there are no cycles,
        making it a DAG.

        We can use Depth-First Search (DFS) with Memoization (Dynamic Programming)
        to solve this. For each cell, we compute the length of the longest increasing
        path starting from that cell.

        Args:
            matrix: A 2D list of integers representing the matrix.

        Returns:
            The length of the longest increasing path.
        """
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        # memo[r][c] will store the length of the longest increasing path
        # starting from cell (r, c). Initialize with 0s.
        memo = [[0] * cols for _ in range(rows)]

        # Define the possible movements: up, down, left, right
        # dr: delta row, dc: delta column
        dr = [-1, 1, 0, 0]  # Changes in row for each direction
        dc = [0, 0, -1, 1]  # Changes in column for each direction

        def dfs(r: int, c: int) -> int:
            """
            Performs a DFS starting from cell (r, c) to find the longest
            increasing path. Uses memoization to avoid redundant computations.

            Args:
                r: The current row index.
                c: The current column index.

            Returns:
                The length of the longest increasing path starting from (r, c).
            """
            # If the result for (r, c) is already computed, return it
            if memo[r][c] != 0:
                return memo[r][c]

            # The current cell itself contributes 1 to the path length
            current_max_path = 1

            # Explore all four possible neighbors
            for i in range(4):
                nr, nc = r + dr[i], c + dc[i]

                # Check boundary conditions
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check increasing condition: neighbor's value must be strictly greater
                    if matrix[nr][nc] > matrix[r][c]:
                        # If valid, recursively find the LIP from the neighbor
                        # and add 1 (for the current cell)
                        current_max_path = max(current_max_path, 1 + dfs(nr, nc))

            # Store the computed result in memoization table
            memo[r][c] = current_max_path
            return current_max_path

        overall_max_path = 0
        # Iterate through every cell in the matrix and start a DFS from each
        # This ensures we cover all possible starting points for the LIP
        for r in range(rows):
            for c in range(cols):
                overall_max_path = max(overall_max_path, dfs(r, c))

        return overall_max_path

    """
    Time Complexity: O(R * C)
    Where R is the number of rows and C is the number of columns in the matrix.
    Each cell (r, c) in the matrix will trigger the `dfs` function at most once
    because of memoization (`memo[r][c] != 0` check).
    Inside each `dfs` call, we perform constant work (checking 4 neighbors).
    Therefore, the total time complexity is proportional to the number of cells.

    Space Complexity: O(R * C)
    - `memo` table: O(R * C) space is used to store the results for each cell.
    - Recursion Stack: In the worst-case scenario, the longest path could involve
      all cells in the matrix (e.g., a snake-like path increasing through all cells).
      This would lead to a recursion depth of O(R * C).
    """


# Test Cases
if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Example from problem description
    matrix1 = [
        [9, 9, 4],
        [6, 6, 8],
        [2, 1, 1]
    ]
    print(f"Matrix 1:\n{matrix1}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix1)}")  # Expected: 4
    print("-" * 30)

    # Test Case 2: Another example from problem description
    matrix2 = [
        [3, 4, 5],
        [3, 2, 6],
        [2, 2, 1]
    ]
    print(f"Matrix 2:\n{matrix2}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix2)}")  # Expected: 4
    print("-" * 30)

    # Test Case 3: Single cell matrix
    matrix3 = [[1]]
    print(f"Matrix 3:\n{matrix3}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix3)}")  # Expected: 1
    print("-" * 30)

    # Test Case 4: Empty matrix
    matrix4 = []
    print(f"Matrix 4:\n{matrix4}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix4)}")  # Expected: 0
    print("-" * 30)

    # Test Case 5: Matrix with one row
    matrix5 = [[1, 2, 3, 4, 5]]
    print(f"Matrix 5:\n{matrix5}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix5)}")  # Expected: 5
    print("-" * 30)

    # Test Case 6: Matrix with one column
    matrix6 = [[5], [4], [3], [2], [1]]
    print(f"Matrix 6:\n{matrix6}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix6)}")  # Expected: 1 (only single cells)
    print("-" * 30)

    # Test Case 7: A more complex matrix
    matrix7 = [
        [7, 8, 9],
        [9, 7, 6],
        [2, 1, 3]
    ]
    print(f"Matrix 7:\n{matrix7}")
    # Path: 1 -> 2 -> 7 -> 8 -> 9 (length 5)
    # Path: 1 -> 2 -> 7 -> 9 (length 4)
    # Path: 3 -> 6 -> 7 -> 8 -> 9 (length 5)
    # Path: 3 -> 6 -> 7 -> 9 (length 4)
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix7)}")  # Expected: 5
    print("-" * 30)

    # Test Case 8: All elements are the same
    matrix8 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    print(f"Matrix 8:\n{matrix8}")
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix8)}")  # Expected: 1
    print("-" * 30)

    # Test Case 9: Zig-zag path
    matrix9 = [
        [1, 2, 9],
        [4, 3, 8],
        [5, 6, 7]
    ]
    print(f"Matrix 9:\n{matrix9}")
    # Path: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 (length 9)
    print(f"Longest Increasing Path: {solver.longestIncreasingPath(matrix9)}")  # Expected: 9
    print("-" * 30)
```