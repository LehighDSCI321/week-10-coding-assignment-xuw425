"""
This module provides classes for creating and traversing directed graphs,
including a specialized Directed Acyclic Graph (DAG) that prevents cycles.
"""
from collections import deque

# --- Base Classes (Final Version) ---

class Digraph:
    """
    A simple implementation of a directed graph using an adjacency list.
    """
    def __init__(self):
        """Initializes a new, empty Digraph."""
        self.adj = {}
        self.nodes = {}
        self.edges = {}

    def add_node(self, node, attrs=None):
        """Adds a node to the graph if it does not already exist."""
        if node not in self.adj:
            self.adj[node] = []
            self.nodes[node] = attrs

    def get_nodes(self):
        """Returns a list of all nodes in the graph."""
        return list(self.adj.keys())

    def get_node_value(self, node):
        """Returns the attributes/value of a given node."""
        return self.nodes.get(node)

    def add_edge(self, start_node, end_node, **kwargs):
        """
        Adds a directed edge from start_node to end_node and stores its attributes.
        """
        self.add_node(start_node)
        self.add_node(end_node)
        if end_node not in self.adj[start_node]:
            self.adj[start_node].append(end_node)
        self.edges[(start_node, end_node)] = kwargs

    def get_edge_weight(self, start_node, end_node):
        """Returns the 'edge_weight' attribute of an edge."""
        edge_attrs = self.edges.get((start_node, end_node), {})
        return edge_attrs.get('edge_weight')

    def successors(self, node):
        """Returns a sorted list of successors for a given node."""
        if node not in self.adj:
            raise KeyError(f"Node {node} not in graph.")
        return sorted(self.adj[node])

    def predecessors(self, node):
        """Returns a sorted list of predecessors for a given node."""
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
            """Recursive helper function for topological sort."""
            if node not in visited:
                visited.add(node)
                for neighbor in sorted(self.adj.get(node, [])):
                    visit(neighbor)
                sorted_order.insert(0, node)

        for node in sorted(list(self.adj.keys())):
            if node not in visited:
                visit(node)
        return sorted_order

# --- Classes for the Assignment (Final Version) ---

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
        stack = list(sorted(self.adj[start_node], reverse=True))
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
        queue = deque(sorted(self.adj[start_node]))

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
    def add_edge(self, start_node, end_node, **kwargs):
        """
        Adds an edge, but first checks if doing so would create a cycle.
        Raises a ValueError if a cycle is detected.
        """
        self.add_node(start_node)
        self.add_node(end_node)

        # A cycle is created if a path already exists from end_node to start_node.
        if start_node == end_node or start_node in self.dfs(end_node):
            raise ValueError(
                f"Adding edge from {start_node} to {end_node} creates a cycle."
            )

        super().add_edge(start_node, end_node, **kwargs)
