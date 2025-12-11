```python
import collections

class Solution:
    def shortestPath(self, grid: list[list[int]]) -> int:
        """
        Calculates the shortest path (minimum number of jumps) from the top-left
        cell (0, 0) to the bottom-right cell (rows-1, cols-1) in a grid.

        Each cell contains a value representing the maximum jump length allowed
        from that cell. Jumps can be horizontal or vertical (up, down, left, right).
        A jump of length `k` means moving exactly `k` cells in one of the cardinal
        directions. Any length from 1 up to the cell's maximum jump length is allowed.

        Args:
            grid: A list of lists of integers representing the grid.
                  grid[r][c] is the maximum jump length from cell (r, c).

        Returns:
            The minimum number of jumps required to reach the target cell.
            Returns -1 if the target cell is unreachable.
        """
        if not grid or not grid[0]:
            return -1  # Handle empty or invalid grid

        rows, cols = len(grid), len(grid[0])
        
        # If the start cell is the target cell (1x1 grid), no jumps needed
        if rows == 1 and cols == 1:
            return 0

        # Queue for Breadth-First Search (BFS)
        # Stores tuples: (row, col, distance)
        # distance: number of jumps taken to reach (row, col)
        queue = collections.deque([(0, 0, 0)])

        # Set to keep track of visited cells
        # This prevents cycles and redundant processing, ensuring we find the shortest path
        visited = set([(0, 0)])

        # Directions for horizontal and vertical movements
        # (dr, dc): (delta_row, delta_col)
        # (0, 1): Right, (0, -1): Left, (1, 0): Down, (-1, 0): Up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            r, c, dist = queue.popleft()

            # Get the maximum allowed jump length from the current cell
            max_jump_length = grid[r][c]

            # Explore all possible jumps from the current cell
            # A jump can be of any length from 1 up to max_jump_length
            for dr, dc in directions:
                for jump_len in range(1, max_jump_length + 1):
                    next_r, next_c = r + dr * jump_len, c + dc * jump_len

                    # Check if the new position is within grid boundaries
                    if 0 <= next_r < rows and 0 <= next_c < cols:
                        # If the new position is the target cell, we found the shortest path
                        if next_r == rows - 1 and next_c == cols - 1:
                            return dist + 1

                        # If this cell has not been visited, add it to the queue
                        # for further exploration
                        if (next_r, next_c) not in visited:
                            visited.add((next_r, next_c))
                            queue.append((next_r, next_c, dist + 1))
        
        # If the queue becomes empty and the target cell was not reached,
        # it means the target is unreachable
        return -1

# --- Complexity Analysis ---
# Let R be the number of rows and C be the number of columns in the grid.
#
# Time Complexity: O(R * C * max(R, C))
#   - Each cell (r, c) is visited and processed at most once.
#   - From each cell (r, c), we iterate through 4 possible cardinal directions.
#   - In each direction, we iterate through jump lengths from 1 up to `grid[r][c]`.
#     The maximum possible value for `grid[r][c]` can be `max(R, C)`
#     (e.g., to reach the end of the grid in one jump).
#   - So, for each of the R * C cells, in the worst case, we might explore
#     approximately `4 * max(R, C)` potential next cells.
#   - Therefore, the total time complexity is roughly `R * C * 4 * max(R, C)`,
#     which simplifies to O(R * C * max(R, C)).
#
# Space Complexity: O(R * C)
#   - The `queue` stores `(r, c, distance)` tuples. In the worst case, it might
#     hold all reachable cells, which is at most R * C cells.
#   - The `visited` set stores `(r, c)` tuples. In the worst case, it might
#     store all cells in the grid, which is R * C cells.
#   - Thus, the space complexity is dominated by the size of the grid, O(R * C).


# --- Test Cases ---
if __name__ == "__main__":
    sol = Solution()

    print("--- Test Case 1: Basic Path (3x3 grid, all 1s) ---")
    grid1 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    # Path: (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) = 4 jumps
    # Or (0,0) -> (1,0) -> (2,0) -> (2,1) -> (2,2) = 4 jumps
    # Expected: 4
    result1 = sol.shortestPath(grid1)
    print(f"Grid:\n{grid1}\nShortest Path: {result1} (Expected: 4)\n")

    print("--- Test Case 2: Unreachable Target (start cell has 0 jump) ---")
    grid2 = [
        [0, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    # Expected: -1 (Cannot move from (0,0))
    result2 = sol.shortestPath(grid2)
    print(f"Grid:\n{grid2}\nShortest Path: {result2} (Expected: -1)\n")

    print("--- Test Case 3: 1x1 Grid (Start is Target) ---")
    grid3 = [
        [5]
    ]
    # Expected: 0
    result3 = sol.shortestPath(grid3)
    print(f"Grid:\n{grid3}\nShortest Path: {result3} (Expected: 0)\n")

    print("--- Test Case 4: Grid with Large Jumps ---")
    grid4 = [
        [2, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    # Path: (0,0) --jump 2--> (0,2) --jump 1--> (1,2) --jump 1--> (2,2) = 3 jumps
    # Expected: 3
    result4 = sol.shortestPath(grid4)
    print(f"Grid:\n{grid4}\nShortest Path: {result4} (Expected: 3)\n")

    print("--- Test Case 5: Unreachable Target (blocked path) ---")
    grid5 = [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    # Path is blocked by cells with 0 jump length
    # Expected: -1
    result5 = sol.shortestPath(grid5)
    print(f"Grid:\n{grid5}\nShortest Path: {result5} (Expected: -1)\n")

    print("--- Test Case 6: Larger Grid with Mixed Jumps ---")
    grid6 = [
        [3, 2, 1, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 1, 1, 0]
    ]
    # (0,0,0) val 3
    #  -> (0,3,1) val 0 (dead end)
    #  -> (1,0,1) val 1
    #    -> (1,1,2) val 1
    #      -> (2,1,3) val 1
    #        -> (2,2,4) val 1
    #          -> (3,2,5) val 1
    #           -> (3,3,6) Target! 6 jumps
    # Another path:
    # (0,0,0) val 3
    #  -> (2,0,1) val 1
    #    -> (2,1,2) val 1
    #      -> (2,2,3) val 1
    #        -> (3,2,4) val 1
    #          -> (3,3,5) Target! 5 jumps
    # Expected: 5
    result6 = sol.shortestPath(grid6)
    print(f"Grid:\n{grid6}\nShortest Path: {result6} (Expected: 5)\n")

    print("--- Test Case 7: All zeros except start (1x2 grid) ---")
    grid7 = [[1,0]]
    # Expected: -1 (Target 0,1 is blocked)
    result7 = sol.shortestPath(grid7)
    print(f"Grid:\n{grid7}\nShortest Path: {result7} (Expected: -1)\n")

    print("--- Test Case 8: All zeros except start (2x1 grid) ---")
    grid8 = [[1],[0]]
    # Expected: -1 (Target 1,0 is blocked)
    result8 = sol.shortestPath(grid8)
    print(f"Grid:\n{grid8}\nShortest Path: {result8} (Expected: -1)\n")

    print("--- Test Case 9: Direct path in 1 jump ---")
    grid9 = [
        [2, 0],
        [0, 0]
    ]
    # (0,0) val 2 -> jump 2 to (0,2) (invalid) or (2,0) (invalid)
    # Oh, target is (1,1). From (0,0) to (1,1) with value 2?
    # (0,0) can jump to (0,1) (invalid) or (1,0) (invalid) if jump_len=1
    # This specific grid won't work. Let's make one that has a 1-jump solution:
    grid9_corrected = [
        [2, 0],
        [0, 0]
    ]
    # Suppose target is (1,0) for this example
    # No, the problem fixed target to (rows-1, cols-1).
    # New grid for 1-jump:
    grid_one_jump = [
        [2, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    # Target (2,2)
    # (0,0) val 2
    # Can jump 2 steps down to (2,0)
    # Then from (2,0) val 1
    # Can jump 1 step right to (2,1)
    # Then from (2,1) val 1
    # Can jump 1 step right to (2,2)
    # This is 3 steps.
    # What if (0,0) can reach (rows-1,cols-1) in one jump?
    grid_direct_jump = [
        [3, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]
    # From (0,0) val 3, can jump 3 steps right to (0,3). dist 1.
    # From (0,0) val 3, can jump 3 steps down to (3,0). dist 1.
    # To reach (3,3):
    # From (0,0) jump 3 steps down to (3,0) (dist 1).
    # From (3,0) val 1, jump 3 steps right. Not possible as max_jump_length is 1.
    # So BFS. (0,0) -> (0,3) (dist 1)
    # From (0,3) val 1 -> (1,3) (dist 2)
    # From (1,3) val 1 -> (2,3) (dist 3)
    # From (2,3) val 1 -> (3,3) (dist 4).
    # Expected: 4
    result_direct_jump = sol.shortestPath(grid_direct_jump)
    print(f"Grid:\n{grid_direct_jump}\nShortest Path: {result_direct_jump} (Expected: 4)\n")
```