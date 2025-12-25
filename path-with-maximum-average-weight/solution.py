```python
import math

class Solution:
    def maxAveragePath(self, grid: list[list[int]]) -> float:
        """
        Calculates the maximum average weight of a path from the top-left cell (0,0)
        to the bottom-right cell (R-1, C-1) in a given grid.
        Movement is restricted to only 'right' or 'down' steps.

        Problem Description:
        Given a 2D grid of integers `grid[R][C]`, where `grid[i][j]` represents
        the weight of the cell (i,j). We need to find a path starting from (0,0)
        and ending at (R-1, C-1) such that the average of the weights of all cells
        along this path is maximized.
        A path can only move from a cell (i,j) to (i+1,j) (down) or (i,j+1) (right).

        Key Insight:
        For any path from (0,0) to (R-1, C-1) using only 'right' and 'down' moves,
        the total number of cells in the path is always constant. This constant
        number of cells is `(R-1 - 0) + (C-1 - 0) + 1 = R + C - 1`.
        Let `k = R + C - 1` be the number of cells in any valid path.
        If a path has a total sum of weights `S`, its average weight is `S / k`.
        Since `k` is constant for all valid paths, maximizing the average `S / k`
        is equivalent to maximizing the total sum of weights `S`.

        Therefore, the problem reduces to finding the path from (0,0) to (R-1, C-1)
        with the maximum sum of weights, using only right and down moves. This is a
        classic dynamic programming problem.

        Dynamic Programming Approach:
        Let `dp[i][j]` represent the maximum possible sum of weights for a path
        from (0,0) to cell (i,j).

        Base Case:
        - `dp[0][0] = grid[0][0]` (The path to the starting cell is just the cell itself)

        Recurrence Relation:
        - For the first row (i=0, j>0): `dp[0][j] = dp[0][j-1] + grid[0][j]`
          (Can only come from the left)
        - For the first column (i>0, j=0): `dp[i][0] = dp[i-1][0] + grid[i][0]`
          (Can only come from above)
        - For any other cell (i>0, j>0): `dp[i][j] = grid[i][j] + max(dp[i-1][j], dp[i][j-1])`
          (Can come from either above or left, choose the path that yields a greater sum)

        The maximum total sum will be `dp[R-1][C-1]`.
        The maximum average will then be `dp[R-1][C-1] / (R + C - 1)`.

        Args:
            grid (list[list[int]]): A 2D list of integers representing the grid weights.

        Returns:
            float: The maximum average weight achievable.
                   Returns 0.0 if the grid is empty or invalid.
        """
        R = len(grid)
        if R == 0:
            return 0.0
        C = len(grid[0])
        if C == 0:
            return 0.0

        # Initialize DP table
        # dp[i][j] stores the maximum sum of weights to reach cell (i,j)
        dp = [[0] * C for _ in range(R)]

        # Base case: The sum to reach (0,0) is just the weight of (0,0)
        dp[0][0] = grid[0][0]

        # Fill the first row
        # To reach (0, j) for j > 0, one must come from (0, j-1)
        for j in range(1, C):
            dp[0][j] = dp[0][j-1] + grid[0][j]

        # Fill the first column
        # To reach (i, 0) for i > 0, one must come from (i-1, 0)
        for i in range(1, R):
            dp[i][0] = dp[i-1][0] + grid[i][0]

        # Fill the rest of the DP table
        # For any cell (i, j), we choose the path from (i-1, j) (above)
        # or (i, j-1) (left) that yields the maximum sum.
        for i in range(1, R):
            for j in range(1, C):
                dp[i][j] = grid[i][j] + max(dp[i-1][j], dp[i][j-1])

        # The maximum total sum path ends at the bottom-right cell (R-1, C-1)
        max_total_sum = dp[R-1][C-1]

        # Calculate the number of cells in any valid path from (0,0) to (R-1,C-1).
        # This is (number of down moves) + (number of right moves) + 1 (for the starting cell).
        # To reach (R-1, C-1) from (0,0), we need (R-1) down moves and (C-1) right moves.
        num_cells_in_path = R + C - 1

        # Calculate the maximum average weight
        max_average = max_total_sum / num_cells_in_path

        return max_average

"""
Time and Space Complexity Analysis:

Time Complexity: O(R * C)
- We iterate through each cell of the `R x C` grid exactly once to populate the `dp` table.
- Each cell's value calculation (`dp[i][j]`) involves a constant number of operations (addition and max comparison).
- Therefore, the total time complexity is directly proportional to the number of cells in the grid.

Space Complexity: O(R * C)
- We use a 2D `dp` table of size `R x C` to store the maximum sums for paths ending at each cell.
- This table stores `R * C` integer values.
- In some dynamic programming problems, space can be optimized to O(min(R, C)) or O(C) by only keeping track of the previous row/column, but for clarity and typical constraints, O(R * C) is generally acceptable and straightforward.
"""

# Test Cases
if __name__ == "__main__":
    solver = Solution()

    print("Running Test Cases:")

    # Test Case 1: Basic 3x3 grid
    grid1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    # DP calculation trace for grid1:
    # dp[0][0]=1, dp[0][1]=3, dp[0][2]=6
    # dp[1][0]=5, dp[1][1]=10 (5+max(3,5)), dp[1][2]=16 (6+max(6,10))
    # dp[2][0]=12, dp[2][1]=20 (8+max(10,12)), dp[2][2]=29 (9+max(16,20))
    # Max sum = 29. Path length = 3 + 3 - 1 = 5. Average = 29 / 5 = 5.8
    expected1 = 5.8
    result1 = solver.maxAveragePath(grid1)
    print(f"Test Case 1 (grid1): Expected: {expected1}, Got: {result1}")
    assert abs(result1 - expected1) < 1e-9, f"Test Case 1 Failed: {result1} != {expected1}"

    # Test Case 2: 1x1 grid
    grid2 = [[100]]
    # Max sum = 100. Path length = 1 + 1 - 1 = 1. Average = 100 / 1 = 100.0
    expected2 = 100.0
    result2 = solver.maxAveragePath(grid2)
    print(f"Test Case 2 (grid2): Expected: {expected2}, Got: {result2}")
    assert abs(result2 - expected2) < 1e-9, f"Test Case 2 Failed: {result2} != {expected2}"

    # Test Case 3: 1xN grid (single row)
    grid3 = [[10, -5, 20, 15]]
    # Max sum = 10 + (-5) + 20 + 15 = 40. Path length = 1 + 4 - 1 = 4. Average = 40 / 4 = 10.0
    expected3 = 10.0
    result3 = solver.maxAveragePath(grid3)
    print(f"Test Case 3 (grid3): Expected: {expected3}, Got: {result3}")
    assert abs(result3 - expected3) < 1e-9, f"Test Case 3 Failed: {result3} != {expected3}"

    # Test Case 4: Nx1 grid (single column)
    grid4 = [[1], [2], [3], [4]]
    # Max sum = 1 + 2 + 3 + 4 = 10. Path length = 4 + 1 - 1 = 4. Average = 10 / 4 = 2.5
    expected4 = 2.5
    result4 = solver.maxAveragePath(grid4)
    print(f"Test Case 4 (grid4): Expected: {expected4}, Got: {result4}")
    assert abs(result4 - expected4) < 1e-9, f"Test Case 4 Failed: {result4} != {expected4}"

    # Test Case 5: Grid with negative numbers (mixed values)
    grid5 = [
        [1, -1, 1],
        [-1, 1, -1],
        [1, -1, 1]
    ]
    # DP trace for grid5:
    # dp[0][0]=1, dp[0][1]=0, dp[0][2]=1
    # dp[1][0]=0, dp[1][1]=1 (1+max(0,0)), dp[1][2]=0 (-1+max(1,1))
    # dp[2][0]=1, dp[2][1]=0 (-1+max(1,1)), dp[2][2]=1 (1+max(0,0))
    # Max sum = 1. Path length = 3 + 3 - 1 = 5. Average = 1 / 5 = 0.2
    expected5 = 0.2
    result5 = solver.maxAveragePath(grid5)
    print(f"Test Case 5 (grid5): Expected: {expected5}, Got: {result5}")
    assert abs(result5 - expected5) < 1e-9, f"Test Case 5 Failed: {result5} != {expected5}"

    # Test Case 6: Empty grid
    grid6 = []
    expected6 = 0.0
    result6 = solver.maxAveragePath(grid6)
    print(f"Test Case 6 (grid6): Expected: {expected6}, Got: {result6}")
    assert abs(result6 - expected6) < 1e-9, f"Test Case 6 Failed: {result6} != {expected6}"

    # Test Case 7: Grid with empty rows
    grid7 = [[]]
    expected7 = 0.0
    result7 = solver.maxAveragePath(grid7)
    print(f"Test Case 7 (grid7): Expected: {expected7}, Got: {result7}")
    assert abs(result7 - expected7) < 1e-9, f"Test Case 7 Failed: {result7} != {expected7}"

    # Test Case 8: Larger grid
    grid8 = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 10, 20, 30]
    ]
    # R=3, C=4. Path length = 3+4-1 = 6.
    # DP trace:
    # Row 0: [10, 30, 60, 100]
    # Row 1: [60, 120 (60+max(30,60)), 190 (70+max(60,120)), 270 (80+max(100,190))]
    # Row 2: [150 (90+max(60,150)), 160 (10+max(120,150)), 180 (20+max(190,160)), 210 (30+max(270,180))]
    # Correction for Row 2, Cell (2,1): 10 + max(dp[1][1], dp[2][0]) = 10 + max(120, 150) = 10 + 150 = 160
    # Correction for Row 2, Cell (2,2): 20 + max(dp[1][2], dp[2][1]) = 20 + max(190, 160) = 20 + 190 = 210
    # Correction for Row 2, Cell (2,3): 30 + max(dp[1][3], dp[2][2]) = 30 + max(270, 210) = 30 + 270 = 300
    # Max sum = 300. Path length = 6. Average = 300 / 6 = 50.0
    expected8 = 50.0
    result8 = solver.maxAveragePath(grid8)
    print(f"Test Case 8 (grid8): Expected: {expected8}, Got: {result8}")
    assert abs(result8 - expected8) < 1e-9, f"Test Case 8 Failed: {result8} != {expected8}"


    print("\nAll test cases passed!")
```