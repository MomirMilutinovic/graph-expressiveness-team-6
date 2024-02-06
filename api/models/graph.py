from .edge import Edge
from .node import Node


class Graph:

    def __init__(self, edges=None, nodes=None):
        if nodes is None:
            nodes = set()
        if edges is None:
            edges = []
        self.edges = edges
        self.nodes = nodes

    def remove_node(self, node: Node):
        self.nodes.remove(node)
        self.edges = [
            edge for edge in self.edges if edge.src != node and edge.dest != node
        ]

    def add_node(self, node: Node):
        self.nodes.add(node)

    def add_edge(self, edge: Edge):
        self.add_node(edge.src)
        self.add_node(edge.dest)
        self.edges.append(edge)

        for node in self.nodes:
            if node == edge.src:
                node.edges.append(edge)
            if node == edge.dest:
                node.edges.append(edge)

    def get_nodes(self) -> set[Node]:
        return self.nodes

    def get_edges(self) -> list[Edge]:
        return self.edges
