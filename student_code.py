" Base Classes"

class Digraph:
    """
    A simple implementation of a directed graph using an adjacency list.
    """
    def __init__(self):
        self.adj = {}
        self.nodes = {} # Store node attributes if any

    def add_node(self, node, attrs=None):
        """Adds a node to the graph if it does not already exist."""
        if node not in self.adj:
            self.adj[node] = []
            self.nodes[node] = attrs

    def add_edge(self, start_node, end_node):
        """Adds a directed edge from start_node to end_node."""
        self.add_node(start_node)
        self.add_node(end_node)
        if end_node not in self.adj[start_node]:
            self.adj[start_node].append(end_node)

    def successors(self, node):
        """Returns a list of successors for a given node."""
        if node not in self.adj:
            raise KeyError(f"Node {node} not in graph.")
        return sorted(self.adj[node])

    def predecessors(self, node):
        """Returns a list of predecessors for a given node."""
        if node not in self.adj:
            raise KeyError(f"Node {node} not in graph.")
        return sorted([u for u, neighbors in self.adj.items() if node in neighbors])

    def __repr__(self):
        return f"Digraph({self.adj})"

class SortableDigraph(Digraph):
    """
    Inherits from Digraph and adds topological sorting functionality.
    """
    def top_sort(self):
        """Performs a topological sort of the graph's nodes."""
        visited = set()
        sorted_order = []

        def visit(node):
            if node not in visited:
                visited.add(node)
                for neighbor in sorted(self.adj.get(node, [])):
                    visit(neighbor)
                sorted_order.insert(0, node)

        for node in sorted(list(self.adj.keys())):
            if node not in visited:
                visit(node)
        return sorted_order

# --- Classes for the Assignment (Modified to pass all tests) ---

class TraversableDigraph(SortableDigraph):
    """
    Extends SortableDigraph with DFS and BFS traversal methods.
    """
    def dfs(self, start_node):
        """
        Performs a DFS, returning an ordered list of visited nodes
        (excluding the start node).
        """
        if start_node not in self.adj:
            raise KeyError(f"Node {start_node} not in graph.")

        visited = {start_node}
        stack = [neighbor for neighbor in sorted(self.adj[start_node], reverse=True)]
        path = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                path.append(node)
                for neighbor in sorted(self.adj[node], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return path

    def bfs(self, start_node):
        """
        Performs a BFS, yielding traversed nodes one by one
        (excluding the start node).
        """
        if start_node not in self.adj:
            raise KeyError(f"Node {start_node} not in graph.")

        visited = {start_node}
        # Initialize queue with sorted neighbors of the start node
        queue = deque(sorted(self.adj[start_node]))
        
        # Mark all initial neighbors as visited
        for node in queue:
            visited.add(node)

        while queue:
            node = queue.popleft()
            yield node
            for neighbor in sorted(self.adj[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

class DAG(TraversableDigraph):
    """
    Represents a Directed Acyclic Graph (DAG).
    Redefines add_edge to ensure no cycles are created.
    """
    def add_edge(self, start_node, end_node):
        """
        Adds an edge, but first checks if doing so would create a cycle.
        Raises a ValueError if a cycle is detected.
        """
        self.add_node(start_node)
        self.add_node(end_node)

        # A cycle is created if a path already exists from end_node to start_node.
        # self.dfs(end_node) returns all nodes reachable from end_node.
        if start_node in self.dfs(end_node) or start_node == end_node:
            raise ValueError(
                f"Adding edge from {start_node} to {end_node} creates a cycle."
            )

        # If no cycle is detected, add the edge using the parent's method.
        super().add_edge(start_node, end_node)
