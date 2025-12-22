```python
class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        """
        Calculates the length of the longest increasing path in a matrix.

        The problem asks to find the longest path where each step moves to an
        adjacent cell (up, down, left, or right) with a strictly greater value.
        This problem can be modeled as finding the longest path in a Directed Acyclic Graph (DAG)
        where nodes are matrix cells and an edge exists from (r1, c1) to (r2, c2)
        if matrix[r2][c2] > matrix[r1][c1] and they are adjacent.

        A Depth-First Search (DFS) with memoization is an effective approach.
        For each cell (r, c), we want to find the length of the longest increasing path
        starting from that cell. Let this be `memo[r][c]`.

        The `dfs(r, c)` function computes `memo[r][c]`:
        1. If `memo[r][c]` is already computed (not 0), return its stored value.
        2. Initialize `current_max_path = 1` (the cell itself is a path of length 1).
        3. For each valid neighbor (nr, nc) such that `matrix[nr][nc] > matrix[r][c]`:
           Recursively call `dfs(nr, nc)` to get the longest path from the neighbor.
           Update `current_max_path = max(current_max_path, 1 + dfs(nr, nc))`.
        4. Store `current_max_path` in `memo[r][c]` and return it.

        The main function iterates through all cells, calling `dfs` for each,
        and keeps track of the maximum path found across all starting points.

        Args:
            matrix: A list of lists of integers representing the input matrix.

        Returns:
            The length of the longest increasing path in the matrix.
        """
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        
        # memo[r][c] will store the length of the longest increasing path
        # starting from matrix[r][c].
        # Initialize with 0s to indicate values not yet computed.
        memo = [[0] * n for _ in range(m)]

        # Directions for movement: (row_change, col_change)
        # (0, 1) -> right, (0, -1) -> left, (1, 0) -> down, (-1, 0) -> up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def dfs(r: int, c: int) -> int:
            """
            Performs a Depth-First Search to find the longest increasing path
            starting from cell (r, c). Memoizes results to avoid recomputation.

            Args:
                r: The current row index.
                c: The current column index.

            Returns:
                The length of the longest increasing path starting at (r, c).
            """
            # If the result for this cell is already computed, return it.
            if memo[r][c] != 0:
                return memo[r][c]

            # The path starting at (r, c) is at least 1 (the cell itself).
            current_max_path = 1

            # Explore all four possible neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check if the neighbor is within matrix bounds
                # and if its value is strictly greater than the current cell's value.
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    # If valid, recursively find the longest path from the neighbor
                    # and add 1 (for the current cell) to it.
                    # Update current_max_path if this new path is longer.
                    current_max_path = max(current_max_path, 1 + dfs(nr, nc))
            
            # Store the computed result in the memoization table before returning.
            memo[r][c] = current_max_path
            return current_max_path

        # Iterate through every cell in the matrix.
        # From each cell, initiate a DFS to find the longest increasing path
        # starting from that cell.
        # Keep track of the overall maximum path found.
        overall_longest_path = 0
        for r in range(m):
            for c in range(n):
                overall_longest_path = max(overall_longest_path, dfs(r, c))

        return overall_longest_path

```