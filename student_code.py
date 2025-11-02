"""Module for graph data structures including traversable directed graphs and DAGs"""
from collections import deque

class SortableDigraph:
    """Base class for a sortable directed graph."""
    def __init__(self):
        """Initialize an empty directed graph."""
        self.graph = {}
        self.node_values = {}
        self.edge_weights = {}

    def add_node(self, node, value=None):
        """Add a node to the graph."""
        if node not in self.graph:
            self.graph[node] = []
        if value is not None:
            self.node_values[node] = value

    def add_edge(self, start, end, edge_weight=None):
        """Add a directed edge from start to end."""
        if start not in self.graph:
            self.add_node(start)
        if end not in self.graph:
            self.add_node(end)
        if end not in self.graph[start]:
            self.graph[start].append(end)
        if edge_weight is not None:
            self.edge_weights[(start, end)] = edge_weight

    def __contains__(self, node):
        """Check if a node exists in the graph."""
        return node in self.graph

    def __getitem__(self, node):
        """Get the neighbors of a node."""
        return self.graph.get(node, [])

    def get_edge_weight(self, start, end):
        """Get the weight of an edge from start to end."""
        return self.edge_weights.get((start, end))

    def successors(self, node):
        """Get the list of successor nodes"""
        return self.graph.get(node, [])

    def predecessors(self, node):
        """Get the list of predecessor nodes"""
        preds = []
        for n, neighbors in self.graph.items():
            if node in neighbors:
                preds.append(n)
        return preds

class TraversableDigraph(SortableDigraph):
    """Augments SortableDigraph with traversal methods"""

    def dfs(self, start):
        """Perform depth-first search traversal from the start node"""
        visited = set()
        stack = [start]

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            if node != start:
                yield node

            # Add neighbors to stack
            neighbors = self[node]
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

    def bfs(self, start):
        """Perform breadth-first search traversal from the start node"""
        visited = set()
        queue = deque([start])

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            if node != start:
                yield node

            for neighbor in self[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

class DAG(TraversableDigraph):
    """Directed Acyclic Graph - inherits from TraversableDigraph"""

    def add_edge(self, start, end, edge_weight=None):
        """Add an edge from start to end, but only if it doesn't create a cycle"""

        if start not in self:
            self.add_node(start)
        if end not in self:
            self.add_node(end)

        if self._has_path(end, start):
            raise ValueError(
                f"Cannot add edge from '{start}' to '{end}': "
                f"would create a cycle (path already exists from "
                f"'{end}' to '{start}')"
            )

        super().add_edge(start, end, edge_weight)

    def _has_path(self, start, target):
        """Check if there's a path from start to target"""

        if start not in self:
            return False

        # Use BFS to search for target
        for node in self.bfs(start):
            if node == target:
                return True
        return False

    def top_sort(self):
        """Perform topological sort on the DAG"""

        in_degree = {node: 0 for node in self.graph}
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                in_degree[neighbor] += 1

        queue = deque([node for node in self.graph if in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result
