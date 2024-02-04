from .edge import Edge
from .node import Node


class Graph:

    def __init__(self, edges: list[Edge] = [], nodes: set[Node] = set()):
        self.edges = edges
        self.nodes = nodes

    def remove_node(self, node: Node):
        self.nodes.remove(node)

    def add_node(self, node: Node):
        self.nodes.add(node)

    def add_edge(self, edge: Edge):
        self.add_node(edge.src)
        self.add_node(edge.dest)
        self.edges.append(edge)

    def get_nodes(self) -> list[Node]:
        return self.nodes
