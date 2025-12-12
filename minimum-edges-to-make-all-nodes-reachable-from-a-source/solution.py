```python
import collections

class Solution:
    """
    Problem Description:
    Given a directed graph with `n` nodes (labeled from 0 to n-1) and a list of `edges`,
    and a `source` node. The task is to find the minimum number of additional directed
    edges that need to be added to the existing graph such that all nodes become
    reachable from the `source` node.

    An "additional edge" means we can create a new directed connection (u, v) between
    any two nodes u and v. The goal is to minimize the total count of such new edges.

    Example:
    n=4, edges=[(0,1), (2,3)], source=0
    Nodes 0 and 1 are reachable from 0. Nodes 2 and 3 are not.
    To make 2 and 3 reachable, we need to add an edge. If we add (0,2), then 2 becomes
    reachable, and since 2 can reach 3, 3 also becomes reachable. So, 1 additional edge.

    Solution Approach:
    This problem can be effectively solved by leveraging the concept of Strongly Connected
    Components (SCCs) and the condensation graph (a Directed Acyclic Graph - DAG of SCCs).

    1.  **Find Strongly Connected Components (SCCs):**
        Decompose the given graph into its SCCs. All nodes within an SCC are mutually
        reachable. Kosaraju's algorithm or Tarjan's algorithm can be used for this.
        Kosaraju's algorithm involves two DFS passes:
        a.  First DFS on the original graph to determine the finishing times of nodes.
            Nodes are pushed onto a stack in the order they finish.
        b.  Second DFS on the transpose graph (all edges reversed), processing nodes
            in decreasing order of finishing times (by popping from the stack). Each
            time a new unvisited node is encountered, a new SCC is identified.

    2.  **Build the Condensation Graph:**
        Create a new graph where each node represents an SCC from the original graph.
        An edge exists from SCC_A to SCC_B in the condensation graph if there is at
        least one edge in the original graph from a node in SCC_A to a node in SCC_B.
        This condensation graph will be a Directed Acyclic Graph (DAG).
        Simultaneously, calculate the in-degree for each SCC node in this DAG.

    3.  **Identify Reachable SCCs from Source:**
        Find the SCC that contains the `source` node. Let this be `source_scc`.
        Perform a Breadth-First Search (BFS) or Depth-First Search (DFS) on the
        condensation graph starting from `source_scc` to determine all SCCs that are
        reachable from `source_scc`. All nodes belonging to these reachable SCCs are
        already reachable from the original `source` node.

    4.  **Count Minimum Edges to Add:**
        The minimum number of additional edges required is the count of SCCs that
        are *not* reachable from `source_scc` AND have an in-degree of 0 in the
        condensation graph. These are the "source" SCCs in the DAG of SCCs that are
        isolated from the original source's reach. For each such unreachable source SCC,
        we must add at least one edge (e.g., from the original `source` node or any
        node in a reachable SCC) to *any* node within that SCC. Adding one edge makes
        that entire SCC reachable, as well as any SCCs downstream from it in the
        condensation graph. Therefore, we simply count these unreachable "source" SCCs.
    """

    def minEdgesToMakeAllNodesReachable(self, n: int, edges: list[list[int]], source: int) -> int:
        # Handle edge case for an empty graph
        if n == 0:
            return 0

        # Step 1: Build the graph and its transpose
        # adj: adjacency list for the original graph
        # rev_adj: adjacency list for the transpose graph (all edges reversed)
        adj = collections.defaultdict(list)
        rev_adj = collections.defaultdict(list)
        for u, v in edges:
            adj[u].append(v)
            rev_adj[v].append(u)

        # Step 2: Kosaraju's Algorithm for Strongly Connected Components (SCCs)

        # DFS 1: Populate a stack with nodes in order of their finishing times
        visited_dfs1 = [False] * n
        stack = [] # Stores nodes in increasing order of finishing times

        def dfs1(u):
            visited_dfs1[u] = True
            for v in adj[u]:
                if not visited_dfs1[v]:
                    dfs1(v)
            stack.append(u) # Node u finishes, push to stack

        # Run DFS1 for all unvisited nodes to ensure all nodes are processed
        for i in range(n):
            if not visited_dfs1[i]:
                dfs1(i)

        # DFS 2: Find SCCs using the transpose graph
        scc_id = [-1] * n  # scc_id[i] stores the SCC identifier for node i
        current_scc_idx = 0 # Counter for assigning unique SCC IDs

        def dfs2(u):
            scc_id[u] = current_scc_idx # Assign current SCC ID to node u
            for v in rev_adj[u]:
                if scc_id[v] == -1:  # If node v has not yet been assigned to an SCC
                    dfs2(v)

        # Process nodes from the stack (in decreasing order of finishing times)
        while stack:
            u = stack.pop()
            if scc_id[u] == -1: # If node u hasn't been assigned to an SCC yet
                dfs2(u) # Start a new DFS2 to find all nodes in this SCC
                current_scc_idx += 1 # Increment for the next SCC

        num_sccs = current_scc_idx # Total number of SCCs identified
        
        # Determine the SCC that contains the original source node
        # It's guaranteed that `source` is a valid node index [0, n-1] if n > 0.
        source_scc = scc_id[source]

        # Step 3: Build Condensation Graph and calculate in-degrees
        # scc_adj: Adjacency list for the condensation graph.
        #          Each entry scc_adj[i] is a set of SCCs reachable from SCC i.
        # scc_in_degree: Array storing the in-degree of each SCC in the condensation graph.
        scc_adj = [set() for _ in range(num_sccs)]
        scc_in_degree = [0] * num_sccs

        # Iterate through all original edges to find edges connecting different SCCs
        for u in range(n):
            for v in adj[u]:
                if scc_id[u] != scc_id[v]: # If edge (u, v) connects two different SCCs
                    # Add an edge from scc_id[u] to scc_id[v] in the condensation graph
                    # Using a set for scc_adj[scc_id[u]] automatically handles duplicate edges
                    scc_adj[scc_id[u]].add(scc_id[v])
        
        # Calculate in-degrees for the condensation graph
        for i in range(num_sccs):
            for neighbor_scc in scc_adj[i]:
                scc_in_degree[neighbor_scc] += 1

        # Step 4: Find all SCCs reachable from the source SCC using BFS
        reachable_sccs = [False] * num_sccs # Tracks which SCCs are reachable from source_scc
        
        q = collections.deque()
        
        # Start BFS from the source SCC
        q.append(source_scc)
        reachable_sccs[source_scc] = True

        while q:
            current_scc = q.popleft()
            for neighbor_scc in scc_adj[current_scc]:
                if not reachable_sccs[neighbor_scc]:
                    reachable_sccs[neighbor_scc] = True
                    q.append(neighbor_scc)

        # Step 5: Count unreachable SCCs that have an in-degree of 0
        # These are the "root" SCCs in the condensation DAG that are not already
        # reachable from the source SCC. Each such SCC needs one additional edge.
        edges_to_add = 0
        for i in range(num_sccs):
            if not reachable_sccs[i] and scc_in_degree[i] == 0:
                edges_to_add += 1

        return edges_to_add

```