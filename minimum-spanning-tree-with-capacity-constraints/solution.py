```python
import pulp
import itertools

def solve_dcmst_ilp(num_vertices: int, edges: list[tuple[int, int, float]], capacities: list[int]) -> tuple[float | None, list[tuple[int, int]] | None]:
    """
    Solves the "Minimum Spanning Tree with Capacity Constraints" problem using
    Integer Linear Programming (ILP) with PuLP.

    Problem Description:
    Given a connected, undirected graph G = (V, E) with `num_vertices` vertices
    and a list of `edges`, where each edge (u, v, weight) has a weight.
    Additionally, each vertex v has a `capacity` constraint, `capacities[v]`,
    which specifies the maximum allowed degree for that vertex in the resulting
    spanning tree.
    The goal is to find a spanning tree T of G such that:
    1. T spans all `num_vertices`.
    2. For every vertex v in V, the degree of v in T (degree_T(v)) is less than
       or equal to `capacities[v]`.
    3. The sum of weights of the edges in T is minimized.

    This problem is formally known as the Degree-Constrained Minimum Spanning Tree (DCMST)
    problem, which is NP-hard. The ILP formulation provides an exact solution
    for small instances. For larger instances, the number of subtour elimination
    constraints (which ensure connectivity) becomes exponential, making it
    computationally intractable without specialized cutting-plane algorithms
    or heuristic approaches. This implementation explicitly generates all
    subtour elimination constraints, limiting its practical applicability to
    graphs with a relatively small number of vertices (e.g., N < 15-20).

    Args:
        num_vertices (int): The number of vertices in the graph (0-indexed).
        edges (list of tuple): A list of tuples, where each tuple is
                               (u, v, weight) representing an edge between
                               vertex u and vertex v with a given weight.
                               Vertices u and v should be 0-indexed.
                               Parallel edges are handled by taking the minimum
                               weight edge between two nodes.
        capacities (list of int): A list where `capacities[i]` is the maximum
                                  allowed degree for vertex `i` in the spanning tree.
                                  A value of -1 or a very large number can signify no
                                  practical constraint for a node, but positive integers
                                  are expected.

    Returns:
        tuple: (total_weight, selected_edges) if an optimal solution is found.
               `total_weight` is the sum of weights of edges in the DCMST.
               `selected_edges` is a list of (u, v) tuples representing the
               edges in the DCMST. The returned edges are in canonical (min, max) form.
               Returns (None, None) if no feasible solution is found or the solver
               fails to find an optimal solution.

    Time Complexity:
        The dominant part of the complexity comes from setting up and solving
        the ILP.
        1.  **Constraint Generation:**
            *   Number of vertices (V) and edges (E) are derived from inputs.
            *   Objective and Degree Constraints: O(V + E).
            *   Subtour Elimination Constraints: These are generated for all
                non-trivial proper subsets of vertices (i.e., subsets S where
                2 <= |S| < `num_vertices`). There are O(2^V) such subsets.
                For each subset, iterating through edges to find internal edges
                takes O(E) time. Thus, generating these constraints takes O(E * 2^V).
        2.  **ILP Solver Execution:** The time taken by the underlying ILP solver
            (e.g., CBC) is typically exponential in the worst case for NP-hard
            problems (e.g., O(poly(V, E) * 2^V) or worse), as it often involves
            branch-and-bound algorithms.

        Therefore, the overall time complexity is dominated by O(E * 2^V), making it
        practical only for small graphs (V < 15-20).

    Space Complexity:
        1.  **Variable and Edge Storage:** O(V + E) for storing edge data,
            PuLP variables for edges, and adjacency lists.
        2.  **Constraint Storage:** The explicit generation of all subtour
            elimination constraints leads to O(E * 2^V) space for storing
            these constraints within the PuLP model object. This dominates
            the space complexity for larger V.

        Overall space complexity is O(E * 2^V).
    """

    # Create the PuLP problem instance
    prob = pulp.LpProblem("Degree Constrained Minimum Spanning Tree", pulp.LpMinimize)

    # Preprocess edges: use canonical form (u,v with u<v) and handle parallel edges
    # by keeping the minimum weight one.
    pulp_edges_data = {}  # {(u, v): weight}
    for u, v, weight in edges:
        edge_key = tuple(sorted((u, v)))
        if edge_key not in pulp_edges_data or weight < pulp_edges_data[edge_key]:
            pulp_edges_data[edge_key] = weight

    # Define PuLP binary variables for edge selection
    # x[e] = 1 if edge e is in the MST, 0 otherwise
    x = pulp.LpVariable.dicts("x", pulp_edges_data.keys(), 0, 1, pulp.LpBinary)

    # Objective Function: Minimize total weight of selected edges
    prob += pulp.lpSum(pulp_edges_data[e] * x[e] for e in pulp_edges_data.keys()), "Total_Tree_Weight"

    # Constraint 1: A spanning tree on N vertices must have exactly N-1 edges
    if num_vertices > 0:
        prob += pulp.lpSum(x[e] for e in pulp_edges_data.keys()) == num_vertices - 1, "Number_of_Edges"
    elif num_vertices == 0:
        # A graph with 0 vertices has no edges and weight 0.
        return 0.0, []
    else: # num_vertices < 0, invalid input
        print("Error: Number of vertices cannot be negative.")
        return None, None

    # Constraint 2: Degree constraints for each vertex
    # Create a mapping from vertex index to a list of its incident edges (canonical form)
    adj_edges = {i: [] for i in range(num_vertices)}
    for u, v in pulp_edges_data.keys():
        adj_edges[u].append((u, v))
        adj_edges[v].append((u, v))

    for i in range(num_vertices):
        if i >= len(capacities) or capacities[i] < 0:
            # If capacities are not provided for a node or are negative,
            # it might indicate an invalid problem setup or an effectively
            # unconstrained node (though negative is typically an error).
            # For this solution, we assume valid non-negative capacities
            # are provided for all nodes.
            print(f"Error: Invalid or missing capacity for node {i}.")
            return None, None
        
        # Sum of x_e for edges incident to node i must be <= capacities[i]
        prob += pulp.lpSum(x[e] for e in adj_edges[i]) <= capacities[i], f"Degree_Constraint_Node_{i}"

    # Constraint 3: Subtour Elimination Constraints (Connectivity)
    # These constraints ensure that no proper non-empty subset of vertices
    # forms a cycle or a disconnected component of the "tree" (except for the case of num_vertices=1 or 0).
    # Combined with Constraint 1 (N-1 edges), this guarantees a spanning tree.
    # We iterate over all possible subsets of vertices `S` (from size 2 up to num_vertices - 1).
    if num_vertices > 1: # No subtours possible for N <= 1
        for i in range(2, num_vertices):  # `i` represents the size of the subset
            for subset_nodes_tuple in itertools.combinations(range(num_vertices), i):
                subset_nodes = set(subset_nodes_tuple)
                
                # Identify all edges whose both endpoints are within the current subset
                edges_within_subset = []
                for u, v in pulp_edges_data.keys():
                    if u in subset_nodes and v in subset_nodes:
                        edges_within_subset.append(x[(u, v)])
                
                # If there are any edges within this subset, add the constraint:
                # The number of selected edges entirely within subset_nodes must be
                # at most |subset_nodes| - 1. This prevents cycles.
                if edges_within_subset:
                    prob += pulp.lpSum(edges_within_subset) <= len(subset_nodes) - 1, \
                            f"Subtour_Elimination_Size_{len(subset_nodes)}_{'_'.join(map(str, sorted(subset_nodes_tuple)))}"

    # Solve the problem using the default solver (usually CBC, which comes with PuLP)
    # msg=0 suppresses solver output for cleaner execution
    solver = pulp.PULP_CBC_CMD(msg=0)
    prob.solve(solver)

    # Check the solution status
    if prob.status == pulp.LpStatusOptimal:
        selected_edges = []
        for u, v in pulp_edges_data.keys():
            # Check if the edge variable's value is close to 1 (selected)
            if x[(u, v)].varValue > 0.5:
                selected_edges.append((u, v))
        return pulp.value(prob.objective), selected_edges
    else:
        print(f"Problem status: {pulp.LpStatus[prob.status]} - No optimal solution found.")
        return None, None

# --- Test Cases ---
if __name__ == "__main__":
    print("--- Test Case 1: Basic MST (high capacities, no real constraint) ---")
    # Expected: Kruskal's MST result, as capacities are not restrictive.
    # Edges: (0,1,1), (0,2,3), (1,2,1), (1,3,5), (2,3,2)
    # MST: (0,1,1), (1,2,1), (2,3,2) -> weight 4
    num_v1 = 4
    edges1 = [(0, 1, 1), (0, 2, 3), (1, 2, 1), (1, 3, 5), (2, 3, 2)]
    caps1 = [3, 3, 3, 3] # Max degree for a node in a 4-node tree is 3
    weight1, tree1 = solve_dcmst_ilp(num_v1, edges1, caps1)
    print(f"Total Weight: {weight1}")
    print(f"Selected Edges: {sorted(tree1) if tree1 else tree1}")
    # Expected: Total Weight: 4.0, Selected Edges: [(0, 1), (1, 2), (2, 3)]
    print("-" * 50)

    print("--- Test Case 2: Star graph with center capacity constraint ---")
    # A star graph where node 0 is the center.
    # Edges: (0,1,1), (0,2,1), (0,3,1), (1,2,10), (2,3,10), (1,3,10)
    # Without constraint: (0,1,1), (0,2,1), (0,3,1) -> weight 3. Degree of 0 is 3.
    # Capacities: [2, 3, 3, 3] (node 0 can only have 2 edges)
    # Expected: Node 0 must connect to 2 nodes, e.g., (0,1) and (0,2).
    # Node 3 then needs to be connected, e.g., via (1,3) or (2,3).
    # (0,1,1), (0,2,1), (1,3,10) -> weight 12.
    num_v2 = 4
    edges2 = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 10), (2, 3, 10), (1, 3, 10)]
    caps2 = [2, 3, 3, 3] # Node 0 capacity is 2
    weight2, tree2 = solve_dcmst_ilp(num_v2, edges2, caps2)
    print(f"Total Weight: {weight2}")
    print(f"Selected Edges: {sorted(tree2) if tree2 else tree2}")
    # Expected: Total Weight: 12.0, Selected Edges: [(0, 1), (0, 2), (1, 3)] or [(0, 1), (0, 3), (1, 2)] etc. (depends on specific choices for symmetric edges)
    # The solver output might pick a different set of symmetric edges. Let's check for sum.
    # e.g., [(0, 1), (0, 2), (1, 3)] is one valid solution. Another is [(0, 1), (0, 3), (1, 2)] (same weight).
    # The actual output from PuLP with CBC might be: [(0, 1), (0, 2), (1, 3)] (or similar)
    print("-" * 50)

    print("--- Test Case 3: No feasible solution (too restrictive capacities) ---")
    # Nodes: 3. Edges needed: 2.
    # Capacities: [1, 1, 1] (each node can only have 1 edge).
    # It's impossible to form a spanning tree where each node has degree at most 1,
    # because a tree with 3 nodes must have at least one node with degree 2 if it's a path,
    # or all nodes with degree 1 if it's disconnected (not a tree).
    num_v3 = 3
    edges3 = [(0, 1, 1), (1, 2, 1), (0, 2, 100)]
    caps3 = [1, 1, 1]
    weight3, tree3 = solve_dcmst_ilp(num_v3, edges3, caps3)
    print(f"Total Weight: {weight3}")
    print(f"Selected Edges: {tree3}")
    # Expected: Total Weight: None, Selected Edges: None (Problem status: Infeasible)
    print("-" * 50)

    print("--- Test Case 4: Larger graph with varied constraints ---")
    num_v4 = 5
    edges4 = [
        (0, 1, 1), (0, 2, 7), (0, 3, 5),
        (1, 2, 2), (1, 3, 4), (1, 4, 3),
        (2, 3, 6), (2, 4, 8),
        (3, 4, 9)
    ]
    # N-1 = 4 edges needed.
    # Capacities: [1, 2, 2, 2, 2]
    # Node 0 must have degree 1.
    # Node 1,2,3,4 can have degree up to 2.
    # Greedy (Kruskal-like with constraints) might pick (0,1,1).
    # Then 0 is "full".
    # Remaining edges: (1,2,2), (1,4,3), (1,3,4), (0,3,5), ...
    # (1,2,2) -> tree: (0,1), (1,2). Current degrees: 0:1, 1:2, 2:1. Node 1 is full.
    # Next must connect 3,4.
    # Can't use (1,3), (1,4). Must use other edges.
    # e.g. (0,1,1), (1,2,2), (1,4,3) would give degree 3 for node 1 if all picked.
    # Let's see what the ILP yields.
    caps4 = [1, 2, 2, 2, 2]
    weight4, tree4 = solve_dcmst_ilp(num_v4, edges4, caps4)
    print(f"Total Weight: {weight4}")
    print(f"Selected Edges: {sorted(tree4) if tree4 else tree4}")
    # A possible solution:
    # (0,1,1) - node 0 is full (deg=1), node 1 deg=1
    # (1,2,2) - node 1 is full (deg=2), node 2 deg=1
    # (3,4,9) - to connect 3 and 4, without involving 0,1,2 that are full or would make 1 full.
    #   but need to connect to {0,1,2} component.
    #   Maybe (0,3,5) or (1,3,4) is forced due to this.
    # Optimal: [(0, 1), (1, 2), (2, 3), (1, 4)] -> W=1+2+6+3=12. Degs: 0:1, 1:3 (violates)
    # Let's consider:
    # (0,1,1) -> d0=1 (full), d1=1
    # (2,3,6) -> d2=1, d3=1 (cost 1)
    # Need to connect {0,1} to {2,3}.
    # Possible connections: (0,2,7), (0,3,5), (1,2,2), (1,3,4)
    # The cheapest to connect {0,1} to {2,3} that doesn't violate node 0 capacity is (1,2,2) or (1,3,4).
    # If (1,2,2): d1=2 (full), d2=1. Tree: (0,1,1), (1,2,2).
    # Now need to connect 3,4.
    # If we connect (3,4,9), then 3 and 4 are still isolated from the main tree.
    # Need to connect 3, 4 to {0,1,2}.
    # With d0=1, d1=2.
    # So connect 3 and 4 via d2. E.g. (2,3,6) (d2=2 full, d3=1) and (1,4,3) (d1=3 violate) or (2,4,8)
    # The answer found by PuLP should be correct.
    # Manual check for [(0, 1), (1, 4), (2, 3), (1, 2)] would be:
    # Edges: (0,1,1), (1,4,3), (2,3,6), (1,2,2)
    # Weights: 1 + 3 + 6 + 2 = 12
    # Degrees:
    # Node 0: (0,1) -> 1 (OK, cap=1)
    # Node 1: (0,1), (1,4), (1,2) -> 3 (FAIL, cap=2)
    # This manually constructed example is incorrect. The ILP solution should be right.
    # The actual PuLP solution for Test Case 4 with caps=[1,2,2,2,2] is likely:
    # Edges: (0, 3), (1, 2), (1, 4), (3, 4)
    # Weights: (0,3,5), (1,2,2), (1,4,3), (3,4,9) -> 5 + 2 + 3 + 9 = 19
    # Degrees:
    # Node 0: (0,3) -> 1 (OK, cap=1)
    # Node 1: (1,2), (1,4) -> 2 (OK, cap=2)
    # Node 2: (1,2) -> 1 (OK, cap=2)
    # Node 3: (0,3), (3,4) -> 2 (OK, cap=2)
    # Node 4: (1,4), (3,4) -> 2 (OK, cap=2)
    # This is a valid solution with weight 19.
    print("-" * 50)

    print("--- Test Case 5: Graph with 1 vertex ---")
    num_v5 = 1
    edges5 = []
    caps5 = [0] # 0 for 1 vertex (no edges)
    weight5, tree5 = solve_dcmst_ilp(num_v5, edges5, caps5)
    print(f"Total Weight: {weight5}")
    print(f"Selected Edges: {tree5}")
    # Expected: Total Weight: 0.0, Selected Edges: []
    print("-" * 50)

    print("--- Test Case 6: Graph with 0 vertices ---")
    num_v6 = 0
    edges6 = []
    caps6 = []
    weight6, tree6 = solve_dcmst_ilp(num_v6, edges6, caps6)
    print(f"Total Weight: {weight6}")
    print(f"Selected Edges: {tree6}")
    # Expected: Total Weight: 0.0, Selected Edges: []
    print("-" * 50)

    print("--- Test Case 7: Complex 5-node example (where simple Kruskal-like fails) ---")
    # This scenario is designed to show how strict degree constraints can
    # force non-greedy choices.
    num_v7 = 5
    edges7 = [
        (0, 1, 10), (0, 2, 1), (0, 3, 10), (0, 4, 10), # Node 0 wants cheap (0,2)
        (1, 2, 10), (1, 3, 1), (1, 4, 10), # Node 1 wants cheap (1,3)
        (2, 3, 10), (2, 4, 1), # Node 2 wants cheap (2,4)
        (3, 4, 10) # Node 3 wants cheap (3,1)
    ]
    # N-1 = 4 edges needed.
    # Capacities: [1, 1, 1, 1, 4]
    # Nodes 0,1,2,3 can only have degree 1. Node 4 can have degree up to 4.
    # This forces 0,1,2,3 to be leaves, connected directly to node 4.
    # The connections should be: (0,2,1), (1,3,1), (2,4,1) - these are not directly connected
    # (0,2,1) -> Degs: 0:1, 2:1. (0,2) is a valid path.
    # If 0,1,2,3 must have degree 1, they must connect to node 4 (the only one with high capacity).
    # So the tree must be a star graph centered at node 4.
    # We need to pick edges (0,4,?), (1,4,?), (2,4,?), (3,4,?).
    # The edges for node 4:
    # (0,4,10)
    # (1,4,10)
    # (2,4,1) (this is the cheapest way to connect 2 to 4)
    # (3,4,10)
    # But wait, edges are: (0, 2, 1), (1, 3, 1), (2, 4, 1)
    # If we choose (0,2,1) and (1,3,1), then nodes 0,1,2,3 are all degree 1.
    # We'd need 2 more edges to connect these two components and ensure node 4 is part of it.
    # This is exactly the type of problem where ILP shines.
    # Expected solution based on constraints:
    # Edges for nodes 0,1,2,3 must have degree 1, meaning they connect to only one other node.
    # The cheapest way to satisfy this while connecting to node 4 (which is the only one
    # that can handle multiple connections) would be for 0,1,2,3 to be leaves connected to 4.
    # Edges from input: (0,4,10), (1,4,10), (2,4,1), (3,4,10).
    # The MST would pick (0,4,10), (1,4,10), (2,4,1), (3,4,10).
    # Total weight: 10 + 10 + 1 + 10 = 31.
    # Degrees: 0:1, 1:1, 2:1, 3:1, 4:4. All valid.
    caps7 = [1, 1, 1, 1, 4]
    weight7, tree7 = solve_dcmst_ilp(num_v7, edges7, caps7)
    print(f"Total Weight: {weight7}")
    print(f"Selected Edges: {sorted(tree7) if tree7 else tree7}")
    # Expected: Total Weight: 31.0, Selected Edges: [(0, 4), (1, 4), (2, 4), (3, 4)]
    print("-" * 50)
```