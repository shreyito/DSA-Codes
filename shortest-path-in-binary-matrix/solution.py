```python
import collections

class Solution:
    """
    Solution for the "Shortest Path in Binary Matrix" problem.
    """

    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        """
        Finds the shortest path from the top-left cell (0, 0) to the bottom-right
        cell (N-1, N-1) in a binary matrix, where 0 represents an open cell and
        1 represents a blocked cell. Movement is allowed in 8 directions
        (horizontally, vertically, and diagonally).

        Args:
            grid: A list of lists of integers representing the binary matrix.
                  The matrix is guaranteed to be square (N x N).

        Returns:
            The length of the shortest clear path, or -1 if no such path exists.
        """
        n = len(grid)

        # 1. Edge Case: Check for invalid grid or inaccessible start/end points
        # If the grid is empty or the start/end cell is blocked (value 1),
        # a path is impossible.
        if n == 0 or grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        # 2. Edge Case: If it's a 1x1 grid and the start cell is 0, the path length is 1.
        if n == 1:
            return 1 # We already checked grid[0][0] == 1 above, so it must be 0 here.

        # 3. BFS Initialization
        # Queue stores tuples of (row, column, distance).
        # We start at (0, 0) with an initial distance of 1.
        queue = collections.deque([(0, 0, 1)])

        # Set to keep track of visited cells to avoid cycles and redundant processing.
        visited = set([(0, 0)])

        # Define all 8 possible directions of movement (row_offset, col_offset).
        # Clockwise from top-left:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
            (0, -1),           (0, 1),   # Left, Right
            (1, -1),  (1, 0),  (1, 1)    # Bottom-left, Bottom, Bottom-right
        ]

        # 4. BFS Traversal
        while queue:
            r, c, dist = queue.popleft()

            # Check if we have reached the destination (bottom-right cell).
            if r == n - 1 and c == n - 1:
                return dist

            # Explore all 8 neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc  # Calculate new neighbor coordinates

                # Check if the neighbor is valid:
                # a. Within grid boundaries (0 <= nr < n and 0 <= nc < n)
                # b. Is an open cell (grid[nr][nc] == 0)
                # c. Has not been visited yet ((nr, nc) not in visited)
                if (0 <= nr < n and 
                    0 <= nc < n and 
                    grid[nr][nc] == 0 and 
                    (nr, nc) not in visited):
                    
                    visited.add((nr, nc))         # Mark as visited
                    queue.append((nr, nc, dist + 1)) # Add to queue with incremented distance
        
        # 5. No Path Found
        # If the queue becomes empty and the destination was never reached,
        # it means there is no clear path.
        return -1

# --- Complexity Analysis ---
# Time Complexity: O(N*M)
# In the worst case, BFS visits every cell in the grid once. For each cell,
# it performs a constant number of operations (checking 8 neighbors).
# Since the grid is N x N, this becomes O(N^2).

# Space Complexity: O(N*M)
# In the worst case, the `queue` could store almost all cells if the shortest
# path covers a large portion of the grid. The `visited` set also stores
# entries for each visited cell.
# For an N x N grid, this becomes O(N^2).

# --- Test Cases ---
if __name__ == "__main__":
    solver = Solution()

    # Test Case 1: Basic 2x2 grid
    grid1 = [[0, 1],
             [1, 0]]
    # Expected: 2 (Path: (0,0) -> (1,1))
    print(f"Grid: {grid1}, Shortest Path: {solver.shortestPathBinaryMatrix(grid1)}") 
    assert solver.shortestPathBinaryMatrix(grid1) == 2

    # Test Case 2: Larger grid with a path
    grid2 = [[0, 0, 0],
             [1, 1, 0],
             [1, 1, 0]]
    # Expected: 4 (Path: (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2)) - incorrect, direct path is better
    # Expected: 4 (Path: (0,0) -> (0,1) -> (1,2) -> (2,2) - diagonal (0,1) to (1,2) is okay)
    # The actual path should be (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) if no diagonal used for (0,1)->(1,2)
    # Using diagonals: (0,0) -> (0,1) -> (1,2) -> (2,2) is length 4
    # (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) is length 5.
    # The shortest is (0,0) -> (0,1) -> (1,2) -> (2,2) = 4
    print(f"Grid: {grid2}, Shortest Path: {solver.shortestPathBinaryMatrix(grid2)}")
    assert solver.shortestPathBinaryMatrix(grid2) == 4

    # Test Case 3: Start cell blocked
    grid3 = [[1, 0, 0],
             [1, 1, 0],
             [1, 1, 0]]
    # Expected: -1
    print(f"Grid: {grid3}, Shortest Path: {solver.shortestPathBinaryMatrix(grid3)}")
    assert solver.shortestPathBinaryMatrix(grid3) == -1

    # Test Case 4: No path (blocked in middle)
    grid4 = [[0, 0, 0],
             [0, 1, 0],
             [0, 0, 0]]
    # Expected: 5 (Path example: (0,0)-(1,0)-(2,0)-(2,1)-(2,2)) or diagonal variations
    print(f"Grid: {grid4}, Shortest Path: {solver.shortestPathBinaryMatrix(grid4)}")
    assert solver.shortestPathBinaryMatrix(grid4) == 5

    # Test Case 5: Destination cell blocked
    grid5 = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 1]]
    # Expected: -1
    print(f"Grid: {grid5}, Shortest Path: {solver.shortestPathBinaryMatrix(grid5)}")
    assert solver.shortestPathBinaryMatrix(grid5) == -1

    # Test Case 6: Direct diagonal path (shortest possible for N>1)
    grid6 = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    # Expected: 3 (Path: (0,0) -> (1,1) -> (2,2))
    print(f"Grid: {grid6}, Shortest Path: {solver.shortestPathBinaryMatrix(grid6)}")
    assert solver.shortestPathBinaryMatrix(grid6) == 3

    # Test Case 7: Single cell grid, clear
    grid7 = [[0]]
    # Expected: 1
    print(f"Grid: {grid7}, Shortest Path: {solver.shortestPathBinaryMatrix(grid7)}")
    assert solver.shortestPathBinaryMatrix(grid7) == 1

    # Test Case 8: Single cell grid, blocked
    grid8 = [[1]]
    # Expected: -1
    print(f"Grid: {grid8}, Shortest Path: {solver.shortestPathBinaryMatrix(grid8)}")
    assert solver.shortestPathBinaryMatrix(grid8) == -1

    # Test Case 9: Larger grid with multiple turns
    grid9 = [[0, 0, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 0, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 0, 0, 0, 0]]
    # Expected: 7 (e.g., (0,0)-(0,1)-(0,2)-(0,3)-(0,4)-(1,4)-(2,4)-(3,4)-(4,4)) is 9 steps
    # Path: (0,0)-(0,1)-(0,2)-(0,3)-(0,4)-(1,4)-(2,4)-(2,3)-(2,2)-(3,3)-(4,4) = 11?
    # Actual BFS path: (0,0)->(1,0)->(2,0)->(2,1)->(2,2)->(3,3)->(4,4) is 7 steps
    print(f"Grid: {grid9}, Shortest Path: {solver.shortestPathBinaryMatrix(grid9)}")
    assert solver.shortestPathBinaryMatrix(grid9) == 7

    print("\nAll test cases passed!")
```