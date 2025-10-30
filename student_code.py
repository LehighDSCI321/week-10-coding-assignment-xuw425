from collections import deque

# --- Base Classes (Assumed to be provided) ---

class Digraph:
    """
    A simple implementation of a directed graph using an adjacency list.
    """
    def __init__(self):
        # adj is a dictionary mapping each node to a list of its neighbors.
        self.adj = {}

    def add_node(self, node):
        """Adds a node to the graph if it does not already exist."""
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, start_node, end_node):
        """Adds a directed edge from start_node to end_node."""
        self.add_node(start_node)
        self.add_node(end_node)
        if end_node not in self.adj[start_node]:
            self.adj[start_node].append(end_node)

    def __repr__(self):
        return f"Digraph({self.adj})"

class SortableDigraph(Digraph):
    """
    Inherits from Digraph. This class is a placeholder for a sortable graph.
    """
    def __init__(self):
        super().__init__()

# --- Classes for the Assignment ---

class TraversableDigraph(SortableDigraph):
    """
    Extends SortableDigraph with DFS and BFS traversal methods.
    """
    def dfs(self, start_node):
        """
        Performs a depth-first search (DFS) traversal.
        Returns a set of all nodes reachable from start_node.
        """
        if start_node not in self.adj:
            raise KeyError(f"Node {start_node} not in graph.")
        
        visited = set()
        stack = [start_node] # Use a list as a stack for DFS

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                # Add unvisited neighbors to the stack
                for neighbor in sorted(self.adj[node], reverse=True):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited

    def bfs(self, start_node):
        """
        Performs a breadth-first search (BFS) traversal.
        This method is a generator, yielding nodes one by one.
        """
        if start_node not in self.adj:
            raise KeyError(f"Node {start_node} not in graph.")
        
        visited = {start_node}
        queue = deque([start_node]) # Use a deque for an efficient queue

        while queue:
            node = queue.popleft()
            yield node # Yield the current node
            # Add unvisited neighbors to the queue
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
        # We can check this by running a traversal from end_node.
        if start_node in self.dfs(end_node):
            raise ValueError(
                f"Adding edge from {start_node} to {end_node} creates a cycle."
            )
        
        # If no cycle is detected, add the edge using the parent's method.
        super().add_edge(start_node, end_node)


# --- Test Code ---
if __name__ == "__main__":
    # 1. Create a DAG instance based on the clothing example
    clothing_dag = DAG()
    print("Building the clothing DAG...")
    try:
        clothing_dag.add_edge("shirt", "tie")
        clothing_dag.add_edge("shirt", "vest")
        clothing_dag.add_edge("pants", "belt")
        clothing_dag.add_edge("pants", "shoes")
        clothing_dag.add_edge("socks", "shoes")
        clothing_dag.add_edge("tie", "jacket")
        clothing_dag.add_edge("belt", "jacket")
        clothing_dag.add_edge("vest", "jacket")
        print("Initial edges added successfully.")
        print("Current Graph:", clothing_dag)
    except ValueError as e:
        print(f"Error during graph creation: {e}")

    # 2. Test traversals
    print("\n--- Testing Traversals from 'shirt' ---")
    dfs_result = clothing_dag.dfs("shirt")
    print("DFS visited nodes:", sorted(list(dfs_result)))

    bfs_result = list(clothing_dag.bfs("shirt"))
    print("BFS traversal order:", bfs_result)
    
    # 3. Test cycle detection
    print("\n--- Testing Cycle Detection ---")
    print("Attempting to add edge 'jacket' -> 'shirt' (should fail)...")
    try:
        clothing_dag.add_edge("jacket", "shirt")
    except ValueError as e:
        print(f"Success: Caught expected error: {e}")
        
    print("\nAttempting to add valid edge 'vest' -> 'shoes' (should succeed)...")
    try:
        clothing_dag.add_edge("vest", "shoes")
        print("Edge ('vest', 'shoes') added successfully.")
        print("Updated Graph:", clothing_dag)
    except ValueError as e:
        print(f"Caught unexpected error: {e}")
