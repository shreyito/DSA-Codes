```python
import collections

class Solution:
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        """
        Finds the length of the longest increasing path in a matrix.

        This problem can be solved using Depth-First Search (DFS) with memoization.
        Each cell (r, c) in the matrix can be the start of an increasing path.
        The length of the longest increasing path starting from (r, c) depends
        on the lengths of the longest increasing paths starting from its valid neighbors
        (neighbors that have a strictly greater value).

        We use a memoization table (dp) to store the computed results for
        each cell. If dp[r][c] is non-zero, it means we have already calculated
        the longest increasing path starting from (r, c), and we can directly
        return that value to avoid redundant computations.

        Args:
            matrix: An m x n integer matrix.

        Returns:
            The length of the longest increasing path.
        """
        if not matrix or not matrix[0]:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        
        # dp[r][c] will store the length of the longest increasing path starting from cell (r, c).
        # Initialize with 0s, which also indicates that the value hasn't been computed yet.
        dp = [[0] * cols for _ in range(rows)]

        # Possible directions to move: right, left, down, up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def dfs(r: int, c: int) -> int:
            """
            Performs a DFS starting from (r, c) to find the longest increasing path.
            Uses memoization to store and retrieve previously computed results.
            """
            # If the value for dp[r][c] is already computed, return it directly.
            if dp[r][c] != 0:
                return dp[r][c]

            # The current cell itself contributes 1 to the path.
            max_path_from_current = 1

            # Explore all four possible directions
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check if the neighbor (nr, nc) is within matrix bounds
                # and if its value is strictly greater than the current cell's value.
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    # Recursively call dfs for the neighbor and add 1 (for the current cell)
                    # Take the maximum of all possible paths from this cell.
                    max_path_from_current = max(max_path_from_current, 1 + dfs(nr, nc))
            
            # Store the computed result in the dp table for future use.
            dp[r][c] = max_path_from_current
            return max_path_from_current

        overall_max_path = 0

        # Iterate through every cell in the matrix.
        # For each cell, perform a DFS to find the longest path starting from it.
        # The overall longest increasing path will be the maximum of all these paths.
        for r in range(rows):
            for c in range(cols):
                overall_max_path = max(overall_max_path, dfs(r, c))
        
        return overall_max_path

# --- Test Cases ---
if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Example from problem description
    matrix1 = [
        [9, 9, 4],
        [6, 6, 8],
        [2, 1, 1]
    ]
    expected1 = 4  # Path example: 1 -> 2 -> 6 -> 9
    result1 = solver.longestIncreasingPath(matrix1)
    print(f"Matrix 1:\n{matrix1}")
    print(f"Longest Increasing Path: {result1}")
    print(f"Expected: {expected1}")
    assert result1 == expected1, f"Test Case 1 Failed: Expected {expected1}, Got {result1}"
    print("-" * 30)

    # Test Case 2: Another example from problem description
    matrix2 = [
        [3, 4, 5],
        [3, 2, 6],
        [2, 2, 1]
    ]
    expected2 = 4  # Path example: 3 -> 4 -> 5 -> 6
    result2 = solver.longestIncreasingPath(matrix2)
    print(f"Matrix 2:\n{matrix2}")
    print(f"Longest Increasing Path: {result2}")
    print(f"Expected: {expected2}")
    assert result2 == expected2, f"Test Case 2 Failed: Expected {expected2}, Got {result2}"
    print("-" * 30)

    # Test Case 3: Single element matrix
    matrix3 = [[1]]
    expected3 = 1
    result3 = solver.longestIncreasingPath(matrix3)
    print(f"Matrix 3:\n{matrix3}")
    print(f"Longest Increasing Path: {result3}")
    print(f"Expected: {expected3}")
    assert result3 == expected3, f"Test Case 3 Failed: Expected {expected3}, Got {result3}"
    print("-" * 30)

    # Test Case 4: Empty matrix
    matrix4 = []
    expected4 = 0
    result4 = solver.longestIncreasingPath(matrix4)
    print(f"Matrix 4:\n{matrix4}")
    print(f"Longest Increasing Path: {result4}")
    print(f"Expected: {expected4}")
    assert result4 == expected4, f"Test Case 4 Failed: Expected {expected4}, Got {result4}"
    print("-" * 30)

    # Test Case 5: Matrix with one row
    matrix5 = [[1, 2, 3, 4, 5]]
    expected5 = 5 # Path: 1 -> 2 -> 3 -> 4 -> 5
    result5 = solver.longestIncreasingPath(matrix5)
    print(f"Matrix 5:\n{matrix5}")
    print(f"Longest Increasing Path: {result5}")
    print(f"Expected: {expected5}")
    assert result5 == expected5, f"Test Case 5 Failed: Expected {expected5}, Got {result5}"
    print("-" * 30)

    # Test Case 6: Matrix with one column
    matrix6 = [[5], [4], [3], [2], [1]]
    expected6 = 1 # No increasing path longer than 1
    result6 = solver.longestIncreasingPath(matrix6)
    print(f"Matrix 6:\n{matrix6}")
    print(f"Longest Increasing Path: {result6}")
    print(f"Expected: {expected6}")
    assert result6 == expected6, f"Test Case 6 Failed: Expected {expected6}, Got {result6}"
    print("-" * 30)

    # Test Case 7: Complex matrix with multiple potential paths
    matrix7 = [
        [7, 8, 9],
        [9, 7, 6],
        [2, 3, 4]
    ]
    expected7 = 4 # Path: 2 -> 3 -> 4 (or 7) -> 8 (or 9)
                  # Example path: 2 -> 3 -> 7 -> 8 -> 9 (length 5)
                  # Ah, wait. The problem description states the second example gives 4.
                  # [3,4,5], [3,2,6], [2,2,1] -> 3->4->5->6 (len 4)
                  # My matrix7: 2->3->4 (len 3), 2->3->7->8->9 (len 5)
                  # 7->8->9 (len 3)
                  # 7->9 (len 2)
                  # Let's verify the path for 2->3->7->8->9:
                  # (2,0) val 2
                  # (2,1) val 3 > 2
                  # (1,1) val 7 > 3
                  # (0,1) val 8 > 7
                  # (0,2) val 9 > 8
                  # This path has length 5.
    result7 = solver.longestIncreasingPath(matrix7)
    print(f"Matrix 7:\n{matrix7}")
    print(f"Longest Increasing Path: {result7}")
    print(f"Expected: {5}") # Corrected expected value based on manual trace
    assert result7 == 5, f"Test Case 7 Failed: Expected 5, Got {result7}"
    print("-" * 30)

    # Test Case 8: All elements same
    matrix8 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    expected8 = 1
    result8 = solver.longestIncreasingPath(matrix8)
    print(f"Matrix 8:\n{matrix8}")
    print(f"Longest Increasing Path: {result8}")
    print(f"Expected: {expected8}")
    assert result8 == expected8, f"Test Case 8 Failed: Expected {expected8}, Got {result8}"
    print("-" * 30)

    print("All test cases passed!")

```