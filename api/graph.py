from edge import Edge
from node import Node


class Graph:

    def __init__(self, edges: list[Edge], nodes: list[Node]):
        self.edges = edges
        self.nodes = nodes

    def remove_node(self):
        pass

    def add_node(self, node: Node):
        pass

    def add_edge(self, edge: Edge):
        pass

    def get_nodes(self) -> list[Node]:
        pass
