```python
import collections

class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        """
        Finds the length of the shortest clear path from the top-left cell (0, 0)
        to the bottom-right cell (n-1, n-1) in a binary matrix.

        A clear path means:
        1. All visited cells must be 0.
        2. Moves can be 8-directional (horizontal, vertical, and diagonal).
        3. The path length includes the starting and ending cells.

        Args:
            grid: An n x n binary matrix where 0 is an open cell and 1 is a blocked cell.

        Returns:
            The length of the shortest clear path, or -1 if no such path exists.
        """
        n = len(grid)

        # Edge case: If the start or end cell is blocked (1), no path is possible.
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        
        # If the grid is just a single cell and it's open, the path length is 1.
        if n == 1:
            return 1 if grid[0][0] == 0 else -1

        # BFS Queue: Stores tuples of (row, col, distance)
        # Start at (0, 0) with an initial distance of 1 (since the starting cell counts).
        queue = collections.deque([(0, 0, 1)])

        # Visited set: Stores tuples of (row, col) to keep track of visited cells
        # and prevent cycles or redundant processing.
        visited = set([(0, 0)])

        # 8-directional movements: (dr, dc)
        # (up, down, left, right, and 4 diagonals)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        while queue:
            r, c, dist = queue.popleft()

            # If we reached the target cell (n-1, n-1), return the current distance.
            if r == n - 1 and c == n - 1:
                return dist

            # Explore all 8 possible neighbors
            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                # Check if the neighbor is within grid boundaries
                # and if it's an open cell (0)
                # and if it hasn't been visited yet.
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
        
        # If the queue becomes empty and we haven't reached the target,
        # it means no clear path exists.
        return -1

```