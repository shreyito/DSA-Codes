```python
import math

class Solution:
    def findTheCity(self, n: int, edges: list[list[int]], distanceThreshold: int) -> int:
        """
        Finds the city with the smallest number of reachable cities within a given
        distance threshold. If there's a tie, the city with the largest label (index) is returned.

        The problem can be modeled as an all-pairs shortest path problem on a weighted,
        undirected graph. Floyd-Warshall algorithm is suitable for this, especially
        given the constraint n <= 100.

        Args:
            n: The number of cities (nodes) in the graph, labeled from 0 to n-1.
            edges: A list of lists, where each inner list [fromi, toi, weighti]
                   represents a bidirectional edge between city `fromi` and city `toi`
                   with a distance `weighti`.
            distanceThreshold: The maximum distance a city can be from another
                               to be considered a "reachable neighbor".

        Returns:
            The label of the city with the smallest number of reachable neighbors
            within the distance threshold. In case of a tie, the city with the
            largest label is returned.
        """

        # Step 1: Initialize the distance matrix for all-pairs shortest paths.
        # dist[i][j] will store the shortest distance from city i to city j.
        # Initialize with infinity, and 0 for self-loops (distance from a city to itself).
        dist = [[math.inf] * n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        # Populate the distance matrix with direct edge weights.
        # Edges are bidirectional, so update both dist[u][v] and dist[v][u].
        # If there are multiple edges between the same two cities, only the
        # minimum weight edge matters for shortest paths.
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)

        # Step 2: Apply the Floyd-Warshall algorithm to find all-pairs shortest paths.
        # k is the intermediate node (the "via" node).
        # i is the source node.
        # j is the destination node.
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # Only update if paths through k are valid (not infinity, avoiding overflow)
                    if dist[i][k] != math.inf and dist[k][j] != math.inf:
                        dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        # Step 3: Count reachable cities for each city and find the best one.
        min_reachable_cities_count = n + 1  # Initialize with a value higher than any possible count
        result_city = -1                    # Initialize with an invalid city label

        # Iterate through cities in reverse order (from n-1 down to 0) to
        # easily handle the tie-breaking condition: "return the city with the largest label".
        for i in range(n - 1, -1, -1):
            current_reachable_cities_count = 0
            for j in range(n):
                # Do not count the city itself
                if i == j:
                    continue
                # If the distance is within the threshold, it's a reachable neighbor
                if dist[i][j] <= distanceThreshold:
                    current_reachable_cities_count += 1

            # Update if this city has fewer reachable neighbors
            # or if it has the same number but its label is larger (due to reverse iteration).
            if current_reachable_cities_count <= min_reachable_cities_count:
                min_reachable_cities_count = current_reachable_cities_count
                result_city = i

        return result_city

```