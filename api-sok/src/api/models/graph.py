from .edge import Edge
from .node import Node


class Graph:
    """
    A class representing a graph structure composed of nodes and edges.

    Attributes:
        edges (set): A set of edges in the graph.
        nodes (set): A set of nodes in the graph.
        directed (bool): A boolean indicating whether the graph is directed.
        root_id (str): Identifier for the root node in the graph.
    """

    def __init__(self, edges=None, nodes=None, directed=True, root_id=None):
        """
        Initializes a Graph object.

        Args:
            edges (set, optional): A set of edges to initialize the graph with. Defaults to None.
            nodes (set, optional): A set of nodes to initialize the graph with. Defaults to None.
            directed (bool, optional): Indicates whether the graph is directed. Defaults to True.
            root_id (str, optional): Identifier for the root node in the graph. Defaults to None.
        """
        if nodes is None:
            nodes = set()
        if edges is None:
            edges = set()
        self.edges = edges
        self.nodes = nodes
        self.directed = directed
        self.root_id = root_id

    def remove_node(self, node: Node):
        """
        Removes a node from the graph along with its incident edges.

        Args:
            node (Node): The node to be removed from the graph.
        """
        self.nodes.remove(node)
        self.edges = [
            edge for edge in self.edges if edge.src != node and edge.dest != node
        ]
        for node in self.nodes:
            node.edges = list(
                filter(
                    lambda edge: edge.src in self.nodes and edge.dest in self.nodes,
                    node.edges,
                )
            )

    def add_node(self, node: Node):
        """
        Adds a node to the graph.

        Args:
            node (Node): The node to be added to the graph.
        """
        self.nodes.add(node)

    def add_edge(self, edge: Edge):
        """
        Adds an edge to the graph, along with its incident nodes.

        Args:
            edge (Edge): The edge to be added to the graph.
        """
        self.add_node(edge.src)
        self.add_node(edge.dest)

        if edge not in self.edges:
            self.edges.add(edge)

            if not self.directed:
                inverted_edge = Edge(edge.data, edge.dest, edge.src)
                self.edges.add(inverted_edge)

            for node in self.nodes:
                if node == edge.src:
                    node.edges.append(edge)
                if not self.directed and node == edge.dest:
                    node.edges.append(inverted_edge)

    def get_nodes(self) -> set[Node]:
        """
        Retrieves all nodes in the graph.

        Returns:
            set[Node]: A set containing all nodes in the graph.
        """
        return self.nodes

    def get_edges(self) -> list[Edge]:
        """
        Retrieves all edges in the graph.

        Returns:
            list[Edge]: A list containing all edges in the graph.
        """
        return list(self.edges)
